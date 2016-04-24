

from openerp import models, fields, api, exceptions

class User(models.Model):
    _name = 'xx.partner.user'
    _inherit = 'res.partner'

    name = fields.Char(compute = "_createName", store=True, default="")
    xx_lastName = fields.Char(string="Achternaam", required=True)
    xx_firstName = fields.Char(string="Voornaam", required=True)
    xx_street = fields.Char(string="Straat")
    xx_houseNumber = fields.Integer(string="Huisnummer")
    xx_city = fields.Char(string="Gemeente")
    xx_areaCode = fields.Char(string="Postcode")
    xx_telephone = fields.Char(string="Telefoonnummer")
    xx_cellphone = fields.Char(string="GSM-nummer")
    #wachtwoord
    xx_email = fields.Char(string="E-mailadres", required=True)
    xx_supplier = fields.Boolean(string="Is verkoper")

    xx_buyTransaction_ids = fields.One2many('xx.transaction','xx_buyer_id', string='Houses bought')

    @api.depends('xx_firstName', 'xx_lastName')
    def _createName(self):
        self.name = self.xx_lastName + ' ' + self.xx_firstName

    @api.constrains('telephone','cellphone')
    def _check_telephone_or_cellphone_empty(self):
        for r in self:
            if not r.telephone and not r.cellphone:
                raise exceptions.ValidationError("Telefoon of gsm nummer moet ingevuld zijn")