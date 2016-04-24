

from openerp import models, fields, api, exceptions

class User(models.Model):
    _name = 'xx.partner.user'
    _inherit = 'res.partner'

    name = fields.Char(string="Naam", required=True)
    firstName = fields.Char(string="Voornaam", required=True)
    street = fields.Char(string="Straat")
    houseNumber = fields.Integer(string="Huisnummer")
    city = fields.Char(string="Gemeente")
    areaCode = fields.Char(string="Postcode")
    telephone = fields.Char(string="Telefoonnummer")
    cellphone = fields.Char(string="GSM-nummer")
    #wachtwoord
    email = fields.Char(string="E-mailadres", required=True)
    supplier = fields.Boolean(string="Is verkoper")


    @api.constrains('telephone','cellphone')
    def _check_telephone_or_cellphone_empty(self):
        for r in self:
            if not r.telephone and not r.cellphone:
                raise exceptions.ValidationError("Telefoon of gsm nummer moet ingevuld zijn")