{
    'name': 'xx_realEstate',
    'author': 'Immomakers',
    'category': 'Company',
    'description': """
Dit is de module voor viaSofie
""",
    'version': '1.0',
    'depends': ['base', 'product', 'calendar', 'website_sale'],
    'data': ['views/partner.xml', 'views/transaction.xml', 'views/attribute.xml', 'views/house.xml', 'views/city.xml',
             'views/house_type.xml', 'views/document.xml', 'views/house_sequence.xml', 'views/visitor.xml',
             'views/status.xml', 'views/ebook.xml', 'security/ir.model.access.csv'],
    'installable': True,
}
