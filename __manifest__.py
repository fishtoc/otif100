{
    'name': 'OTIF 100',
    'description': 'Production control system to achieve 100% On Time In Full delivery',
    'author': 'Matias Birrell R.',
    'website': 'https://www.ingeser.cl',
    'category': 'PRO',
    'version': '1.1.0',
    'depends': [
        'base',
    ],
    'data': [  # Todos los archivos CSV y XML que va a detectar el sistema
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/partner.xml',
        'views/otif100.xml',
        'views/work_order.xml',
        'views/family.xml',
        'views/sku.xml',
        'views/nonworkingdays.xml',
    ]
}
