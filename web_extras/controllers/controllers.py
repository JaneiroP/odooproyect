from odoo import http
from odoo.addons.web.controllers import main


class DataSet(http.Controller):
    @http.route('/web/dataset/search_read', type='json', auth="user")
    def search_read(self, model, fields=False, offset=0, limit=False, domain=None, sort=None):
        if model == 'product.template' or model == 'product.product':
            if domain is not None:
                for x in domain:
                    if "name" in x:
                        arrayname = x
                        if len(arrayname[2]) <= 10:
                            arrayname[2] = (arrayname[2].upper()).replace('R', '%R%')
                            for i in range(len(domain)):
                                if domain[i] == x:
                                    domain[i] = arrayname

        return self.do_search_read(model, fields, offset, limit, domain, sort)


main.DataSet.search_read = DataSet.search_read