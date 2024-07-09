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

    @http.route('/api/v1/get_tables', auth='public', type='json', methods=['POST'], cors='*')
    def get_tables(self, **kw):
        request_body = request.httprequest.data.decode('utf-8')
        data = json.loads(request_body)
        dossier_id = data.get('dossier_id')

        if not dossier_id:
            return Response(json.dumps({'error': 'Dossier ID not provided'}), status=400, headers={'Content-Type': 'application/json'})

        dossier = request.env['wk.workflow.ponctuel'].sudo().browse(dossier_id)

        if not dossier.exists():
            return Response(json.dumps({'error': 'Dossier not found'}), status=404, headers={'Content-Type': 'application/json'})
        if not dossier.states:
            return Response(json.dumps({'error': 'No steps found'}), status=404,
                            headers={'Content-Type': 'application/json'})
        step1 = dossier.states.filtered(lambda l:l.sequence == 1)
        '''الفرع'''
        #تفاصيل التسهيلات الممنوحة (KDA)
        facilite_accorde_data = []
        for item in step1.facilite_accorde:
            demande_ids = ''
            if len(item.type_demande_ids) != 1:
                for line in item.type_demande_ids:
                    demande_ids += line.name + ' / '
            else:
                for line in item.type_demande_ids:
                    demande_ids += line.name
            element = {
                'type_demande_ids': demande_ids,
                'date': item.date,
                'montant_da_actuel': item.montant_da_actuel,
                'montant_da_demande': item.montant_da_demande,
                'montant_da_total': item.montant_da_total,
                'garantie_montant': item.garantie_montant,
                'remarques': item.remarques
            }
            facilite_accorde_data.append(element)

        #توزيع راس مال الشركة
        apropos_data = []
        for item in step1.apropos:
            element = {
                'nom_partenaire': item.nom_partenaire,
                'age': item.age,
                'statut_partenaire': item.statut_partenaire,
                'nationalite': item.nationalite.name,
                'pourcentage': item.pourcentage,
            }
            apropos_data.append(element)

        # اعرف عميلك KYC
        kyc_data = []
        for item in step1.kyc:
            answer = ''
            if item.answer == 'oui':
                answer = 'نعم'
            elif item.answer == 'non':
                answer = 'لا'
            element = {
                'info': item.info,
                'answer': answer,
                'detail': item.detail,
            }
            kyc_data.append(element)

        # فريق التسيير
        gestion_data = []
        for item in step1.gestion:
            element = {
                'name': item.name,
                'job': item.job,
                'niveau_etude': item.niveau_etude,
                'age': item.age,
                'experience': item.experience
            }
            gestion_data.append(element)

        # الوضعية المالية لدى الغير
        situations_data = []
        for item in step1.situations:
            element = {
                'banque': item.banque.name,
                'type_fin': item.type_fin.name,
                'montant': item.montant,
                'encours': item.encours,
                'garanties': item.garanties
            }
            situations_data.append(element)

        # الموردون
        fournisseur_data = []
        for item in step1.fournisseur:
            type_payment = ''
            if len(item.type_payment) != 1:
                for line in item.type_payment:
                    type_payment += line.name + ' / '
            elif len(item.type_payment) == 1:
                for line in item.type_payment:
                    type_payment = line.name
            element = {
                'name': item.name,
                'country': item.country.name,
                'type_payment': type_payment
            }
            fournisseur_data.append(element)

        # الزبائن
        client_data = []
        for item in step1.client:
            type_payment = ''
            if len(item.type_payment) != 1:
                for line in item.type_payment:
                    type_payment += line.name + ' / '
            elif len(item.type_payment) == 1:
                for line in item.type_payment:
                    type_payment = line.name
            element = {
                'name': item.name,
                'country': item.country.name,
                'type_payment': type_payment
            }
            client_data.append(element)

        step2 = dossier.states.filtered(lambda l:l.sequence == 2)
        '''مديرية الاعمال التجارية'''

        # تفاصيل الضمانات
        # الضمانات العقارية الحالية
        detail_garantie_actuel_ids_data = []
        for item in step2.detail_garantie_actuel_ids:
            niveau = ''
            if item.niveau == '3':
                niveau = 'منخفض'
            elif item.niveau == '2':
                niveau = 'متوسط'
            elif item.niveau == '1':
                niveau = 'عالي'
            element = {
                'type_garantie': item.type_garantie.name,
                'type_contrat': item.type_contrat.name,
                'montant': item.montant,
                'date': item.date,
                'recouvrement': item.recouvrement,
                'niveau': niveau,
            }
            detail_garantie_actuel_ids_data.append(element)

        # الضمانات العقارية المقترحة
        detail_garantie_propose_ids_data = []
        for item in step2.detail_garantie_propose_ids:
            niveau = ''
            if item.niveau == '3':
                niveau = 'منخفض'
            elif item.niveau == '2':
                niveau = 'متوسط'
            elif item.niveau == '1':
                niveau = 'عالي'
            element = {
                'type_garantie': item.type_garantie.name,
                'type_contrat': item.type_contrat.name,
                'montant': item.montant,
                'date': item.date,
                'recouvrement': item.recouvrement,
                'niveau': niveau,
            }
            detail_garantie_propose_ids_data.append(element)

        # الشروط السابقة/المقترحة و الموافق عليها من لجان التمويل
        garantie_conf_data = []
        for item in step2.garantie_conf:
            answer = ''
            if item.answer == 'oui':
                answer = 'نعم'
            elif item.answer == 'non':
                answer = 'لا'
            element = {
                'info': item.info,
                'answer': answer,
                'detail': item.detail,
            }
            garantie_conf_data.append(element)

        # الشروط المالية
        garantie_fin_data = []
        for item in step2.garantie_fin:
            answer = ''
            if item.answer == 'oui':
                answer = 'نعم'
            elif item.answer == 'non':
                answer = 'لا'
            element = {
                'info': item.info,
                'answer': answer,
                'detail': item.detail,
            }
            garantie_fin_data.append(element)
        # الشروط المالية
        garantie_autres_data = []
        for item in step2.garantie_autres:
            answer = ''
            if item.answer == 'oui':
                answer = 'نعم'
            elif item.answer == 'non':
                answer = 'لا'
            element = {
                'info': item.info,
                'answer': answer,
                'detail': item.detail,
            }
            garantie_autres_data.append(element)

        # مركزية المخاطر
        risque_central_data = []
        for item in step2.risque_central:
            element = {
                'declaration': item.declaration,
                'montant_esalam_dz_donne': item.montant_esalam_dz_donne,
                'montant_esalam_dz_used': item.montant_esalam_dz_used,
                'montant_other_dz_donne': item.montant_other_dz_donne,
                'montant_other_dz_used': item.montant_other_dz_used,
                'montant_total_dz_donne': item.montant_total_dz_donne,
                'montant_total_dz_used': item.montant_total_dz_used,
            }
            risque_central_data.append(element)

        # التسهيلات القائمة مع المصرف
        facitlite_existante_data = []
        for item in step2.facitlite_existante:
            demande_ids = ''
            if len(item.type_demande_ids) != 1:
                for line in item.type_demande_ids:
                    demande_ids += line.name + ' / '
            else:
                for line in item.type_demande_ids:
                    demande_ids += line.name
            element = {
                'company': item.company,
                'facilite': item.facilite.name,
                'type_demande_ids': demande_ids,
                'brut_da': item.brut_da,
                'net_da': item.net_da,
                'montant_total_dz_donne': item.montant_total_dz_donne,
                'montant_total_dz_used': item.montant_total_dz_used,
            }
            facitlite_existante_data.append(element)

        dossier_data = {
            #Champs bruts
            'classification': step1.classification.name if step1.classification else '',
            'adress_siege': step1.adress_siege if step1.adress_siege else '',
            'nif': step1.nif if step1.nif else '',
            'num_registre_commerce': step1.num_registre_commerce if step1.num_registre_commerce else '',
            'date_ouverture_compte': step1.date_ouverture_compte if step1.date_ouverture_compte else '',
            'date_inscription': step1.date_inscription if step1.date_inscription else '',
            'date_debut_activite': step1.date_debut_activite if step1.date_debut_activite else '',
            'activite': step1.activite.name if step1.activite else '',
            'activite_second': step1.activite_second.name if step1.activite_second else '',
            'activite_sec': step1.activite_sec if step1.activite_sec else '',
            'activity_code': step1.activity_code if step1.activity_code else '',
            'activity_description': step1.activity_description if step1.activity_description else '',
            'phone': step1.phone if step1.phone else '',
            'email': step1.email if step1.email else '',
            'siteweb': step1.siteweb if step1.siteweb else '',
            'gerant': step1.gerant.name if step1.gerant else '',

            #Champs One2many
            'facilite_accorde': facilite_accorde_data if step1.facilite_accorde else [],
            'apropos': apropos_data if step1.apropos else [],
            'kyc': kyc_data if step1.kyc else [],
            'gestion': gestion_data if step1.gestion else [],
            'fournisseur': fournisseur_data if step1.fournisseur else [],
            'client': client_data if step1.client else [],
            # commercial
            'detail_garantie_actuel_ids': detail_garantie_actuel_ids_data if step2.detail_garantie_actuel_ids else [],
            'detail_garantie_propose_ids': detail_garantie_propose_ids_data if step2.detail_garantie_propose_ids else [],
            'garantie_conf': garantie_conf_data if step2.garantie_conf else [],
            'garantie_fin': garantie_fin_data if step2.garantie_fin else [],
            'garantie_autres': garantie_autres_data if step2.garantie_autres else [],
            'risque_central': risque_central_data if step2.risque_central else [],
            'facitlite_existante': facitlite_existante_data if step2.facitlite_existante else [],

        }
        return Response(json.dumps({'data': dossier_data}), status=200, headers={'Content-Type': 'application/json'})


