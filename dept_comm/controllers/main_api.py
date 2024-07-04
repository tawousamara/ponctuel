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
        #recevoir la liste des dossiers en cours de traitement en filtrant les 2 premieres etapes
        dossier_ids = request.env['wk.workflow.ponctuel'].search([('state', 'not in', ['1', '2', '11'])])
        data = []
        for dossier in dossier_ids:
            data.append({
                'id': dossier.id,
                'name': dossier.name,
                'client': dossier.nom_client.name,
                'agence': dossier.branche.ref
            })
        return Response(json.dumps({'data': data}), status=200 , headers={'Content-Type': 'application/json'})

    @http.route('/api/v1/get_dossier', auth='none', type='http', methods=['GET'], cors='*')
    def get_dossier(self, dossier_id):
        #information general a recevoir

        dossier = request.env['wk.workflow.ponctuel'].browse(dossier_id)
        data = {
            'capital': dossier.nom_client.chiffre_affaire,
            'num_compte': dossier.num_compte,
            'num_registre_commerce': dossier.num_registre_commerce,
            'demande': dossier.demande.name,
            'explanation': dossier.explanation,
            'avis_conseil': dossier.avis_conseil,
            'recommendation_agence': dossier.recommendation_agence,
            'recommendation_1': dossier.recommendation_1,
            'recommendation_2': dossier.recommendation_2,
            'recommendation_3': dossier.recommendation_3,
            'recommendation_4': dossier.recommendation_4,
            'recommendation_5': dossier.recommendation_5,
            'recommendation_6': dossier.recommendation_6,
            'recommendation_7': dossier.recommendation_7,
            'recommendation_8': dossier.recommendation_8,
            'recommendation_9': dossier.recommendation_9,
            'recommendation_10': dossier.recommendation_10,
        }
        return Response(json.dumps({'data': data, }), status=200 , headers={'Content-Type': 'application/json'})

    @http.route('/api/v1/post_dossier', auth='none', type='http', methods=['POST'], cors='*')
    def post_dossier(self, dossier_id,avis):
        #information general a recevoir
        dossier = request.env['wk.workflow.ponctuel'].browse(dossier_id)
        data = {}
        if dossier.state == "3":
            data = {
                'recommendation_2': avis,
            }
        elif dossier.state == "4":
            data = {
                'recommendation_3': avis,
            }
        elif dossier.state == "5":
            data = {
                'recommendation_4': avis,
            }
        elif dossier.state == "6":
            data = {
                'recommendation_5': avis,
            }
        elif dossier.state == "7":
            data = {
                'recommendation_6': avis,
            }
        elif dossier.state == "8":
            data = {
                'recommendation_7': avis,
            }
        new_state = str(int(dossier.state) + 1)
        data['state'] = new_state
        dossier.write(data)
        return Response(json.dumps({'data': data, }), status=200 , headers={'Content-Type': 'application/json'})



    @http.route('/api/v1/post_data', auth='none', type='http', methods=['POST'], cors='*')
    def post_data(self, **kw):
        request_body = request.httprequest.data.decode('utf-8')
        data = json.loads(request_body)
        user_id = data.get('user_id')
        # do somthing ....
        return Response(json.dumps({'data': 'data', }), status=200, headers={'Content-Type': 'application/json'})