from openerp import models, fields, api, exceptions
import re
from random import randint


class User(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    name = fields.Char(string="Naam", required=True, default='')
    xx_street = fields.Char(string="Straat")
    xx_houseNumber = fields.Integer(string="Huisnummer")
    xx_city = fields.Many2one('xx.city', 'Gemeente')
    xx_zip = fields.Char('Postcode')
    xx_telephone = fields.Char(string="Telefoonnummer")
    xx_cellphone = fields.Char(string="GSM-nummer")
    xx_has_login = fields.Boolean('Heeft login')
    # wachtwoord
    email = fields.Char(string="E-mailadres", required=True)
    xx_type = fields.Selection([('verkoper', 'Verkoper'), ('koper', 'Koper'), ('verkoper_koper', 'Verkoper/Koper'), ('bezoeker', 'Bezoeker')], string='Type', required=True)

    xx_buyTransaction_ids = fields.One2many('xx.transaction', 'xx_buyer_id', string='Huizen gekocht')

    xx_housesOnSale_ids = fields.One2many('product.template', 'xx_seller_id', string='Huizen te koop')
    xx_visitor_ids = fields.One2many('xx.house.visitors', 'name', string="Huizen bezichtigd")






    # Replace attributes to avoid error
    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
                                                  string="Account Payable", oldname="property_account_payable",
                                                  domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
                                                  help="This account will be used instead of the default one as the payable account for the current partner",
                                                  required=False)
    property_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
                                                     string="Account Receivable", oldname="property_account_receivable",
                                                     domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]",
                                                     help="This account will be used instead of the default one as the receivable account for the current partner",
                                                     required=False)

    @api.onchange('xx_city')
    def _onchange_city(self):
        if self.xx_city:
            self.xx_zip = self.xx_city.xx_zip

    @api.constrains('xx_telephone', 'xx_cellphone')
    def _check_telephone_or_cellphone_empty(self):
        if not self.xx_telephone and not self.xx_cellphone:
            raise exceptions.ValidationError("Telefoon of gsm nummer moet ingevuld zijn")

    @api.constrains('email')
    def _check_email_valid(self):
        if not re.match("[^@]+@[^@]+\.[^@]+", self.email):
            raise exceptions.ValidationError("Email is niet geldig")

    @api.onchange('email')
    def _check_unique_email(self):
        user = self.search([('email', '=', self.email)])
        if len(user) != 0:
            raise exceptions.ValidationError('Email reeds in gebruik bij %s' % user[0].name)

    @api.multi
    def create_user(self):
        from openerp.pydev import pydevd
        pydevd.settrace('localhost', port=22000, stdoutToServer=True, stderrToServer=True)

        username = self._get_username(str(self.name).replace(" ", "").lower())

        vals = {
            'name': username,
            'login': self.email
        }
        self.env['res.users'].create(vals)

    @api.model
    def _get_username(self, username):
        from openerp.pydev import pydevd
        pydevd.settrace('localhost', port=22000, stdoutToServer=True, stderrToServer=True)

        returning_username = username
        if len(self.env['res.users'].search([('name', '=', username)])) != 0:
            returning_username += str(randint(1, 9))
            self._username_taken(returning_username)
        return returning_username
