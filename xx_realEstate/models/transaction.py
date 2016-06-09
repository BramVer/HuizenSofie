from openerp import models, fields, api, exceptions


class Transaction(models.Model):
    _name = 'xx.transaction'

    name = fields.Char(string="Transactie", required=True)
    xx_date = fields.Date(string="Datum", required=True)
    xx_price = fields.Integer(string="Prijs", required=True)
    xx_notaris = fields.Char(string="Notaris")

    xx_buyer_id = fields.Many2one('res.partner', string="Koper", domain=['|',('xx_type', '=', 'koper'), ('xx_type', '=', 'verkoper_koper')])
    xx_house_id = fields.Many2one('product.template', string="Woning", required=True)
    xx_transactionSeller = fields.Many2one('res.partner', string="Verkoper")

    @api.model
    def create(self, vals):
        new_transaction = super(Transaction, self).create(vals)
        new_transaction.write({'xx_transactionSeller': new_transaction.xx_house_id.xx_seller_id.id})
        env = self.env["product.template"]
        house = env.browse(vals.get('xx_house_id'))

        max_status_pos = self.env["xx.house.status"].search([('xx_position', '>', -1)], count=True) - 1
        max_status = self.env["xx.house.status"].search([('xx_position', '=', max_status_pos)])
        house.write({
            'xx_transaction_id': new_transaction.id,
            'xx_status_id': max_status.id
        })
        return new_transaction

    @api.onchange('xx_house_id')
    def _onchange_house(self):
        self.xx_transactionSeller = self.xx_house_id.xx_seller_id.id

