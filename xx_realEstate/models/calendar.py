from openerp import models, fields, api, exceptions


class Calendar(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def create(self, vals):
        create_obj = super(Calendar, self).create(vals)
        for partner in create_obj.attendee_ids:
            partner.partner_id.write({'xx_calendar_event': [create_obj.id]})
        return create_obj
