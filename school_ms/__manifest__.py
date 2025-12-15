# -*- coding: utf-8 -*-
{
    'name': "school_ms",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'seqauence':"-100",
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','mail','account'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/menus.xml',
        'wizard/change_student_state_wizard_view.xml',
        'wizard/change_class_state_wizard_view.xml',
        'views/school_students_view.xml',
        'views/school_classes_view.xml',
        'views/study_material_view.xml',
        'views/education_stages_view.xml',
        'views/class_schedule_view.xml',
        'data/sequence_data.xml',
        'data/report_class_schedule.xml',
        'data/report_students_info.xml'

    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

