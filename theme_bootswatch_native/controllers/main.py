import openerp
import werkzeug

from openerp.addons.base.ir.ir_qweb import AssetsBundle
from openerp.addons.web.controllers.main import WebClient, Binary
from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import table_compute


PPG = 20 # Products Per Page
PPR = 4  # Products Per Row

class website_houses(openerp.addons.website_sale.controllers.main.website_sale):

    @http.route()
    def shop(self, page=0, ppg=False, searched = False, soort = False, gemeente = False, prijs = False):


        old_sold = super(website_houses, self).shop(page=page, ppg=PPG)
        old_qcontext = old_sold.qcontext

        product_obj = http.request.env["product.template"]
        status_obj = http.request.env["xx.house.status"]
        test = status_obj.search([])

        if(searched):
            filtered_products_list = product_obj.search([])
            if (soort):
                soorten = request.httprequest.form.getlist('soort')
                for sort in soorten:
                    filtered_products_list = product_obj.search([('id', 'in', filtered_products_list._ids), ('xx_house_type', '=', sort)])
            if (gemeente):
                gemeentes = request.httprequest.form.getlist('gemeente')
            if (prijs):
                prijzen = request.httprequest.form.get('prijs')



            new_product_count = len(filtered_products_list._ids)
            pager = request.website.pager(url="/shop", total=new_product_count, page=page, step=PPG, scope=7)
            new_product_ids = product_obj.search([('id', 'in', filtered_products_list._ids)],limit=PPG, offset=pager['offset'], order='website_published desc, website_sequence desc')


            values = {
                'search': old_qcontext.get('search'),
                'category': old_qcontext.get('category'),
                'attrib_values': old_qcontext.get('attrib_values'),
                'attrib_set': old_qcontext.get('attrib_set'),
                'pager': pager,
                'pricelist': old_qcontext.get('pricelist'),
                'products': new_product_ids,
                'bins': table_compute().process(new_product_ids, PPG),
                'rows': PPR,
                'styles': old_qcontext.get('styles'),
                'categories': old_qcontext.get('categs'),
                'attributes': old_qcontext.get('attributes'),
                'compute_currency': old_qcontext.get('compute_currency'),
                'keep': old_qcontext.get('keep'),
                'parent_category_ids': old_qcontext.get('parent_category_ids'),
                'style_in_product': lambda style, product: style.id in [s.id for s in product.website_style_ids],
                'attrib_encode': lambda attribs: werkzeug.url_encode([('attrib', i) for i in attribs]),
            }

            return request.website.render("website_sale.products", values)



        return old_sold


