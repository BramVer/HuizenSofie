import openerp
import werkzeug

from openerp.addons.base.ir.ir_qweb import AssetsBundle
from openerp.addons.web.controllers.main import WebClient, Binary
from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import table_compute

PPG = 8  # Products Per Page
PPR = 4  # Products Per Row


class website_houses(openerp.addons.website_sale.controllers.main.website_sale):
    @http.route()
    def shop(self, page=0, ppg=False, house_type=False, gemeente=False, min_price=False, max_price=False, slaapkamers=False, soort_bebouwing=False, tuin=False, terras=False, garage=False, zwembad=False, lift=False, **post):

        old_sold = super(website_houses, self).shop(page=page, ppg=PPG, post=post)
        old_qcontext = old_sold.qcontext

        product_obj = http.request.env["product.template"]
        attribute_obj = http.request.env["xx.house.attribute"]

        filtered_products_list = product_obj.search([])
        if house_type:
            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('xx_house_type', '=', house_type)])
            post["house_type"] = house_type
        if gemeente:
            gemeente_string = gemeente
            post["gemeente"] = gemeente
            gem = "Ditisgeenechtegemeente"
            zip = ""

            words = gemeente_string.split()

            for word in words:
                if product_obj.search([('xx_city', 'ilike', word)]):
                    gem = word
                else:
                    if product_obj.search([('xx_zip', '=ilike', word)]):
                        zip = word

            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), '|', ('xx_zip', '=ilike', zip), ('xx_city', 'ilike', gem)])


        if min_price:
            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('xx_current_price', '>=', min_price)])
            post["min_price"] = min_price

        if max_price:
            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('xx_current_price', '<=', max_price)])
            post["max_price"] = max_price

        if slaapkamers:
            if slaapkamers == "4":
                attribute_list = attribute_obj.search([('name', 'ilike', "slaapkamer"), ('xx_value', '>=', 5 )])
            else:
                attribute_list = attribute_obj.search([('name', 'ilike', "slaapkamer"), ('xx_value', '=', int(slaapkamers)+1)])

            house_id_set = set()
            for attr in attribute_list:
                house_id_set.add(attr.xx_house.id)
            house_id_list = list(house_id_set)
            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('id', 'in', house_id_list)])
            post["slaapkamers"] = slaapkamers

        if soort_bebouwing:
            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('xx_building_type', '=', soort_bebouwing)])
            post["soort_bebouwing"]= soort_bebouwing

        if tuin:
            attribute_list = attribute_obj.search([('name', 'ilike', tuin), '!', ('xx_value', 'ilike', 'nee')])
            house_id_set = set()
            for attr in attribute_list:
                house_id_set.add(attr.xx_house.id)
            house_id_list = list(house_id_set)

            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('id', 'in', house_id_list)])

            post["tuin"] = tuin

        if terras:
            attribute_list = attribute_obj.search([('name', 'ilike', terras), '!', ('xx_value', 'ilike', 'nee')])
            house_id_set = set()
            for attr in attribute_list:
                house_id_set.add(attr.xx_house.id)
            house_id_list = list(house_id_set)

            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('id', 'in', house_id_list)])

            post["terras"] = terras

        if garage:
            attribute_list = attribute_obj.search([('name', 'ilike', garage), '!', ('xx_value', 'ilike', 'nee')])
            house_id_set = set()
            for attr in attribute_list:
                house_id_set.add(attr.xx_house.id)
            house_id_list = list(house_id_set)

            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('id', 'in', house_id_list)])

            post["garage"] = garage

        if zwembad:
            attribute_list = attribute_obj.search([('name', 'ilike', zwembad), '!', ('xx_value', 'ilike', 'nee')])
            house_id_set = set()
            for attr in attribute_list:
                house_id_set.add(attr.xx_house.id)
            house_id_list = list(house_id_set)

            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('id', 'in', house_id_list)])

            post["zwembad"] = zwembad

        if lift:
            attribute_list = attribute_obj.search([('name', 'ilike', lift), '!', ('xx_value', 'ilike', 'nee')])
            house_id_set = set()
            for attr in attribute_list:
                house_id_set.add(attr.xx_house.id)
            house_id_list = list(house_id_set)

            filtered_products_list = product_obj.search(
                [('id', 'in', filtered_products_list._ids), ('id', 'in', house_id_list)])

            post["lift"] = lift


        new_product_count = len(filtered_products_list._ids)
        pager = request.website.pager(url="/shop", total=new_product_count, page=page, step=PPG, scope=7, url_args=post)
        new_product_ids = product_obj.search([('id', 'in', filtered_products_list._ids)], limit=PPG,
                                             offset=pager['offset'],
                                             order='website_published desc, website_sequence desc')
        house_type = []
        for h_type in http.request.env['xx.house.type'].search([]):
            house_type.append(h_type.name)

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
            'house_types': house_type
        }
        return request.website.render("website_sale.products", values)


class website_welcome(openerp.addons.website.controllers.main.Website):

    @http.route()
    def index(self, email=False, **kw):
        if email:
            ebook_obj = http.request.env["xx.ebook"]
            ebook_obj.create_from_website(email)
        return super(website_welcome, self).index()


