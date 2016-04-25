{
    'name': 'xx_house',
    'author': 'BramBonar',
    'category': 'Company',
    'description': """
Dit is de module waarin huizen kunnen beheerd worden
""",
    'version': '1.0',
    'depends': ['base', 'product'],
    'data': ['views/house.xml', 'views/attribute.xml'],
    'depends': ['base', 'product', 'xx_realEstate'],
    'data': ['views/house.xml'],
    'installable': True,
}