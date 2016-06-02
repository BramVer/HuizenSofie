import re
from urlparse import urljoin
import werkzeug
from openerp import models, fields, api, exceptions


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
    xx_want_ebook = fields.Boolean('Wilt E-Book')
    # wachtwoord

    email = fields.Char(string="E-mailadres", required=True)
    xx_type = fields.Selection(
        [('verkoper', 'Verkoper'), ('koper', 'Koper'), ('verkoper_koper', 'Verkoper/Koper'), ('bezoeker', 'Bezoeker')],
        string='Type', required=True)

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

    @api.onchange('xx_want_ebook')
    def _onchange_ebook(self):
        if self.xx_want_ebook:
            email = self.env["xx.ebook"].search([('name', '=', self.email)])
            if len(email)==0:
                vals = {
                    'name' : self.email
                }
                ebook_mail = self.env["xx.ebook"].create(vals)
        else:
            email = self.env["xx.ebook"].search([('name', '=', self.email)])
            if len(email)==1:
                self.env["xx.ebook"].browse(email.id).unlink()

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
    def setup_user(self):
        self.create_user()
        self.send_email()

    @api.multi
    def action_apply(self):
        user_id = self._create_user()
        self.write({'user_id': user_id})
        self._send_email()

    @api.multi
    def _create_user(self):
        values = {
            'email': self.email,
            'login': self.email,
            'partner_id': self.id,
            'groups_id': [(6, 0, [])]
        }
        self._context.update = dict(self._context or {}, noshortcut=True, no_reset_password=True)
        user = self.env['res.users'].create(values)
        return user.id

    @api.multi
    def _send_email(self):
        # TODO check email signup
        user = self.user_id
        context = dict({}, lang=user.lang)
        ctx_portal_url = dict(context, signup_force_type_in_url='')
        portal_url = self._get_signup_url_for_action([user.partner_id], context=ctx_portal_url)[
            user.partner_id.id]
        self.signup_prepare([user.partner_id.id], context=context)
        context.update({'dbname': self._cr.dbname, 'portal_url': portal_url})
        template_id = self.env['ir.model.data'].xmlid_to_res_id('portal.mail_template_data_portal_welcome')
        for partner in self:
            if template_id:
                self.pool['mail.template'].send_mail(self._cr, self._uid, template_id, partner.id, force_send=True,
                                                     context=context)

    @api.v7
    def _get_signup_url_for_action(self, cr, uid, ids, action=None, view_type=None, menu_id=None, res_id=None,
                                   model=None, context=None):
        if context is None:
            context = {}
        res = dict.fromkeys(ids, False)
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
        for partner in self.browse(cr, uid, ids, context):
            if context.get('signup_valid') and not partner.user_ids:
                self.signup_prepare(cr, uid, [partner.id], context=context)
            route = 'login'
            query = dict(db=cr.dbname)
            signup_type = context.get('signup_force_type_in_url', partner.signup_type or '')
            if signup_type:
                route = 'reset_password' if signup_type == 'reset' else signup_type
            if partner.signup_token and signup_type:
                query['token'] = partner.signup_token
            elif partner.user_ids:
                query['login'] = partner.user_ids[0].login
            else:
                continue

            fragment = dict()
            base = '/web#'
            if action == '/mail/view':
                base = '/mail/view?'
            elif action:
                fragment['action'] = action
            if view_type:
                fragment['view_type'] = view_type
            if menu_id:
                fragment['menu_id'] = menu_id
            if model:
                fragment['model'] = model
            if res_id:
                fragment['res_id'] = res_id
            if fragment:
                query['redirect'] = base + werkzeug.url_encode(fragment)

            url = urljoin(base_url, "/web/%s?%s" % (route, werkzeug.url_encode(query)))
            if '[1]' in url:
                url = url.replace('[1]', 'signup')
            res[partner.id] = url
        return res
