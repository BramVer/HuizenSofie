from openerp import models, fields, api, exceptions


class House(models.Model):
    _inherit = 'product.template'

    xx_house_type = fields.Many2one('xx.house.type', 'House type')
    name = fields.Char(compute='_get_name', store=True, default='', string='Address')
    xx_street = fields.Char('Street name', required=True)
    xx_street_number = fields.Char('Street number', required=True)
    xx_city = fields.Char('City', required=True)
    xx_zip = fields.Char('Zip code', required=True)
    xx_provence = fields.Char('Provence', required=True)
    xx_starting_price = fields.Float('Starting price', required=True)
    xx_current_price = fields.Float('Current price')
    xx_total_area = fields.Float('Total surface', required=True)
    xx_living_area = fields.Float('Total living area', required=True)
    xx_energy = fields.Float('Energy', required=True)
    xx_unique_epc = fields.Float('EPC code', required=True)

    xx_seller_id = fields.Many2one('res.partner', string='Verkoper', required=True)


    @api.depends('xx_street', 'xx_street_number')
    def _get_name(self):
        if self.xx_street and self.xx_street_number:
            self.name = self.xx_street + ' ' + self.xx_street_number


class HouseType(models.Model):
    _name = 'xx.house.type'

    name = fields.Char('House type', required=True)
