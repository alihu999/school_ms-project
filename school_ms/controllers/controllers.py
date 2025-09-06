# -*- coding: utf-8 -*-
# from odoo import http


# class SchoolMs(http.Controller):
#     @http.route('/school_ms/school_ms', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_ms/school_ms/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_ms.listing', {
#             'root': '/school_ms/school_ms',
#             'objects': http.request.env['school_ms.school_ms'].search([]),
#         })

#     @http.route('/school_ms/school_ms/objects/<model("school_ms.school_ms"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_ms.object', {
#             'object': obj
#         })

