import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-service",
    description="Meta package for open-synergy-opnsynid-service Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_service',
        'odoo14-addon-ssi_service_project',
        'odoo14-addon-ssi_service_quality_control',
        'odoo14-addon-ssi_service_quotation',
        'odoo14-addon-ssi_service_quotation_lead',
        'odoo14-addon-ssi_service_quotation_project',
        'odoo14-addon-ssi_service_quotation_risk_analysis',
        'odoo14-addon-ssi_service_quotation_risk_analysis_lead',
        'odoo14-addon-ssi_service_quotation_work_log',
        'odoo14-addon-ssi_service_risk_analysis',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
