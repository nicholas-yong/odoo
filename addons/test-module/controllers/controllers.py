# -*- coding: utf-8 -*-
# from odoo import http


# class Test-module(http.Controller):
#     @http.route('/test-module/test-module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test-module/test-module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test-module.listing', {
#             'root': '/test-module/test-module',
#             'objects': http.request.env['test-module.test-module'].search([]),
#         })

#     @http.route('/test-module/test-module/objects/<model("test-module.test-module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test-module.object', {
#             'object': obj
#         })
