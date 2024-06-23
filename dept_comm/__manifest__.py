{
    'name': "Workflow Ponctuel",
    'depends': ['base', 'dept_wk'],
    'sequence': '30',
    'author': "FINOUTSOURCE",
    'category': 'Extra Tools',
    'summary': "Module pour le financement",
    # data files always loaded at installation
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
            'reports/mail_template.xml',
            'data/state_data.xml',
            'reports/report.xml',
            'views/workflow_new.xml',
            'views/wizard.xml'],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

    'assets': {
        'web.assets_backend': [
            'dept_wk/static/src/css/custom_styles.css',
            'dept_wk/static/src/css/custom_font.css',  # Path to your CSS file
        ],
        'web.report_assets_common': [
            'dept_wk/static/src/css/custom_font.css',  # Path to your CSS file
        ],
    },
}
