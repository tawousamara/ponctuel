from odoo import http
from odoo.http import request, Response
import json


class ApiController(http.Controller):

    @http.route('/api/contacts', auth='public', methods=['GET'], type='json')
    def get_contacts(self):
        # Récupérer tous les contacts
        contacts = request.env['res.partner'].sudo().search([])
        # Préparer les données à retourner
        contact_data = [{
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
        } for contact in contacts]
        return contact_data

    @http.route('/api/v1/get_data', auth='none', type='http', methods=['GET'], cors='*')
    def get_data(self, **kw):
        print('tested')
        #return Response(json.dumps({'data': 'data', }), status=200 , headers={'Content-Type': 'application/json'})
        return json.dumps({'data': 'data', })
    @http.route('/api/v1/post_data', auth='none', type='http', methods=['POST'], cors='*')
    def post_data(self, **kw):
        request_body = request.httprequest.data.decode('utf-8')
        data = json.loads(request_body)
        user_id = data.get('user_id')
        # do somthing ....
        return Response(json.dumps({'data': 'data', }), status=200 ,headers={'Content-Type': 'application/json'})