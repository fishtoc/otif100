{
    'name': 'OTIF 100',
    'description': 'Sistema para controlar la producción y lograr 100% de entrega a tiempo',
    'author': 'Matias Birrell R.',
    'website': 'https://www.ingeser.cl',
    'category': 'PRO',
    'version': '0.0.1',
    'depends': [
        'base',
    ],
    'data': [  # Todos los archivos CSV y XML que va a detectar el sistema
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/otif100.xml',
        'views/work_order.xml',
        'views/family.xml',
        'views/sku.xml',
    ]
}
