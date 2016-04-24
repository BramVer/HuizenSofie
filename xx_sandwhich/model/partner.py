

from openerp.osv import osv,fields

class partner(osv.osv):
     _inherit = 'res.partner'

     _columns={
         'xx_sandwich': fields.char(string = "Broodje",required=True),
         'xx_saus': fields.char(string = "Saus", required = True)
     }