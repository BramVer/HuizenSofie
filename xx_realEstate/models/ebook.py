from openerp import models, fields, api, exceptions
import datetime

class Ebook_email(models.Model):
    _name = 'xx.ebook'

    name = fields.Char(string="E-mailaddres", required=True)
    xx_previous_date = fields.Date(string="Laatste verzenddatum")

    @api.multi
    def send_single_ebook(self):
        self.xx_previous_date = datetime.datetime.today().strftime('%Y-%m-%d')
        # Call mail function


    @api.constrains('name')
    def _check_unique_email(self):
        ebook = self.search([('name', '=ilike', self.name)])
        if len(ebook) != 1:
            raise exceptions.ValidationError('Email reeds in gebruik')

    @api.model
    def create(self, vals):
        new_transaction = super(Ebook_email, self).create(vals)
        return new_transaction

    @api.multi
    def create_from_website(self, name):
        self.sudo().create(
            {
                "name": name,
                "xx_previous_date": False
            })


