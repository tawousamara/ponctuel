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

    @http.route('/api/v1/get_detail', auth='public', type='json', methods=['POST'], cors='*')
    def get_dossier(self, **kw):
        request_body = request.httprequest.data.decode('utf-8')
        data = json.loads(request_body)
        dossier_id = data.get('dossier_id')

        if not dossier_id:
            return Response(json.dumps({'error': 'Dossier ID not provided'}), status=400,
                            headers={'Content-Type': 'application/json'})

        dossier = request.env['wk.workflow.ponctuel'].sudo().browse(dossier_id)

        if not dossier.exists():
            return Response(json.dumps({'error': 'Dossier not found'}), status=404,
                            headers={'Content-Type': 'application/json'})

        step1 = dossier.states.filtered(lambda l: l.sequence == 1)
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
                # نوع التسهيلات
                'type_demande_ids': demande_ids,
                # تاريخ الرخصة
                'date': item.date,
                # الحالي
                'montant_acctual': item.montant_da_actuel,
                # المطلوبة
                'montant_demande': item.montant_da_demande,
                # الاجمالي الصافي
                'total': item.montant_da_total,
                # التأمين النقدي
                'percent': item.garantie_montant,
            }
            facilite_accorde_data.append(element)

        step2 = dossier.states.filtered(lambda l: l.sequence == 2)
        donnee_financiere = {}
        # حقوق الملكية
        droit = step2.bilan_id.filtered(lambda l: l.sequence == 1)
        donnee_financiere["rights"] = {
            'name': 'حقوق الملكية',
            '2023': droit.year_3,
            '2024': droit.year_4,
        }
        # رأس المال
        capital = step2.bilan_id.filtered(lambda l: l.sequence == 2)
        donnee_financiere["capital"] = {
            'name': 'رأس المال',
            '2023': capital.year_3,
            '2024': capital.year_4,
        }
        # احتياجات رأس المال العامل
        bfr = step2.bilan_id.filtered(lambda l: l.sequence == 11)
        donnee_financiere["rights_active"] = {
            'name': 'احتياجات رأس المال العامل',
            '2023': bfr.year_3,
            '2024': bfr.year_4,
        }
        # صافي الارباح
        benifice = step2.bilan_id.filtered(lambda l: l.sequence == 23)
        donnee_financiere["profit"] = {
            'name': 'صافي الارباح',
            '2023': benifice.year_3,
            '2024': benifice.year_4,
        }
        # EBITDA
        ebitda = step2.bilan_id.filtered(lambda l: l.sequence == 22)
        donnee_financiere["EBITDA"] = {
            'name': 'EBITDA',
            '2023': ebitda.year_3,
            '2024': ebitda.year_4,
        }

        dossier_data = {
            #الراس المال الحالي
            'dossier_id': dossier.id,
            'capital': dossier.nom_client.chiffre_affaire if dossier.nom_client else '',
            # تفاصيل التسهيلات الممنوحة
            'tableau_bord': facilite_accorde_data if step1.facilite_accorde else [],
            #tableau bilan
            'detail_finance': donnee_financiere,
            'rank': dossier.risk_scoring.resultat_scoring if dossier.risk_scoring else 0
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
                # نوع التسهيلات
                'type_demande_ids': demande_ids,
                # تاريخ الرخصة
                'date': item.date,
                # الحالي
                'montant_da_actuel': item.montant_da_actuel,
                # المطلوبة
                'montant_da_demande': item.montant_da_demande,
                # الاجمالي الصافي
                'montant_da_total': item.montant_da_total,
                # التأمين النقدي
                'garantie_montant': item.garantie_montant,
                # ملاحظات
                'remarques': item.remarques
            }
            facilite_accorde_data.append(element)

        #توزيع راس مال الشركة
        apropos_data = []
        for item in step1.apropos:
            element = {
                # اسم الشريك/المالك
                'nom_partenaire': item.nom_partenaire,
                # تاريخ التاسيس/الميلاد
                'age': item.age,
                # صفة الشريك
                'statut_partenaire': item.statut_partenaire,
                # الجنسية
                'nationalite': item.nationalite.name,
                # نسبة الحصة
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
                # معلومات إضافية عن العميل
                'info': item.info,
                # نعم/ لا
                'answer': answer,
                # التفاصيل
                'detail': item.detail,
            }
            kyc_data.append(element)

        # فريق التسيير
        gestion_data = []
        for item in step1.gestion:
            element = {
                # السيد(ة)
                'name': item.name,
                # المهنة
                'job': item.job,
                # المستوى الدراسي
                'niveau_etude': item.niveau_etude,
                # السن
                'age': item.age,
                # الخبرة المهنية
                'experience': item.experience
            }
            gestion_data.append(element)

        # الوضعية المالية لدى الغير
        situations_data = []
        for item in step1.situations:
            element = {
                # البنك
                'banque': item.banque.name,
                # نوع التمويل
                'type_fin': item.type_fin.name,
                # المبلغ KDA
                'montant': item.montant,
                # المبلغ المستغل KDA
                'encours': item.encours,
                # الضمانات الممنوحة
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
                # الاسم
                'name': item.name,
                # البلد
                'country': item.country.name,
                # طريقة السداد
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
                # الاسم
                'name': item.name,
                # البلد
                'country': item.country.name,
                # طريقة السداد
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
                # نوعية الضمان
                'type_garantie': item.type_garantie.name,
                # نوعية العقد
                'type_contrat': item.type_contrat.name,
                # القيمة
                'montant': item.montant,
                # تاريخ التقييم
                'date': item.date,
                # التغطية
                'recouvrement': item.recouvrement,
                # كفاية الضمانات قابلية التنفيذ عليها
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
                # نوعية الضمان
                'type_garantie': item.type_garantie.name,
                # نوعية العقد
                'type_contrat': item.type_contrat.name,
                # القيمة
                'montant': item.montant,
                # تاريخ التقييم
                'date': item.date,
                # التغطية
                'recouvrement': item.recouvrement,
                # كفاية الضمانات قابلية التنفيذ عليها
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
                # الشروط السابقة و المقترحة
                'info': item.info,
                # نعم/ لا
                'answer': answer,
                # التعليق
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
                # الشروط السابقة و المقترحة
                'info': item.info,
                # نعم/ لا
                'answer': answer,
                # التعليق
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
                # الشروط السابقة و المقترحة
                'info': item.info,
                # نعم/ لا
                'answer': answer,
                # التعليق
                'detail': item.detail,
            }
            garantie_autres_data.append(element)

        # مركزية المخاطر
        risque_central_data = []
        for item in step2.risque_central:
            element = {
                # البيان
                'declaration': item.declaration,
                # السلام:الممنوح
                'montant_esalam_dz_donne': item.montant_esalam_dz_donne,
                # المستغل
                'montant_esalam_dz_used': item.montant_esalam_dz_used,
                # اخرى :الممنوحة
                'montant_other_dz_donne': item.montant_other_dz_donne,
                # المستغل
                'montant_other_dz_used': item.montant_other_dz_used,
                # الاجمالي:الممنوحة
                'montant_total_dz_donne': item.montant_total_dz_donne,
                # المستغل
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
            garanties = ''
            if len(item.garanties) != 1:
                for line in item.garanties:
                    garanties += line.name + ' / '
            else:
                for line in item.garanties:
                    garanties += line.name
            element = {
                # الشركة
                'company': item.company,
                # نوع التسهيلات
                'facilite': item.facilite.name,
                # نوع التسهيلات
                'type_demande_ids': demande_ids,
                # الخام الحالي
                'brut_da': item.brut_da,
                # الصافي الحالي
                'net_da': item.net_da,
                # الضمانات
                'garanties' : item.garanties
            }
            facitlite_existante_data.append(element)

        dossier_data = {
            #Champs bruts
            # الغرض من الطلب
            'explanation': dossier.explanation if dossier.explanation else '',
            # الطلب
            'demande': dossier.demande.name if dossier.demande else '',
            # الفرع
            'branche': dossier.branche.ref if dossier.branche else '',
            #تصنيف الشركة
            'classification': step1.classification.name if step1.classification else '',
            #عنوان المقر الاجتماعي
            'adress_siege': step1.adress_siege if step1.adress_siege else '',
            # NIF
            'nif': step1.nif if step1.nif else '',
            # رقم السجل التجاري
            'num_registre_commerce': step1.num_registre_commerce if step1.num_registre_commerce else '',
            # تاريخ فتح الحساب
            'date_ouverture_compte': step1.date_ouverture_compte if step1.date_ouverture_compte else '',
            # تاريخ القيد في السجل التجاري
            'date_inscription': step1.date_inscription if step1.date_inscription else '',
            # تاريخ بداية النشاط
            'date_debut_activite': step1.date_debut_activite if step1.date_debut_activite else '',
            # النشاط
            'activite': step1.activite.name if step1.activite else '',
            # النشاط الثانوي حسب السجل التجاري
            'activite_second': step1.activite_second.name if step1.activite_second else '',
            # رمز النشاط الثانوي في السجل التجاري
            'activite_sec': step1.activite_sec if step1.activite_sec else '',
            # رمز النشاط حسب السجل التجاري
            'activity_code': step1.activity_code if step1.activity_code else '',
            # لنشاط حسب السجل التجاري
            'activity_description': step1.activity_description if step1.activity_description else '',
            # الهاتف
            'phone': step1.phone if step1.phone else '',
            # البريد الإلكتروني
            'email': step1.email if step1.email else '',
            # الموقع الالكتروني للشركة
            'siteweb': step1.siteweb if step1.siteweb else '',
            # المسير
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
