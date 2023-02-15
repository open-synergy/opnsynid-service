# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import logging


def migrate(cr, version):
    if not version:
        return
    logger = logging.getLogger(__name__)
    logger.info("Updating project_project...")
    cr.execute(
        """
    UPDATE
        project_project pr
    SET
        name = sr.title,
        code = sr.name
    FROM service_contract sr
    WHERE
        pr.id = sr.project_id AND
        sr.auto_create_project IS true;
    """
    )
    logger.info("Successfully updated project_project tables")
