from openerp import models, fields, api, exceptions
from reportlab.graphics.barcode import createBarcodeDrawing
import base64
from openerp.tools.translate import _
import datetime

WEBSITE_URL = 'http://0.0.0.0:8069/shop/product/'
QR_URL = 'http://0.0.0.0:8069/web/image?model=product.template&id='
QR_ATTRIBUTE = '&field=image'


class House(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    xx_display_name = fields.Char('Weergave naam', required=True)
    xx_house_type = fields.Many2one('xx.house.type', 'Huis type', required=True)
    name = fields.Char(compute='_get_name', store=True, default='', string='Adres')
    xx_street = fields.Char('Straatnaam', required=True)
    xx_street_number = fields.Char('Huisnummer', required=True)
    xx_city = fields.Many2one('xx.city', 'Gemeente', required=True)
    xx_zip = fields.Char('Postcode', required=True)
    xx_provence = fields.Selection(
        [('antwerpen', 'Antwerpen'), ('limburg', 'Limburg'), ('oostvlaanderen', 'Oost-Vlaanderen'),
         ('westvlaanderen', 'West-Vlaanderen'), ('brussel', 'Brussel'), ('henegouwen', 'Henegouwen'), ('luik', 'Luik'),
         ('namen', 'Namen'), ('luxemburg', 'Luxemburg')], string='Provincie', required=True)
    xx_starting_price = fields.Float('Start prijs', required=True)
    xx_current_price = fields.Float('Huidige prijs', required=True)
    xx_total_area = fields.Integer('Totale oppervlakte', required=True)
    xx_living_area = fields.Integer('Bewoonbare oppervlakte', required=True)
    xx_unique_epc = fields.Char('EPC code')
    xx_sold = fields.Boolean('Verkocht')
    xx_buy_hire = fields.Selection([('huren', 'Huren'), ('kopen', 'Kopen'), ('beide', 'Beide')], string='Kopen/Huren',
                                   required=True)
    xx_description = fields.Text('Omschrijving', required=True)
    xx_build_year = fields.Char('Bouwjaar')
    xx_reference = fields.Char('Referentie')

    xx_attribute = fields.One2many('xx.house.attribute', 'xx_house', 'Attributen')
    xx_documents = fields.One2many('xx.house.document', 'xx_house', 'Documenten')

    xx_visitor_count = fields.Integer('Bezoekers', compute='_get_visitors')
    xx_visitors = fields.One2many('xx.house.visitors', 'xx_house', 'Bezoekers')
    xx_visitor_ids = fields.Many2many("xx.house.visitors", string='Bezoekers', compute="_get_visitors", readonly=True,
                                      copy=False)

    xx_seller_id = fields.Many2one('res.partner', string='Verkoper', required=True)
    xx_transaction_id = fields.Many2one('xx.transaction', string='Transactie')
    xx_status_id = fields.Many2one('xx.house.status', string='Status', required=True)

    @api.constrains('xx_build_year')
    def _check_build_year_valid(self):
        if self.xx_build_year:
            bouwjaar = self.xx_build_year
            if not bouwjaar.isdigit():
                raise exceptions.ValidationError("Bouwjaar is niet geldig")

    @api.multi
    def action_view_visitor(self):
        invoice_ids = self.mapped('xx_visitor_ids')
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('xx_realEstate.xx_visitor_list_action')
        list_view_id = imd.xmlid_to_res_id('xx_realEstate.xx_visitor_tree_view')
        form_view_id = imd.xmlid_to_res_id('xx_realEstate.xx_visitor_form_view')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'],
                      [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        if len(invoice_ids) >= 0:
            result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
        elif len(invoice_ids) == 1:
            result['views'] = [(form_view_id, 'form')]
            result['res_id'] = invoice_ids.ids[0]
        return result

    @api.multi
    def _get_visitors(self):
        for record in self:
            xx_visitor_ids = record.xx_visitors.mapped('id')
            record.update({
                'xx_visitor_count': len(record.xx_visitors),
                'xx_visitor_ids': xx_visitor_ids
            })

    @api.model
    def create(self, vals):
        # TODO Use sequence to fetch the reference
        reference_dict = {
            'xx_reference': str(len(self.search_read([], ['id']))) + str(datetime.datetime.now().microsecond)}
        vals.update(reference_dict)
        new_obj = super(House, self).create(vals)
        new_obj.generate_image(new_obj.xx_street, new_obj.xx_street_number, new_obj.id)
        return new_obj

    @api.onchange('xx_starting_price')
    def _onchange_starting_price(self):
        if self.xx_current_price:
            self.xx_current_price = self.xx_starting_price
            warning = {
                'title': _('Opgelet'),
                'message': _(
                    'Het veranderen van de startprijs past automatisch de huidige prijs aan')
            }
            return {'warning': warning}
        self.xx_current_price = self.xx_starting_price

    # TODO does the format change? Else delete
    @api.onchange('xx_current_price')
    def _onchange_current_price(self):
        self.xx_starting_price = self.xx_starting_price

    @api.depends('xx_street', 'xx_street_number')
    def _get_name(self):
        if self.xx_street and self.xx_street_number:
            self.name = self.xx_street + ' ' + self.xx_street_number

    @api.onchange('xx_city')
    def _onchange_city(self):
        if self.xx_city:
            self.xx_zip = self.xx_city.xx_zip

    @api.multi
    def show_current_house(self):
        current_url = WEBSITE_URL + (
            self.xx_street + "-" + self.xx_street_number + "-" + str(self.id)).lower()
        return {
            'name': 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'current',
            'url': current_url
        }

    @api.multi
    def show_qr_image(self):
        return {
            'name': 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'current',
            'url': QR_URL + str(self.id) + QR_ATTRIBUTE
        }

    @api.multi
    def create_transaction(self):
        if self.id:
            if not self.xx_transaction_id:
                self.xx_sold = True
                view_ref = self.env['ir.model.data'].get_object_reference('xx_realEstate', 'xx_transaction_form_view')
                view_id = view_ref[1] if view_ref else False
                t_name = "T" + str(self.id).zfill(6)
                res = {
                    'type': 'ir.actions.act_window',
                    'name': 'Transaction',
                    'res_model': 'xx.transaction',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': view_id,
                    'target': 'current',
                    'context': {'default_xx_house_id': self.id,
                                'default_xx_transactionSeller': self.xx_seller_id.id,
                                'default_name': t_name,
                                'default_xx_price': self.xx_current_price,
                                'default_xx_date': datetime.datetime.today().strftime('%Y-%m-%d')
                                }
                }
                return res
            else:
                raise exceptions.Warning(
                    "Er bestaat al een transactie voor deze woning, voor elke woning kan er maar 1 transactie bestaan")
        else:
            raise exceptions.Warning("De woning moet opgeslagen worden voor er een transactie kan aangemaakt worden")

    @api.multi
    def delete_transaction(self):
        if self.xx_transaction_id:
            self.xx_sold = False
            self.xx_transaction_id.unlink()

        else:
            raise exceptions.Warning("Er is nog geen transactie opgeslagen voor deze woning")

    @api.multi
    def next_status(self):
        if self.xx_status_id:
            xhs = self.env['xx.house.status']
            position = self.xx_status_id.xx_position

            status = xhs.search([('xx_position', '=', position + 1)])
            if status:
                status2 = xhs.search([('xx_position', '=', position + 2)])
                if not status2:
                    return self.create_transaction()
                self.xx_status_id = status.id
            else:
                raise exceptions.Warning("De woning bevindt zich in de laatste status")

    @api.multi
    def previous_status(self):
        if self.xx_status_id:

            xhs = self.env['xx.house.status']
            position = self.xx_status_id.xx_position
            status = xhs.search([('xx_position', '=', position - 1)])
            if status:
                self.xx_status_id = status.id
                status2 = xhs.search([('xx_position', '=', position + 1)])
                if not status2:
                    self.delete_transaction()
            else:
                raise exceptions.Warning("De woning bevindt zich in de eerste status")

    @api.onchange('xx_house_type')
    def _onchange_house_type(self):
        if self.xx_house_type:
            xha = self.env['xx.house.attribute']
            house_type = self.xx_house_type
            attribute_types = house_type.xx_attribute_types
            attributes = []

            for type in attribute_types:
                vals = {
                    'name': type.id,
                    'xx_house': self.id,
                    'xx_unit_type': type.xx_unit
                }
                attr = xha.create(vals)
                attributes.append(attr.id)
            self.xx_attribute = attributes

    @api.model
    def default_get(self, vals):
        res = super(House, self).default_get(vals)
        xhd = self.env['xx.house.document']
        docu_types = self.env['xx.house.document.type'].search([('name', '!=', False)])
        if len(docu_types) > 0:

            documents = []
            for type in docu_types:
                vals = {
                    'name': type.id,
                    'xx_house': self.id,
                    'xx_exists': False
                }
                docu = xhd.create(vals)
                documents.append(docu.id)
            res.update({
                'xx_documents': documents
            })

        xhs = self.env['xx.house.status']
        status = xhs.search([('xx_position', '=', 0)])
        if status:
            res.update({
                'xx_status_id': status.id
            })
        return res


class HouseType(models.Model):
    _name = 'xx.house.type'

    name = fields.Char('Huistype', required=True)
    xx_attribute_types = fields.Many2many('xx.house.attribute.type', string='Attribuut types')

    _sql_constraints = [
        ('house_type_unique', 'unique(name)', 'Huistype bestaat al!')
    ]


class QrCode(models.Model):
    _inherit = 'product.template'

    image = fields.Binary('QR code')

    @api.multi
    def generate_image(self, street, number, house_id):
        options = {'width': 500, 'height': 500}
        current_url = WEBSITE_URL + (
            street + "-" + number + "-" + str(house_id)).lower()
        ret_val = createBarcodeDrawing('QR', value=str(current_url), **options)
        image = base64.encodestring(ret_val.asString('png'))
        self.write({'image': image})


class HouseAttribute(models.Model):
    _name = 'xx.house.attribute'

    name = fields.Many2one('xx.house.attribute.type', 'Attribuut', required=True)
    xx_house = fields.Many2one('product.template', 'Huis')
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
    xx_house_type = fields.Many2many('xx.house.type', string='Huistypes')
    xx_attribute_id = fields.One2many('xx.house.attribute', 'name', string='Verkoper', required=True)


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
    xx_house = fields.Many2one('product.template', 'Huis')
    xx_exists = fields.Boolean('Aanwezig')


class HouseDocumentType(models.Model):
    _name = 'xx.house.document.type'

    name = fields.Char('Document type', required=True)


class HouseVisitors(models.Model):
    _name = 'xx.house.visitors'

    name = fields.Many2one('res.partner', 'Naam', required=True)
    xx_date = fields.Datetime('Datum', required=True)
    xx_house = fields.Many2one('product.template', 'Huis')

    @api.model
    def default_get(self, vals):
        res = super(HouseVisitors, self).default_get(vals)
        res.update({
            'xx_house': self._context.get('active_id')
        })
        return res


class HouseStatus(models.Model):
    _name = 'xx.house.status'

    name = fields.Char('Status', required=True)
    xx_position = fields.Integer('Positie', required=True)

    @api.constrains('xx_position')
    def _check_position_valid(self):
        if self.xx_position < 0:
            raise exceptions.ValidationError("Positie is niet geldig, moet positief zijn")
        else:
            pos = self.env["xx.house.status"].search([('xx_position', '=', self.xx_position)])
            if len(pos) > 1:
                raise exceptions.ValidationError("Positie bestaat al")
            else:
                small_pos = self.search([('xx_position', '=', self.xx_position - 1)])
                if len(small_pos) == 0 and self.xx_position != 0:
                    raise exceptions.ValidationError(
                        "Vooraleer deze positie gebruikt mag worden moet eerst positie %s gebruikt worden" % str(
                            self.xx_position - 1))
