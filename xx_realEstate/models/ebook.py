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


    @api.onchange('name')
    def _check_unique_email(self):
        ebook = self.search([('name', '=', self.name)])
        if len(ebook) != 0:
            raise exceptions.ValidationError('Email reeds in gebruik')
