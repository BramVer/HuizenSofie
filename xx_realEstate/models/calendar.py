from openerp import models, fields, api, exceptions
from datetime import datetime


class Calendar(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def create(self, vals):
        create_obj = super(Calendar, self).create(vals)
        for partner in create_obj.attendee_ids:
            partner.partner_id.write({'xx_calendar_event': [create_obj.id]})
        create_obj.get_happened()
        return create_obj

    @api.multi
    def get_date_normal(self):
        app_datetime = datetime.strptime(self.start_datetime, '%Y-%m-%d %I:%M:%S')
        new_date_string = "" + app_datetime.day + "-" + app_datetime.month + "-" + app_datetime.year
        return new_date_string

    @api.multi
    def get_time_normal(self):
        app_datetime = datetime.strptime(self.start_datetime, '%Y-%m-%d %I:%M:%S')
        new_time_string = "" + app_datetime.hour + ":" + app_datetime.minute
        return new_time_string

    @api.multi
    def get_duration_normal(self):
        app_duration = self.duration * 60
        app_hours = app_duration / 60
        app_minutes = app_duration % 60
        new_duration_string = "" + app_hours + ":" + app_minutes
        return new_duration_string

    @api.multi
    def get_happened(self):
        app_datetime = datetime.strptime(self.stop_datetime, '%Y-%m-%d %I:%M:%S')
        difference = (app_datetime - datetime.today()).days
        from openerp.pydev import pydevd
        pydevd.settrace('localhost', port=21000, stdoutToServer=True, stderrToServer=True)
        if difference < 0:
            return False
        else:
            return True
