from openerp import models, fields, api, exceptions
from datetime import datetime


class Calendar(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def create(self, vals):
        create_obj = super(Calendar, self).create(vals)
        for partner in create_obj.attendee_ids:
            partner.partner_id.write({'xx_calendar_event': [create_obj.id]})
        return create_obj

    @api.multi
    def get_date_normal(self):
        if self.start_datetime:
            app_datetime = datetime.strptime(self.start_datetime, '%Y-%m-%d %H:%M:%S')
        else:
            app_datetime = datetime.strptime(self.start_date, '%Y-%m-%d')
        new_date_string = "{0}-{1}-{2}".format(app_datetime.day, app_datetime.month, app_datetime.year)
        return new_date_string

    @api.multi
    def get_time_normal(self):
        if self.start_datetime:
            app_datetime = datetime.strptime(self.start_datetime, '%Y-%m-%d %H:%M:%S')
        else:
            app_datetime = datetime.strptime(self.start_date, '%Y-%m-%d')
        new_time_string = "{0}:{1}".format(app_datetime.hour, app_datetime.minute)
        return new_time_string

    @api.multi
    def get_duration_normal(self):
        app_duration = self.duration * 60

        app_hours = int(app_duration / 60)
        app_minutes = int(app_duration % 60)

        app_hours = str(app_hours).zfill(2)
        app_minutes = str(app_minutes).zfill(2)
        #new_result = "{0}:{1}".format(app_hours, app_minutes)
        new_result = "" + app_hours + ":" + app_minutes
        return new_result

    @api.multi
    def get_happened(self):
        if self.stop_datetime:
            app_datetime = datetime.strptime(self.stop_datetime, '%Y-%m-%d %H:%M:%S')
<<<<<<< HEAD
            difference = (app_datetime - datetime.today()).days
=======
        else:
            app_datetime = datetime.strptime(self.stop_date, '%Y-%m-%d')
        difference = (app_datetime - datetime.today()).days
>>>>>>> d4c8e6c7752ac9e50627581ec29723de36c98e6e
        if difference < 0:
            return True
        else:
            return False
