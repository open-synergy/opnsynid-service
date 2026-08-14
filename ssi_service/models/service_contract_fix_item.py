# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class ServiceContractFixItem(models.Model):
    """Read-only SQL view aggregating fix items per contract.

    Rows are grouped from ``service.contract_fix_item_payment_term_detail``
    (see :meth:`_from`/:meth:`_join`) so the contract form can show one
    line per product regardless of how many payment terms reference it.
    This model is a database view (``_auto = False``): it is never
    written to directly, only rebuilt by :meth:`init`.
    """

    _name = "service.contract_fix_item"
    _auto = False
    _inherit = [
        "service.fix_item_mixin",
    ]
    _description = "Service Contract Fix Item"
    _order = "service_id, sequence, product_category_id, product_id, id"

    service_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
    )

    def _select(self):
        """Return the SQL ``SELECT`` clause of the aggregation view.

        ``ROW_NUMBER() OVER()`` is given an explicit ``ORDER BY`` on the
        exact same columns as :meth:`_group_by`. Those columns already
        form a complete, unique sort key for the aggregated output (it
        is what the ``GROUP BY`` groups on), so ordering by them makes
        the row-to-number assignment deterministic and repeatable
        across separate queries against the same underlying data --
        without it, PostgreSQL is free to hand out row numbers in
        whatever order its query plan happens to produce them, which is
        not guaranteed to match between two separate ``SELECT``s (even
        back-to-back ones with no writes in between). Since this
        aggregated view has no other stable identity for a row --
        multiple ``service_contract_fix_item_payment_term_detail`` rows
        can merge into one output row -- an unstable id here is not
        just "sometimes stale in the ORM cache": a fresh read for
        "id N" can genuinely resolve to a *different* logical row than
        an earlier read for that same "id N" did, silently mixing
        unrelated rows' field values together for any caller that
        re-reads by id (see ``ssi_service_revenue_recognition``'s
        ``pob_id`` compute, which does exactly that and was the
        reporter of this bug -- OFS/26/000027).

        :return: str, the ``SELECT`` clause used by :meth:`init`.
        """
        select_str = """
        SELECT
            ROW_NUMBER() OVER(
                ORDER BY   c.id,
                           a.product_category_id,
                           a.product_id,
                           a.name,
                           a.price_unit,
                           a.uom_id
            ) AS id,
            c.id AS service_id,
            a.product_id AS product_id,
            a.product_category_id as product_category_id,
            a.name AS name,
            a.price_unit AS price_unit,
            a.uom_id AS uom_id,
            SUM(a.quantity) AS quantity,
            MAX(a.sequence) AS sequence,
            SUM(a.price_subtotal) AS amount_untaxed,
            SUM(a.price_tax) AS amount_tax,
            SUM(a.price_total) AS amount_total
        """
        return select_str

    def _from(self):
        """Return the SQL ``FROM`` clause of the aggregation view.

        :return: str, the ``FROM`` clause used by :meth:`init`.
        """
        from_str = """
        service_contract_fix_item_payment_term_detail AS a
        """
        return from_str

    def _where(self):
        """Return the SQL ``WHERE`` clause of the aggregation view.

        :return: str, the ``WHERE`` clause used by :meth:`init`.
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        """Return the SQL ``JOIN`` clauses of the aggregation view.

        :return: str, the ``JOIN`` clauses used by :meth:`init`.
        """
        join_str = """
        JOIN service_contract_fix_item_payment_term AS b
            ON a.term_id = b.id
        JOIN service_contract AS c
            ON b.service_id = c.id
        """
        return join_str

    def _group_by(self):
        """Return the SQL ``GROUP BY`` clause of the aggregation view.

        :return: str, the ``GROUP BY`` clause used by :meth:`init`.
        """
        group_str = """
        GROUP BY    c.id,
                    a.product_category_id,
                    a.product_id,
                    a.name,
                    a.price_unit,
                    a.uom_id
        """
        return group_str

    def init(self):
        """Create the backing SQL view, replacing it if it exists.

        Combines :meth:`_select`, :meth:`_from`, :meth:`_join`,
        :meth:`_where`, and :meth:`_group_by` into a single
        ``CREATE OR REPLACE VIEW`` statement, run once at module
        installation/update time.
        """
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
