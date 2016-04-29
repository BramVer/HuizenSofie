from openerp import models, fields, api, exceptions
from reportlab.graphics.barcode import createBarcodeDrawing
import base64


class House(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    xx_display_name = fields.Char('Display naam')
    xx_house_type = fields.Many2one('xx.house.type', 'Huis type')
    name = fields.Char(compute='_get_name', store=True, default='', string='Adres')
    xx_street = fields.Char('Straatnaam', required=True)
    xx_street_number = fields.Char('Huisnummer', required=True)
    xx_city = fields.Many2one('xx.city', 'City')
    xx_zip = fields.Char('Postcode', required=True)
    xx_provence = fields.Selection(
        [('antwerpen', 'Antwerpen'), ('limburg', 'Limburg'), ('oostvlaanderen', 'Oost-Vlaanderen'),
         ('westvlaanderen', 'West-Vlaanderen'), ('brussel', 'Brussel'), ('henegouwen', 'Henegouwen'), ('luik', 'Luik'),
         ('namen', 'Namen'), ('luxemburg', 'Luxemburg')], string='Provincie', required=True)
    xx_starting_price = fields.Float('Start prijs', required=True)
    xx_current_price = fields.Float('Huidige prijs')
    xx_total_area = fields.Integer('Totale oppervlakte', required=True)
    xx_living_area = fields.Integer('Bewoonbare oppervlakte', required=True)
    xx_energy = fields.Float('Energie', required=True)
    xx_unique_epc = fields.Float('EPC code', required=True)
    xx_sold = fields.Boolean('Verkocht')

    xx_attribute = fields.One2many('xx.house.attribute', 'xx_house', 'Attributen')
    xx_documents = fields.One2many('xx.house.document', 'name', 'Documenten')


    xx_seller_id = fields.Many2one('res.partner', string='Verkoper', required=True)
    xx_transaction_id = fields.Many2one('xx.transaction', string='Transactie')


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

    name = fields.Char('Huistype', required=True)

    _sql_constraints = [
        ('house_type_unique', 'unique(name)', 'Huistype bestaat al!')
    ]


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

    name = fields.Many2one('xx.house.attribute.type', 'Attribuut', required=True)
    xx_house = fields.Many2one('product.template', 'Huis')
    xx_exists = fields.Boolean('Zichtbaar')
    xx_value = fields.Char('Waarde')
    xx_unit_type = fields.Char('Eenheid')
    xx_note = fields.Text('Extra info')

    @api.onchange('name')
    def _onchange_attribute(self):
        current_attributetype_obj = self.name
        self.xx_unit_type = current_attributetype_obj.xx_unit


class HouseAttributeType(models.Model):
    _name = 'xx.house.attribute.type'

    name = fields.Char('Attribuut type', required=True)
    xx_unit = fields.Char('Eenheid')




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

    name = fields.Char('Gemeente', required=True)
    xx_zip = fields.Char('Postcode', required=True)

class HouseDocument(models.Model):
    _name = 'xx.house.document'

    name = fields.Many2one('xx.house.document.type', 'Document', required=True)
    xx_exists = fields.Boolean('Aanwezig')


class HouseDocumentType(models.Model):
    _name = 'xx.house.document.type'

    name = fields.Char('Document type', required=True)


