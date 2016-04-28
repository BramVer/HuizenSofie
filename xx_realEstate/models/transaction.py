from openerp import models, fields, api, exceptions

class Transaction(models.Model):
    _name = 'xx.transaction'

    name = fields.Char(string="Transactie", required=True)
    xx_date = fields.Date(string="Datum", required=True)
    xx_price = fields.Integer(string="Prijs", required=True)
    xx_notaris = fields.Char(string="Notaris")

    xx_buyer_id = fields.Many2one('res.partner', string="Koper", required=True)
    xx_house_id = fields.Many2one('product.template', string ="Woning", required=True)
    xx_transactionSeller_id = fields.Char(string='Verkoper')

    @api.onchange('xx_house_id')
    def _onchange_house(self):
        current_seller_obj = self.xx_house_id.xx_seller_id
        self.xx_transactionSeller_id = current_seller_obj.xx_firstName + ' ' + current_seller_obj.xx_lastName
