from odoo import http
from odoo.http import request, Response
import json


class ApiController(http.Controller):

    @http.route('/api/v1/get_data', auth='public', type='http', methods=['GET'], cors='*')
    def get_data(self, **kw):
        # recevoir la liste des dossiers en cours de traitement en filtrant les 2 premieres etapes
        dossier_ids = request.env['wk.workflow.ponctuel'].sudo().search(
            [('state', 'not in', ['1', '2', '11'])]
        )
        data = []
        for dossier in dossier_ids:
            data.append({
                'id': dossier.id,
                'name': dossier.name,
                'client': dossier.nom_client.name if dossier.nom_client else '',
                'agence': dossier.branche.ref if dossier.branche else ''
            })
        return Response(json.dumps({'data': data}), status=200, headers={'Content-Type': 'application/json'})

    @http.route('/api/v1/get_dossier', auth='public', type='json', methods=['POST'], cors='*')
    def get_dossier(self, **kw):
        request_body = request.httprequest.data.decode('utf-8')
        data = json.loads(request_body)
        dossier_id = data.get('dossier_id')

        if not dossier_id:
            return Response(json.dumps({'error': 'Dossier ID not provided'}), status=400, headers={'Content-Type': 'application/json'})

        dossier = request.env['wk.workflow.ponctuel'].sudo().browse(dossier_id)

        if not dossier.exists():
            return Response(json.dumps({'error': 'Dossier not found'}), status=404, headers={'Content-Type': 'application/json'})

        dossier_data = {
            'capital': dossier.nom_client.chiffre_affaire if dossier.nom_client else '',
            'num_compte': dossier.num_compte or '',
            'num_registre_commerce': dossier.num_registre_commerce or '',
            'demande': dossier.demande.name if dossier.demande else '',
            'explanation': dossier.explanation or '',
            'avis_conseil': dossier.avis_conseil or '',
            'recommendation_agence': dossier.recommendation_agence or '',
            'recommendation_1': dossier.recommendation_1 or '',
            'recommendation_2': dossier.recommendation_2 or '',
            'recommendation_3': dossier.recommendation_3 or '',
            'recommendation_4': dossier.recommendation_4 or '',
            'recommendation_5': dossier.recommendation_5 or '',
            'recommendation_6': dossier.recommendation_6 or '',
            'recommendation_7': dossier.recommendation_7 or '',
            'recommendation_8': dossier.recommendation_8 or '',
            'recommendation_9': dossier.recommendation_9 or '',
            'recommendation_10': dossier.recommendation_10 or '',
        }
        return Response(json.dumps({'data': dossier_data}), status=200, headers={'Content-Type': 'application/json'})
