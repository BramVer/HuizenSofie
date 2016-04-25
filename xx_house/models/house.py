from openerp import models, fields, api, exceptions
from reportlab.graphics.barcode import createBarcodeDrawing
import base64


class House(models.Model):
    _inherit = 'product.template'

    xx_house_type = fields.Many2one('xx.house.type', 'House type')
    name = fields.Char(compute='_get_name', store=True, default='', string='Address')
    xx_street = fields.Char('Street name', required=True)
    xx_street_number = fields.Char('Street number', required=True)
    xx_city = fields.Many2one('xx.city', 'City')
    xx_zip = fields.Char('Zip code', required=True)
    xx_provence = fields.Selection(
        [('antwerpen', 'Antwerpen'), ('limburg', 'Limburg'), ('oostvlaanderen', 'Oost-Vlaanderen'),
         ('westvlaanderen', 'West-Vlaanderen'), ('brussel', 'Brussel'), ('henegouwen', 'Henegouwen'), ('luik', 'Luik'),
         ('namen', 'Namen'), ('luxemburg', 'Luxemburg')], string='Provence', required=True)
    xx_starting_price = fields.Float('Starting price', required=True)
    xx_current_price = fields.Float('Current price')
    xx_total_area = fields.Integer('Total surface', required=True)
    xx_living_area = fields.Integer('Total living area', required=True)
    xx_energy = fields.Float('Energy', required=True)
    xx_unique_epc = fields.Float('EPC code', required=True)
    xx_attribute = fields.One2many('xx.house.attribute', 'name', 'Attributes')

    xx_seller_id = fields.Many2one('res.partner', string='Verkoper', required=True)


    @api.depends('xx_street', 'xx_street_number')
    def _get_name(self):
        if self.xx_street and self.xx_street_number:
            self.name = self.xx_street + ' ' + self.xx_street_number

    @api.onchange('xx_city')
    def _onchange_city(self):
        if self.xx_city:
            self.xx_zip = self.xx_city.xx_zip


class HouseType(models.Model):
    _name = 'xx.house.type'

    name = fields.Char('House type', required=True)


class QrCode(models.Model):
    _inherit = 'product.template'

    image = fields.Binary('QR code')
    xx_width = fields.Integer('Width')
    xx_height = fields.Integer('Height')

    def generate_image(self, cr, uid, ids, context=None):
        #TODO form correct URL, waiting for server
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.xx_width and self_obj.xx_height:
                options = {'width': self_obj.xx_width, 'height': self_obj.xx_height}
            else:
                options = {'width': 0, 'hight': 0}
            ret_val = createBarcodeDrawing('QR', value=str('Groep 2 is de beste groep!'), **options)
            image = base64.encodestring(ret_val.asString('png'))
            self.write(cr, uid, self_obj.id,
                       {'image': image}, context=context)
        return True


class HouseAttribute(models.Model):
    _name = 'xx.house.attribute'

    name = fields.Many2one('xx.house.attribute.type', 'Attribute', required=True)
    xx_amount = fields.Integer('Amount')
    xx_surface = fields.Integer('Square feet')
    xx_note = fields.Text('Extra info')


class HouseAttributeType(models.Model):
    _name = 'xx.house.attribute.type'

    name = fields.Char('Attribute type', required=True)


class Image(models.Model):
    _inherit = 'product.template'

    xx_image1 = fields.Binary('')
    xx_image2 = fields.Binary('')
    xx_image3 = fields.Binary('')
    xx_image4 = fields.Binary('')
    xx_image5 = fields.Binary('')
    xx_image6 = fields.Binary('')
    xx_image7 = fields.Binary('')
    xx_image8 = fields.Binary('')
    xx_image9 = fields.Binary('')
    xx_image10 = fields.Binary('')


class City(models.Model):
    _name = 'xx.city'

    name = fields.Char('City name', required=True)
    xx_zip = fields.Char('Zip code', required=True)
