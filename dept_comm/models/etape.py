from odoo import models, fields, api, _
import base64
import datetime
from io import BytesIO
import numpy as np
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import rcParams
from bidi.algorithm import get_display
import arabic_reshaper
from odoo.exceptions import ValidationError, UserError
import magic
import xlrd



List_items = ['هل العميل شخص مقرب سياسيا؟',
              'هل أحد الشركاء/المساهمين/مسير مقرب سياسيا؟',
              'هل العميل أو أحد الشركاء/المساهمين/مسير مقرب من البنك؟',
              'هل للعميل شركات زميلة / مجموعة؟',
              'المتعامل / أحد الشركاء مدرج ضمن القوائم السوداء',
              'المتعامل / أحد الشركاء مدرج ضمن قائمة الزبائن المتعثرين بمركزية المخاطر لبنك الجزائر']

List_risque = [
    'المباشرة قصيرة الأجل',
    'المباشرة متوسطة الأجل',
    'الغير المباشرة',
    'الاجمالي'
]
list_mouvement = [
    'السنة',
    'الإيداعات (1)',
    'الإيرادات (2)',
    '(1)/(2)',
    'الربحية',
]
List_position = [
    'الوضعية الجبائية',
    'الوضعية الشبه جبائية',
    'الوضعية الشبه جبائية لغير الاجراء'
]
list_fisc = [
    'السنة',
    'حقوق الملكية',
    'مجموع الديون',
    'نسبة المديونية leverage',
     'نسبة الالتزامات تجاه البنوك /Gearing',
    'رقم الاعمال',
    'EBIDTA',
    'صافي الربح',
    'راس المال العامل',
    'احتياجات راس المال العامل'
]

list_bilan = [
    ('1', 'حقوق الملكية'),
    ('1', 'رأس المال'),
    ('1', 'الاحتياطات'),
    ('1', 'الارباح المتراكمة (محتجزة+محققة)'),
    ('1', 'حقوق الملكية / مجموع الميزانية'),
    ('1', 'ACTIF NET IMMOBILISE CORPOREL'),
    ('1', 'الات ومعدات و عتاد نقل'),
    ('1', 'إهتلاكات المعدات'),
    ('1', 'اهتلاكات / آلات و معدات و عتاد نقل'),
    ('1', 'صافي رأس المال العامل'),
    ('1', 'احتياجات رأس المال العامل'),
    ('1', 'FR/BFR'),
    ('2', 'مجموع المطلوبات (الديون)'),
    ('2', 'التزامات بنكية'),
    ('2', 'تسهيلات الموردين'),
    ('2', 'ضرائب مستحقة غير مدفوعة'),
    ('2', 'مطلوبات أخرى متداولة'),
    ('2', 'نسبة المديونية Leverage'),
    ('2', 'الالتزامات تجاه البنوك / حقوق'),
    ('3', 'مجموع الميزانية'),
    ('3', '(المبيعات، الايرادات)'),
    ('3', 'EBITDA'),
    ('3', 'صافي الارباح'),
    ('3', 'صافي الارباح/المبيعات ROS'),
    ('3', 'معدل العائد على الموجودات ROA'),
    ('3', 'معدل العائد على حقوق الملكية ROE'),
    ('4', 'التدفقات النقدية التشغيلية'),
    ('4', 'نسبة التداول (السيولة)'),
    ('4', 'نسبة السيولة السريعة'),
    ('5', 'حقوق عند الزبائن'),
    ('5', 'المخزون'),
    ('5', 'متوسط دوران المخزون (يوم)'),
    ('5', 'متوسط فترة التحصيل (يوم)'),
    ('5', 'متوسط مدة تسهيلات الموردين  (يوم)'),
]

list_recap = [
    'فترة التحصيل بالأيام',
    'فترة دوران المخزون',
    'مدة تسهيلات الموردين',
    'فترة دوران رأس المال العامل',
    'المبلغ المستحق لتسهيلات قصيرة الأمد',
]
list_var = [
    'المبيعات',
    'كلفة المبيعات',
    'الذمم المدينة',
    'المخزون',
    'الذمم الدائنة',
]
list_garantie = [
    'وجود التأمين على العقارات والضمانات و صلاحيتها',
    'التعهد بتحويل الإيجارات في الحساب / توطين الصفقات في الحساب',
    'تقديم الحسابات المدققة للسنة الماضية في الآجال (خلال 6 أشهر)',
    'تغطية الضمانات تفوق 120%']
list_garantie_fisc = [
    'أقل مستوى لرأس المال',
    'خطاب التنازل عن حقوق سابقة',
    'هامش ضمان الجدية',
    'خطاب دمج الحسابات'
]
list_autre_term = [
    'رهن الحصص والاسهم',
    'رهن حسابات جارية/لأجل'
]
list_poste = [
    'الاطارات',
    'التقنيين',
    'التنفيذ'
]

list_siege = [
    'المقر الاجتماعي',
    'المقرات الثانوية 01',
    'المقرات الثانوية 02',
    'المقرات الثانوية 03'
]

list_situation = [
    'السنة',
    'حقوق الملكية',
    'مجموع الميزانية',
    'رقم الأعمال',
    'صافي الارباح'
]

list_bilan = [
    ('1', 'حقوق الملكية'),
    ('1', 'رأس المال'),
    ('1', 'الاحتياطات'),
    ('1', 'الارباح المتراكمة (محتجزة+محققة)'),
    ('1', 'حقوق الملكية / مجموع الميزانية'),
    ('1', 'ACTIF NET IMMOBILISE CORPOREL'),
    ('1', 'الات ومعدات و عتاد نقل'),
    ('1', 'إهتلاكات المعدات'),
    ('1', 'اهتلاكات / آلات و معدات و عتاد نقل'),
    ('1', 'صافي رأس المال العامل'),
    ('1', 'احتياجات رأس المال العامل'),
    ('1', 'FR/BFR'),
    ('2', 'مجموع المطلوبات (الديون)'),
    ('2', 'التزامات بنكية'),
    ('2', 'تسهيلات الموردين'),
    ('2', 'ضرائب مستحقة غير مدفوعة'),
    ('2', 'مطلوبات أخرى متداولة'),
    ('2', 'نسبة المديونية Leverage'),
    ('2', 'الالتزامات تجاه البنوك / حقوق'),
    ('3', 'مجموع الميزانية'),
    ('3', '(المبيعات، الايرادات)'),
    ('3', 'EBITDA'),
    ('3', 'صافي الارباح'),
    ('3', 'صافي الارباح/المبيعات ROS'),
    ('3', 'معدل العائد على الموجودات ROA'),
    ('3', 'معدل العائد على حقوق الملكية ROE'),
    ('4', 'التدفقات النقدية التشغيلية'),
    ('4', 'نسبة التداول (السيولة)'),
    ('4', 'نسبة السيولة السريعة'),
    ('5', 'حقوق عند الزبائن'),
    ('5', 'المخزون'),
    ('5', 'متوسط دوران المخزون (يوم)'),
    ('5', 'متوسط فترة التحصيل (يوم)'),
    ('5', 'متوسط مدة تسهيلات الموردين  (يوم)'),
]
list_bil = [
    ('1', 'حقوق الملكية'),
    ('2', 'رأس المال'),
    ('4', 'نتائج متراكمة'),
    ('13', 'مجموع المطلوبات (الديون)'),
    ('18', 'نسبة المديونية Leverage'),
    ('19', 'الالتزامات تجاه البنوك / حقوق(Gearing)'),
    ('21', 'رقم الأعمال'),
    ('22', 'EBITDA'),
    ('23', 'صافي الأرباح'),
    ('10', 'صافي رأس المال العامل'),
    ('11', 'احتياجات رأس المال العامل'),
]


class Etape(models.Model):
    _name = 'wk.etape.ponctuel'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    workflow = fields.Many2one('wk.workflow.ponctuel', ondelete="cascade")
    workflow_old = fields.Many2one('wk.workflow.dashboard', string='ملف سابق',related="workflow.workflow_old")
    state_etape = fields.Selection([('1', 'قيد الدراسة'),
                                    ('2', 'انتهاء التحليل'),
                                    ], default='1')
    state_etape_commercial = fields.Selection([('1', 'قيد الدراسة'),
                                    ('2', 'مدير الاعمال التجارية'),
                                    ('3', 'انتهاء التحليل'),
                                    ], default='1')
    etape = fields.Many2one('wk.state.ponctuel', string='Etape')
    name = fields.Char(string='Nom', related='etape.name', store=True)
    sequence = fields.Integer(string='Sequence', related='etape.sequence')
    state_compute = fields.Float(string='Pourcentage', compute='compute_pourcentage_state')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    raison_refus = fields.Text(string='سبب طلب المراجعة')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    chiffre_affaire = fields.Monetary(string='راس المال الحالي KDA', currency_field='currency_id',
                                      related='nom_client.chiffre_affaire')
    chiffre_affaire_creation = fields.Monetary(string='راس المال التاسيسي KDA', currency_field='currency_id',
                                               related='nom_client.chiffre_affaire_creation')
    montant_demande = fields.Float(string='المبلغ المطلوب')
    # lanced = fields.Boolean(string='Traitement lancé', compute='compute_visible_states')
    state = fields.Selection(related='workflow.state', store=True)
    nom_client = fields.Many2one('res.partner', string='اسم المتعامل',
                                 domain=lambda self: [('branche', '=', self.env.user.partner_id.branche.id),
                                                      ('is_client', '=', True)], )
    branche = fields.Many2one('wk.agence', string='الفرع', related='nom_client.branche')
    num_compte = fields.Char(string='رقم الحساب', related='nom_client.num_compte', store=True)
    demande = fields.Many2one('wk.type.demande', string='الطلب', )
    classification = fields.Many2one('wk.classification', string="تصنيف الشركة", related='nom_client.classification')
    adress_siege = fields.Char(string='عنوان المقر الاجتماعي', related='nom_client.adress_siege')
    wilaya = fields.Many2one('wk.wilaya', string='الولاية', related='nom_client.wilaya')
    nif = fields.Char(string='NIF', related='nom_client.nif')
    num_registre_commerce = fields.Char(string='رقم السجل التجاري', related='nom_client.rc')
    date_ouverture_compte = fields.Date(string='تاريخ فتح الحساب', related='nom_client.date_ouverture_compte')
    date_inscription = fields.Date(string='تاريخ القيد في السجل التجاري', related='nom_client.date_inscription')
    date_debut_activite = fields.Date(string='تاريخ بداية النشاط', related='nom_client.date_debut_activite')
    activite = fields.Many2one('wk.activite', string='النشاط الرئيسي حسب بنك الجزائر', related='nom_client.activite')
    activite_second = fields.Many2one('wk.secteur', string='النشاط الثانوي حسب السجل التجاري',
                                      related='nom_client.activite_second')
    activite_sec = fields.Char(string='النشاط الثانوي حسب السجل التجاري', related='nom_client.activite_sec')
    activity_code = fields.Char(string='رمز النشاط حسب السجل التجاري', related='nom_client.activity_code')
    activity_description = fields.Char(string='النشاط حسب السجل التجاري', related='nom_client.activity_description')
    phone = fields.Char(string='الهاتف', related='nom_client.mobile')
    email = fields.Char(string='البريد الإلكتروني', related='nom_client.email')
    siteweb = fields.Char(string='الموقع الالكتروني للشركة', related='nom_client.website')
    gerant = fields.Many2one('res.partner', string='المسير',
                             domain="[('parent_id', '=', nom_client),('is_company', '=', False)]")
    partner_id = fields.Many2one('res.partner', string='المسير', related='gerant', store=True)
    phone_gerant = fields.Char(string='الهاتف', related='gerant.mobile')
    email_gerant = fields.Char(string='البريد الإلكتروني', related='gerant.email')
    email_to = fields.Char(string='البريد الإلكتروني', store=True)
    email_from = fields.Char(string='البريد الإلكتروني', related='user_id.partner_id.email', store=True)
    author_id = fields.Many2one('res.partner', related='user_id.partner_id', store=True)
    user_id = fields.Many2one('res.users', string='المكلف بالملف', )
    annee_fiscal_list = fields.Many2one('wk.year', string='السنة المالية N', )
    description_company = fields.Text(string='تعريف الشركة')
    interet_company = fields.Text(string='اهمية العلاقة')
    unit_prod = fields.Text(string='وحدات الانتاج')
    stock = fields.Text(string='المخازن')
    prod_company = fields.Text(string='منتوجات الشركة')
    politique_comm = fields.Text(string='السياسة التسويقية')
    cycle_exploit = fields.Text(string='دورة الاستغلال')
    concurrence = fields.Text(string='المنافسة و دراسة السوق')
    program_invest = fields.Text(string='البرنامج الاستثماري /المشاريع التطويرية')
    result_visit = fields.Text(string='نتائج الزيارة')
    # images = fields.One2many('wk.documents', 'step_id', string='الصور المرفقة')
    forme_jur = fields.Many2one('wk.forme.jur', string='الشكل القانوني', related='nom_client.forme_jur')

    documents = fields.One2many('wk.document.check', 'step_id', string='التاكد من الوثائق المرفقة')

    kyc = fields.One2many('wk.kyc.details', 'step_id')
    apropos = fields.One2many('wk.partenaire', 'step_id', string='نبذة عن المتعامل')
    gestion = fields.One2many('wk.gestion', 'step_id', string='فريق التسيير')
    # employees = fields.One2many('wk.nombre.employee', 'step_id', string='عدد العمال (حسب الفئة المهنية)')
    # sieges = fields.One2many('wk.siege', 'step_id', string='مقرات تابعة للشركة')
    tailles = fields.One2many('wk.taille', 'step_id', string='حجم و هيكل التمويلات المطلوبة')
    situations = fields.One2many('wk.situation', 'step_id', string='التمويل لدى البنوك الاخرى')
    situations_fin = fields.One2many('wk.situation.fin', 'step_id',
                                     string='البيانات المالية المدققة للثلاث سنوات الأخيرة KDA')

    fournisseur = fields.One2many('wk.fournisseur', 'step_id', string='الموردين')
    client = fields.One2many('wk.client', 'step_id', string='الزبائن')
    companies = fields.One2many('wk.companies', 'step_id')

    avis_conseil = fields.Text('راي المكلف بالملف')
    recommendation_agence = fields.Text('توصية مدير الفرع')

    assigned_to_commercial = fields.Many2one('res.users', string='المكلف بالاعمال التجارية',
                                             domain=lambda self: [
                                                 ('groups_id', 'in',
                                                  self.env.ref('dept_wk.dept_wk_group_charge_commercial').id)],
                                             track_visibility='always')

    taux_change = fields.Float(string='1$ = ?DA: سعر الصرف', default=1)
    facilite_accorde = fields.One2many('wk.facilite.accorde', 'step_id',
                                       string='تفاصيل التسهيلات الممنوحة (KDA)')
    detail_garantie_actuel_ids = fields.One2many('wk.detail.garantie', 'step_id',
                                                 string='الضمانات العقارية الحالية')
    garantie_actuel_comment = fields.Text(string='تعليق')
    detail_garantie_propose_ids = fields.One2many('wk.detail.garantie.propose', 'step_id',
                                                  string='الضمانات العقارية المقترحة')
    garantie_propose_comment = fields.Text(string='تعليق')
    garantie_conf = fields.One2many('wk.garantie.conf', 'step_id',
                                    string='الشروط السابقة/المقترحة و الموافق عليها من لجان التمويل')
    garantie_fin = fields.One2many('wk.garantie.fin', 'step_id', string='الشروط المالية')
    garantie_autres = fields.One2many('wk.garantie.autres', 'step_id', string='الشروط الاخرى')
    risque_central = fields.One2many('wk.risque.line', 'step_id', string='مركزية المخاطر')
    compute_risque = fields.Float(string='compute field', compute='compute_risk')
    risque_date = fields.Date(string='مركزية المخاطر بتاريخ')
    nbr_banque = fields.Integer(string='عدد البنوك المصرحة')
    comment_risk_central = fields.Text(string='تعليق')
    capture_filename = fields.Char(default='ملف مركزية المخاطر')
    risk_capture = fields.Binary(string='ملف مركزية المخاطر')
    position_tax = fields.One2many('wk.position', 'step_id', string='الوضعية الجبائية والشبه جبائية')
    mouvement = fields.One2many('wk.mouvement', 'step_id',
                                string='الحركة والأعمال الجانبية للحساب مع مصرف السلام الجزائر (KDA)')
    detail_mouvement = fields.Text(string='التوطين البنكي')
    risk_scoring = fields.Many2one('risk.scoring', string='إدارة المخاطر', related='workflow.risk_scoring')
    companies_fisc = fields.One2many('wk.companies.fisc', 'step_id')
    comment_fisc = fields.Text(string='تعليق')
    visualisation2 = fields.Binary(string='visualisation')

    facitlite_existante = fields.One2many('wk.facilite.existante', 'step_id')

    mouvement_group = fields.One2many('wk.mouvement.group', 'step_id',
                                      string='الحركة والأعمال الجانبية للمجموعة مع مصرف السلام الجزائر (KDA)')
    tcr_id = fields.Many2one('import.ocr.tcr', string='TCR')
    passif_id = fields.Many2one('import.ocr.passif', string='Passif')
    actif_id = fields.Many2one('import.ocr.actif', string='Actif')
    bilan_id = fields.One2many('wk.bilan', 'step_id')
    bilan1_id = fields.One2many('wk.bilan.cat1', 'step_id')
    comment_cat1 = fields.Text(string='تعليق')
    bilan2_id = fields.One2many('wk.bilan.cat2', 'step_id')
    comment_cat2 = fields.Text(string='تعليق')
    bilan3_id = fields.One2many('wk.bilan.cat3', 'step_id')
    comment_cat3 = fields.Text(string='تعليق')
    bilan4_id = fields.One2many('wk.bilan.cat4', 'step_id')
    comment_cat4 = fields.Text(string='تعليق')
    bilan5_id = fields.One2many('wk.bilan.cat5', 'step_id')
    comment_cat5 = fields.Text(string='تعليق')
    comment_bilan = fields.Text(string='تعليق')
    tcr_id = fields.Many2one('import.ocr.tcr', string='TCR')
    passif_id = fields.Many2one('import.ocr.passif', string='Passif')
    actif_id = fields.Many2one('import.ocr.actif', string='Actif')
    analyse_secteur_act = fields.Text(string='تحليل قطاع عمل العميل')
    analyse_concurrence = fields.Text(string='تحليل المنافسة')
    ampleur_benefice = fields.Float(string='حجم الارباح PNB المتوقعة')
    analyse_relation = fields.Text(string='تحليل اهمية العلاقة على المدى المتوسط')
    recap_ids = fields.One2many('wk.recap', 'step_id')
    var_ids = fields.One2many('wk.variable', 'step_id')
    weakness_ids = fields.One2many('wk.swot.weakness', 'step_id')
    strength_ids = fields.One2many('wk.swot.strength', 'step_id')
    threat_ids = fields.One2many('wk.swot.threat', 'step_id')
    opportunitie_ids = fields.One2many('wk.swot.opportunitie', 'step_id')

    comite = fields.Many2one('wk.comite', string='اللجنة')
    recommandation_dir_fin = fields.Text(string='راي مدير ادارة التمويلات', track_visibility='always')
    facilite_propose = fields.One2many('wk.facilite.propose', 'step_id', string='التسهيلات المقترحة')
    garantie_ids = fields.Many2many('wk.garanties', 'garantie_relation', string='الضمانات المقترحة')
    garanties_demande_ids = fields.Many2many('wk.garanties', 'garantie_precedente_relat', string='الضمانات')
    exception_ids = fields.Many2many('wk.exception', string='الاستثناءات مع سياسة الائتمان')
    risk_scoring = fields.Many2one('risk.scoring', string='إدارة المخاطر')
    recommendation_1 = fields.Text(string='توصية مدير إدارة الاعمال التجارية')

    annee_fiscal = fields.Integer(string='السنة المالية N', compute='change_annee')

    def validate_information_commercial(self):
        for rec in self:
            if rec.state_etape_commercial == '1':
                rec.state_etape_commercial = '2'
            else:
                if rec.state_etape_commercial == '2':
                    rec.state_etape_commercial = '3'
                    template = self.env.ref('dept_comm.email_template_ponctuel')
                    return {
                        'name': _("تاكيد"),
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'confirmation.mail.send',
                        'target': 'new',
                        'context': {
                            'relance': False,
                            'is_step': True,
                            'default_folder_id': rec.workflow.id,
                            'default_step_id': rec.id,
                            'default_mail_template_id': template.id,
                        },
                    }

    def compute_pourcentage_state(self):
        for rec in self:
            partner = rec.workflow.states.filtered(lambda l: l.sequence == 1).gerant
            if partner:
                mail_invite = self.env['mail.wizard.invite'].with_context({
                    'default_res_model': 'wk.etape.ponctuel',
                    'default_res_id': rec.id
                }).with_user(self.env.user).create({
                    'partner_ids': [(4, partner.id)],
                    'notify': False})
                mail_invite.add_followers()
            if rec.state_etape == '1':
                rec.state_compute = 0
            else:
                rec.state_compute = 1
            if rec.etape.sequence == 2:
                if rec.state_etape_commercial == '1':
                    rec.state_compute = 0
                elif rec.state_etape_commercial == '2':
                    rec.state_compute = 0.5
                else:
                    rec.state_compute = 1

    def action_create_tcr(self):
        for rec in self:
            view_id = self.env.ref('financial_modeling.import_ocr_tcr_view_form').id
            return {
                'name': 'TCR',
                'domain': [('step_id', '=', rec.id)],
                'res_model': 'import.ocr.tcr',
                'view_mode': 'form',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'context': {'step_id': rec.id}
            }

    def action_create_actif(self):
        for rec in self:
            view_id = self.env.ref('financial_modeling.import_ocr_actif_view_form').id
            return {
                'name': 'Actif',
                'domain': [('step_id', '=', rec.id)],
                'res_model': 'import.ocr.actif',
                'view_mode': 'form',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'context': {'step_id': rec.id}
            }

    def action_create_passif(self):
        for rec in self:
            view_id = self.env.ref('financial_modeling.import_ocr_passif_view_form').id
            return {
                'name': 'Passif',
                'domain': [('step_id', '=', rec.id)],
                'res_model': 'import.ocr.passif',
                'view_mode': 'form',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'context': {'step_id': rec.id}
            }
    def validate_information(self):
        for rec in self:
            template = self.env.ref('dept_comm.email_template_ponctuel')
            return {
                'name': _("تاكيد"),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'confirmation.mail.send',
                'target': 'new',
                'context': {
                    'relance': False,
                    'is_step': True,
                    'default_folder_id': rec.workflow.id,
                    'default_step_id': rec.id,
                    'default_mail_template_id': template.id,
                },
            }

    def validate_information_function(self):
        for rec in self:
            print('i work')
            last_state = int(rec.state)
            actuel_state = int(rec.state) + 1
            rec.state = str(actuel_state)
            rec.state_etape = '2'
            rec.raison_refus = False
            last_track = self.env['wk.tracking.ponctuel'].search([('ponctuel_id', '=', rec.workflow.id),
                                                                  ('state', '=', last_state)])
            if last_track:
                last_track.date_fin = fields.Date.today()
            self.env['wk.tracking.ponctuel'].create({'ponctuel_id': rec.workflow.id,
                                            'state': rec.state,
                                            'date_debut': fields.Date.today(),
                                            'is_revision': True if rec.raison_refus else False,
                                            'comment': False})
            if actuel_state == '11':
                rec.date_fin = fields.Date.today()
            if rec.etape.sequence == 1:
                step_2 = rec.workflow.states.filtered(lambda l: l.sequence == 2)
                if not step_2:
                    rec.env['wk.etape.ponctuel'].create({
                                                    'workflow': rec.workflow.id,
                                                    'etape': self.env.ref('dept_comm.principe_2').id,
                                                    'nom_client': rec.nom_client.id})

    def a_revoir(self):
        for rec in self:
            view_id = self.env.ref('dept_comm.retour_ponctuel_form').id
            return {
                'name': 'سبب طلب المراجعة',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'wk.ponctuel.retour',
                'view_id': view_id,
                'target': 'new',
                'context': {'default_ponctuel_id': rec.workflow.id,
                            'default_state': rec.workflow.state}
            }


    def action_open_risk(self):
        for rec in self:
            view_id = self.env.ref('dept_comm.scoring_inherit_view_form').id
            if not rec.risk_scoring:
                scoring = self.env['risk.scoring'].create({
                    'partner_id': rec.nom_client.id,
                    'ponctuel_id': rec.workflow.id
                })
                rec.workflow.risk_scoring = scoring.id
            return {
                'name': 'ادارة المخاطر',
                'res_model': 'risk.scoring',
                'view_mode': 'form',
                'res_id': rec.risk_scoring.id,
                'view_id': view_id,
                'type': 'ir.actions.act_window',
            }
    @api.onchange('annee_fiscal_list')
    def change_annee(self):
        for rec in self:
            rec.annee_fiscal = int(rec.annee_fiscal_list.name)
            if rec.annee_fiscal_list:
                rec.situations_fin.filtered(lambda l: l.sequence == 0).write({
                    'year1': rec.annee_fiscal,
                    'year2': rec.annee_fiscal - 1,
                    'year3': rec.annee_fiscal - 2,
                })
                rec.mouvement.filtered(lambda l: l.sequence == 0).write({
                    'n_dz': rec.annee_fiscal,
                    'n1_dz': rec.annee_fiscal - 1,
                    'n2_dz': rec.annee_fiscal - 2,
                    'n3_dz': rec.annee_fiscal - 3,
                })
                rec.mouvement_group.filtered(lambda l: l.company == 'السنة').write({'n_dz': rec.annee_fiscal,
                                                                                    'n1_dz': rec.annee_fiscal - 1,
                                                                                    'n2_dz': rec.annee_fiscal - 2,
                                                                                    'sequence': 0})
                rec.companies_fisc.filtered(lambda l: l.sequence == 0).write({
                    'year_4': rec.annee_fiscal,
                    'year_3': rec.annee_fiscal - 1,
                    'year_2': rec.annee_fiscal - 2,
                    'year_1': rec.annee_fiscal - 3,
                })
                rec.bilan1_id.filtered(lambda l: l.declaration == 'السنة').write({
                    'year_1': rec.annee_fiscal - 3,
                    'year_2': rec.annee_fiscal - 2,
                    'year_3': rec.annee_fiscal - 1,
                    'year_4': rec.annee_fiscal, })
                rec.bilan2_id.filtered(lambda l: l.declaration == 'السنة').write({
                    'year_1': rec.annee_fiscal - 3,
                    'year_2': rec.annee_fiscal - 2,
                    'year_3': rec.annee_fiscal - 1,
                    'year_4': rec.annee_fiscal})
                rec.bilan3_id.filtered(lambda l: l.declaration == 'السنة').write({
                    'year_1': rec.annee_fiscal - 3,
                    'year_2': rec.annee_fiscal - 2,
                    'year_3': rec.annee_fiscal - 1,
                    'year_4': rec.annee_fiscal})
                rec.bilan4_id.filtered(lambda l: l.declaration == 'السنة').write({
                    'year_1': rec.annee_fiscal - 3,
                    'year_2': rec.annee_fiscal - 2,
                    'year_3': rec.annee_fiscal - 1,
                    'year_4': rec.annee_fiscal})
                rec.bilan5_id.filtered(lambda l: l.declaration == 'السنة').write({
                    'year_1': rec.annee_fiscal - 3,
                    'year_2': rec.annee_fiscal - 2,
                    'year_3': rec.annee_fiscal - 1,
                    'year_4': rec.annee_fiscal})
    def action_get_view(self):
        for rec in self:
            view_id = self.env.ref('dept_comm.view_wk_etape_ponctuel_form').id
            return {
                'type': 'ir.actions.act_window',
                'name': _('الفرع'),
                'view_mode': 'form',
                'res_model': 'wk.etape.ponctuel',
                'res_id': rec.id,
                'views': [[view_id, 'form']],
            }

    @api.model
    def create(self, vals):
        res = super(Etape, self).create(vals)
        count = 0
        for item in list_situation:
            line = self.env['wk.situation.fin'].create({'type': item,
                                                        'sequence': count,
                                                        'step_id': res.id})
            count += 1
        res.situations_fin.filtered(lambda l: l.sequence == 0).write({
            'year1': res.annee_fiscal,
            'year2': res.annee_fiscal - 1,
            'year3': res.annee_fiscal - 2,
        })
        for item in list_garantie:
            line = self.env['wk.garantie.conf'].create({'info': item, 'step_id': res.id})
        for item in list_garantie_fisc:
            line = self.env['wk.garantie.fin'].create({'info': item, 'step_id': res.id})
        for item in list_autre_term:
            line = self.env['wk.garantie.autres'].create({'info': item, 'step_id': res.id})
        for item in List_risque:
            line = self.env['wk.risque.line'].create({'declaration': item, 'step_id': res.id})
        for item in List_position:
            line = self.env['wk.position'].create({'name': item, 'step_id': res.id})
        count = 0
        for item in list_mouvement:
            line = self.env['wk.mouvement'].create({'mouvement': item,
                                                    'step_id': res.id,
                                                    'sequence': count})
            count += 1
        res.mouvement.filtered(lambda l: l.sequence == 0).write({
            'n_dz': res.annee_fiscal,
            'n1_dz': res.annee_fiscal - 1,
            'n2_dz': res.annee_fiscal - 2,
            'n3_dz': res.annee_fiscal - 3,
        })
        self.env['wk.mouvement.group'].create({'company': 'السنة',
                                               'step_id': res.id,
                                               'n_dz': res.annee_fiscal,
                                               'n1_dz': res.annee_fiscal - 1,
                                               'n2_dz': res.annee_fiscal - 2,
                                               'sequence': 0})
        count = 0
        for item in list_fisc:
            line = self.env['wk.companies.fisc'].create({'declaration': item,
                                                         'sequence': count,
                                                         'step_id': res.id})
            count += 1
        res.companies_fisc.filtered(lambda l: l.sequence == 0).write({
            'year_4': res.annee_fiscal,
            'year_3': res.annee_fiscal - 1,
            'year_2': res.annee_fiscal - 2,
            'year_1': res.annee_fiscal - 3,
        })
        vals = {'step_id': res.id,
                        'sequence': 0,
                        'declaration': 'السنة',
                        'year_3': res.annee_fiscal - 1,
                        'year_4': res.annee_fiscal,
                        }
        self.env['wk.bilan.cat1'].create(vals)
        self.env['wk.bilan.cat2'].create(vals)
        self.env['wk.bilan.cat3'].create(vals)
        self.env['wk.bilan.cat4'].create(vals)
        self.env['wk.bilan.cat5'].create(vals)
        count = 1
        for index, item in list_bilan:
            line = self.env['wk.bilan'].create({'declaration': item,
                                                'categorie': index,
                                                'step_id': res.id,
                                                'sequence': count})
            count += 1
        count = 1
        for item in list_recap:
            line = self.env['wk.recap'].create({'declaration': item, 'step_id': res.id, 'sequence': count})
            count += 1
        count = 1
        for item in list_var:
            line = self.env['wk.variable'].create({'var': item, 'step_id': res.id, 'sequence': count})
            count += 1

        return res
    
    tcr_id = fields.Many2one('import.ocr.tcr', string='TCR')
    passif_id = fields.Many2one('import.ocr.passif', string='Passif')
    actif_id = fields.Many2one('import.ocr.actif', string='Actif')

    def action_create_tcr(self):
        for rec in self:
            view_id = self.env.ref('financial_modeling.import_ocr_tcr_view_form').id
            return {
                'name': 'TCR',
                'domain': [('step_id', '=', rec.id)],
                'res_model': 'import.ocr.tcr',
                'view_mode': 'form',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'context': {'step_id': rec.id, 'year': 1}
            }
            
    def action_create_actif(self):
        for rec in self:
            view_id = self.env.ref('financial_modeling.import_ocr_actif_view_form').id
            return {
                'name': 'Actif',
                'domain': [('step_id', '=', rec.id)],
                'res_model': 'import.ocr.actif',
                'view_mode': 'form',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'context': {'step_id': rec.id, 'year': 1}
            }
    
    def action_create_passif(self):
        for rec in self:
            view_id = self.env.ref('financial_modeling.import_ocr_passif_view_form').id
            return {
                'name': 'Passif',
                'domain': [('step_id', '=', rec.id)],
                'res_model': 'import.ocr.passif',
                'view_mode': 'form',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'context': {'step_id': rec.id, 'year': 1}
            }
    
    def import_data(self):
        for rec in self:
            if rec.tcr_id.state not in ['valide', 'modified'] or rec.actif_id.state not in ['valide', 'modified'] or rec.passif_id.state not in ['valide', 'modified']:
                raise ValidationError("Vous devriez d'abord valider les bilans")
            else:
                to_delete = rec.bilan_id.filtered(lambda r: r.declaration in ['ACTIF NET IMMOBILISE CORPOREL',
                                                                              'الات ومعدات و عتاد نقل',
                                                                              'إهتلاكات المعدات',
                                                                              'اهتلاكات / آلات و معدات و عتاد نقل'])
                if to_delete:
                    to_delete1 = rec.bilan1_id.filtered(lambda r: r.sequence in [6, 7, 8, 9])
                    to_delete.unlink()
                    to_delete1.unlink()
                    other_bilan = rec.bilan_id.filtered(lambda r: r.sequence >= 6)
                    count = 6
                    for item in other_bilan:
                        in_view = self.env[f'wk.bilan.cat{item.categorie}'].search([('bilan', '=', item.id)])
                        item.sequence = in_view.sequence = count
                        count += 1
                    print(other_bilan)
                bilan_1 = rec.bilan_id.filtered(lambda r: r.sequence == 1)
                # total I حقوق الملكية
                passif_1 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 12)
                bilan_1.write({ 'year_4': passif_1.montant_n,
                                'year_3': passif_1.montant_n1})

                # capital emis رأس المال
                bilan_2 = rec.bilan_id.filtered(lambda r: r.sequence == 2)
                passif_2 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 2)
                bilan_2.write({'year_4': passif_2.montant_n,
                                'year_3': passif_2.montant_n1})

                # Passif - Autres capitaux propres - report à nouveau الاحتياطات
                bilan_3 = rec.bilan_id.filtered(lambda r: r.sequence == 3)
                passif_3 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 4)
                bilan_3.write({'year_4': passif_3.montant_n,
                                'year_3': passif_3.montant_n1})

                # الارباح المتراكمة
                bilan_4 = rec.bilan_id.filtered(lambda r: r.sequence == 4)
                passif_3 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 8)
                tcr_3 = rec.tcr_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 50)
                bilan_4.write({'year_4': passif_3.montant_n + tcr_3.montant_n,
                                'year_3': passif_3.montant_n1 + tcr_3.montant_n1})

                #حقوق الملكية / مجموع الميزانية
                bilan_5 = rec.bilan_id.filtered(lambda r: r.sequence == 5)
                passif_12 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 25)
                bilan_5.write({'year_4': (passif_1.montant_n / passif_12.montant_n) * 100 if passif_12.montant_n != 0 else 0,
                               'year_3': (passif_1.montant_n1 / passif_12.montant_n1) * 100 if passif_12.montant_n1 != 0 else 0})
                if passif_12.montant_n == 0:
                    bilan_5.is_null_4 = True
                else:
                    bilan_5.is_null_4 = False
                if passif_12.montant_n1 == 0:
                    bilan_5.is_null_3 = True
                else:
                    bilan_5.is_null_3 = False
                    
                # Passif (Total I + Total II) - Total actif non courant   صافي رأس المال العامل
                actif_2 = rec.actif_id.actif_lines.filtered(lambda r: r.rubrique.sequence == 16)
                actif1_2 = rec.actif1_id.actif_lines.filtered(lambda r: r.rubrique.sequence == 16)
                actif_27 = rec.actif_id.actif_lines.filtered(lambda r: r.rubrique.sequence == 27)
                passif_24 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 24)
                bilan_10 = rec.bilan_id.filtered(lambda r: r.sequence == 6)
                bilan_10.write({'year_4': actif_27.montant_n - passif_24.montant_n,
                                'year_3': actif_27.montant_n1 - passif_24.montant_n1
                                })

                # احتياجات رأس المال العامل
                passif_5 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 23)
                passif1_5 = rec.passif1_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 23)
                bilan_11 = rec.bilan_id.filtered(lambda r: r.sequence == 7)
                passif_20 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 20)
                passif1_20 = rec.passif1_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 20)
                actif_18 = rec.actif_id.actif_lines.filtered(lambda r: r.rubrique.sequence == 18)
                actif_20 = rec.actif_id.actif_lines.filtered(lambda r: r.rubrique.sequence == 20)
                actif_126 = rec.actif_id.actif_lines.filtered(lambda r: r.rubrique.sequence == 26)
                bilan_11.write({'year_4': actif_27.montant_n - actif_126.montant_n - (passif_24.montant_n - passif_5.montant_n),
                                'year_3': actif_27.montant_n1 - actif_126.montant_n1 - (passif_24.montant_n1 - passif_5.montant_n1),
                                })

                # FR / BFR Passif (Total I + Total II) - Actif (Total actif non courant)  / Actif (Stock et encours + Créances et emploi assimili + Disponibilité et assimilé) - Passif (Total III)
                bilan_12 = rec.bilan_id.filtered(lambda r: r.sequence == 8)
                actif_4 = rec.actif_id.actif_lines.filtered(lambda r: r.rubrique.sequence == 18)

                if bilan_11.year_4 == 0:
                    bilan_12.is_null_4 = True
                if bilan_11.year_4 == 0:
                    bilan_12.is_null_3 = True
                if bilan_11.year_4 == 0:
                    bilan_12.is_null_2 = True
                if bilan_11.year_4 == 0:
                    bilan_12.is_null_1 = True
                bilan_12.write({'year_4': (bilan_10.year_4 / bilan_11.year_4) * 100 if bilan_11.year_4 != 0 else 0,
                                'year_3': (bilan_10.year_3 / bilan_11.year_3) * 100 if bilan_11.year_3 != 0 else 0,
                                })
                # مجموع المطلوبات Passif - Total II + Total III
                bilan_13 = rec.bilan_id.filtered(lambda r: r.sequence == 9)
                passif_5 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 18)
                passif_6 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 24)
                bilan_13.write({'year_4': passif_5.montant_n + passif_6.montant_n, 
                                'year_3': passif_5.montant_n1 + passif_6.montant_n1, 
                                })

                # التزامات بنكية
                bilan_14 = rec.bilan_id.filtered(lambda r: r.sequence == 10)
                passif_5 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 23)
                passif_6 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 14)

                bilan_14.write({'year_4': passif_5.montant_n + passif_6.montant_n,
                                'year_3': passif_5.montant_n1 + passif_6.montant_n1,
                                })
                # تسهيلات الموردين
                bilan_15 = rec.bilan_id.filtered(lambda r: r.sequence == 11)
                passif_7 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 20)
                var_5 = rec.var_ids.filtered(lambda r: r.sequence == 5)
                bilan_15.write({'year_4': passif_7.montant_n,
                               'year_3': passif_7.montant_n1})

                var_5.write({'montant': passif_7.montant_n})

                # Passif - Impôts مستحقات ضرائب
                bilan_16 = rec.bilan_id.filtered(lambda r: r.sequence == 12)
                passif_8 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 21)
                bilan_16.write({'year_4': passif_8.montant_n,
                               'year_3': passif_8.montant_n1
                               })

                #Passif - Autres dettes + fournisseur  مطلوبات أخرى متداولة
                bilan_17 = rec.bilan_id.filtered(lambda r: r.sequence == 13)
                passif_8 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 22)
                bilan_17.write({'year_4': passif_8.montant_n,
                                'year_3': passif_8.montant_n1
                                })

                # (Emprunts et dettes financières passif + Trésorerie passif - Trésorerie coté actif ) / Total I coté passif نسبة المديونية Leverage
                bilan_18 = rec.bilan_id.filtered(lambda r: r.sequence == 14)
                passif_18 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 18)
                passif_24 = rec.passif_id.passif_lines.filtered(lambda r: r.rubrique.sequence == 24)
                bilan_18.write({'year_4': (passif_18.montant_n + passif_24.montant_n) / passif_1.montant_n if passif_1.montant_n != 0 else 0,
                               'year_3': (passif_18.montant_n1 + passif_24.montant_n1) / passif_1.montant_n1 if passif_1.montant_n1 != 0 else 0
                               })
                if passif_1.montant_n == 0:
                    bilan_18.is_null_4 = True
                else:
                    bilan_18.is_null_4 = False
                if passif_1.montant_n1 == 0:
                    bilan_18.is_null_3 = True
                else:
                    bilan_18.is_null_3 = False

                #الالتزامات اتجاه البنوك / الحقوق
                bilan_19 = rec.bilan_id.filtered(lambda r: r.sequence == 15)
                bilan_19.write({'year_4': bilan_14.year_4 / passif_1.montant_n if passif_1.montant_n != 0 else 0,
                                'year_3': bilan_14.year_3 / passif_1.montant_n1 if passif_1.montant_n1 != 0 else 0
                                })

                if passif_1.montant_n == 0:
                    bilan_19.is_null_4 = True
                else:
                    bilan_19.is_null_4 = False
                if passif_1.montant_n1 == 0:
                    bilan_19.is_null_3 = True
                else:
                    bilan_19.is_null_3 = False

                # مجموع الميزانية
                bilan_20 = rec.bilan_id.filtered(lambda r: r.sequence == 16)
                bilan_20.write({'year_4': passif_12.montant_n,
                                'year_3': passif_12.montant_n1
                                })
                # المبيعات ، الايرادات
                bilan_21 = rec.bilan_id.filtered(lambda r: r.sequence == 17)
                tcr_1 = rec.tcr_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 7)
                tcr1_1 = rec.tcr1_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 7)
                var_1 = rec.var_ids.filtered(lambda r: r.sequence == 1)
                bilan_21.write({'year_4': tcr_1.montant_n,
                                'year_3': tcr_1.montant_n1
                                })
                var_1.write({'montant': tcr_1.montant_n})
                # TCR- Excédent brut d`exploitation   EBITDA
                bilan_22 = rec.bilan_id.filtered(lambda r: r.sequence == 18)
                tcr_2 = rec.tcr_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 33)
                bilan_22.write({'year_4': tcr_2.montant_n,
                                'year_3': tcr_2.montant_n1})

                # TCR - Résultat net de l`exercice   صافي الأرباح
                bilan_23 = rec.bilan_id.filtered(lambda r: r.sequence == 19)
                tcr_3 = rec.tcr_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 50)
                bilan_23.write({'year_4': tcr_3.montant_n,
                                'year_3': tcr_3.montant_n1})

                bilan_24 = rec.bilan_id.filtered(lambda r: r.sequence == 20)
                # صافي الأرباح/المبيعات
                bilan_24.write({'year_4': (tcr_3.montant_n / tcr_1.montant_n) * 100 if tcr_1.montant_n != 0 else 0,
                                'year_3': (tcr_3.montant_n1 / tcr_1.montant_n1) * 100 if tcr_1.montant_n1 != 0 else 0})

                if tcr_1.montant_n == 0:
                    bilan_24.is_null_4 = True
                else:
                    bilan_24.is_null_4 = False
                if tcr_1.montant_n1 == 0:
                    bilan_24.is_null_3 = True
                else:
                    bilan_24.is_null_3 = False
                if tcr1_1.montant_n == 0:
                    bilan_24.is_null_2 = True
                else:
                    bilan_24.is_null_2 = False
                if tcr1_1.montant_n1 == 0:
                    bilan_24.is_null_1 = True
                else:
                    bilan_24.is_null_1 = False
                # معدل العائد على الموجودات ROA
                bilan_25 = rec.bilan_id.filtered(lambda r: r.sequence == 21)
                bilan_25.write({'year_4': (tcr_3.montant_n / actif_2.montant_n) * 100 if actif_2.montant_n != 0 else 0,
                                'year_3': (tcr_3.montant_n1 / actif_2.montant_n1) * 100 if actif_2.montant_n1 != 0 else 0})

                if actif_2.montant_n == 0:
                    bilan_25.is_null_4 = True
                else:
                    bilan_25.is_null_4 = False
                if actif_2.montant_n1 == 0:
                    bilan_25.is_null_3 = True
                else:
                    bilan_25.is_null_3 = False
                if actif1_2.montant_n == 0:
                    bilan_25.is_null_2 = True
                else:
                    bilan_25.is_null_2 = False
                if actif1_2.montant_n1 == 0:
                    bilan_25.is_null_1 = True
                else:
                    bilan_25.is_null_1 = False
                # معدل العائد على حقوق الملكية ROE
                bilan_26 = rec.bilan_id.filtered(lambda r: r.sequence == 22)
                bilan_26.write({'year_4': (tcr_3.montant_n / passif_1.montant_n) * 100 if passif_1.montant_n != 0 else 0,
                                'year_3': (tcr_3.montant_n1 / passif_1.montant_n1) * 100 if passif_1.montant_n1 != 0 else 0})

                if passif_1.montant_n == 0:
                    bilan_26.is_null_4 = True
                else:
                    bilan_26.is_null_4 = False
                if passif_1.montant_n1 == 0:
                    bilan_26.is_null_3 = True
                else:
                    bilan_26.is_null_3 = False
                    
                # التدفقات النقدية التشغيلية
                bilan_27 = rec.bilan_id.filtered(lambda r: r.sequence == 23)
                tcr_36 = rec.tcr_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 36)
                bilan_27.write(
                    {'year_4': tcr_3.montant_n + tcr_36.montant_n,
                     'year_3': tcr_3.montant_n1 + tcr_36.montant_n1})

                # نسبة التداول (السيولة)
                actif_26 = rec.actif_id.actif_lines.filtered(lambda r: r.rubrique.sequence == 26)
                bilan_28 = rec.bilan_id.filtered(lambda r: r.sequence == 24)
                bilan_28.write({'year_4': (actif_26.montant_n + actif_18.montant_n + actif_20.montant_n) / (passif_5.montant_n + passif_20.montant_n) if passif_5.montant_n + passif_20.montant_n != 0 else 0,
                                'year_3': (actif_26.montant_n1 + actif_18.montant_n1 + actif_20.montant_n1) / (passif_5.montant_n1 + passif_20.montant_n1) if passif_5.montant_n1 + passif_20.montant_n1 != 0 else 0})

                #نسبة السيولة السريعة
                bilan_29 = rec.bilan_id.filtered(lambda r: r.sequence == 25)
                bilan_29.write({'year_4': (actif_26.montant_n) / (passif_5.montant_n + passif_20.montant_n) if passif_5.montant_n + passif_20.montant_n != 0 else 0,
                                'year_3': (actif_26.montant_n) / (passif_5.montant_n1 + passif_20.montant_n1) if passif_5.montant_n1 + passif_20.montant_n1 != 0 else 0
                                })

                if (passif_5.montant_n + passif_20.montant_n) == 0:
                    bilan_28.is_null_4 = True
                    bilan_29.is_null_4 = True
                else:
                    bilan_28.is_null_4 = False
                    bilan_29.is_null_4 = False
                if (passif_5.montant_n1 + passif_20.montant_n1) == 0:
                    bilan_28.is_null_3 = True
                    bilan_29.is_null_3 = True
                else:
                    bilan_28.is_null_3 = False
                    bilan_29.is_null_3 = False
                if (passif1_5.montant_n + passif1_20.montant_n) == 0:
                    bilan_28.is_null_2 = True
                    bilan_29.is_null_2 = True
                else:
                    bilan_28.is_null_2 = False
                    bilan_29.is_null_2 = False
                if (passif1_5.montant_n1 + passif1_20.montant_n1) == 0:
                    bilan_28.is_null_1 = True
                    bilan_29.is_null_1 = True
                else:
                    bilan_28.is_null_1 = False
                    bilan_29.is_null_1 = False
                #حقوق عند الزبائن
                bilan_30 = rec.bilan_id.filtered(lambda r: r.sequence == 26)
                actif_5 = rec.actif_id.actif_lines.filtered(lambda r: r.rubrique.sequence == 20)
                var_3 = rec.var_ids.filtered(lambda r: r.sequence == 3)
                bilan_30.write({'year_4': actif_5.montant_n,
                                'year_3': actif_5.montant_n1
                                })
                var_3.write({'montant': actif_5.montant_n})

                # المخزون
                bilan_31 = rec.bilan_id.filtered(lambda r: r.sequence == 27)
                bilan_31.write({'year_4': actif_4.montant_n,
                                'year_3': actif_4.montant_n1
                                })
                var_4 = rec.var_ids.filtered(lambda r: r.sequence == 4)
                var_4.write({'montant': actif_4.montant_n})

                #متوسط دوران المخزون (يوم)
                bilan_32 = rec.bilan_id.filtered(lambda r: r.sequence == 28)
                tcr_5 = rec.tcr_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 12)
                tcr1_5 = rec.tcr1_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 12)
                tcr_6 = rec.tcr_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 13)
                tcr1_6 = rec.tcr1_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 13)
                tcr_14 = rec.tcr_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 14)
                tcr1_14 = rec.tcr1_id.tcr_lines.filtered(lambda r: r.rubrique.sequence == 14)
                var_2 = rec.var_ids.filtered(lambda r: r.sequence == 2)
                bilan_32.write({'year_4': (actif_4.montant_n * 360) / (tcr_5.montant_n + tcr_6.montant_n + tcr_14.montant_n) if (tcr_5.montant_n + tcr_6.montant_n + tcr_14.montant_n) != 0 else 0,
                                'year_3': (actif_4.montant_n1 * 360) / (tcr_5.montant_n1 + tcr_6.montant_n1 + tcr_14.montant_n1) if (tcr_5.montant_n1 + tcr_6.montant_n1 + tcr_14.montant_n1) != 0 else 0
                                })

                if (tcr_5.montant_n + tcr_6.montant_n + tcr_14.montant_n) == 0:
                    bilan_32.is_null_4 = True
                else:
                    bilan_32.is_null_4 = False
                if (tcr_5.montant_n1 + tcr_6.montant_n1 + tcr_14.montant_n1) == 0:
                    bilan_32.is_null_3 = True
                else:
                    bilan_32.is_null_3 = False
                if (tcr1_5.montant_n + tcr1_6.montant_n + tcr1_14.montant_n) == 0:
                    bilan_32.is_null_2 = True
                else:
                    bilan_32.is_null_2 = False
                if (tcr1_5.montant_n1 + tcr1_6.montant_n1 + tcr1_14.montant_n1) == 0:
                    bilan_32.is_null_1 = True
                else:
                    bilan_32.is_null_1 = False

                var_2.write({'montant': (tcr_5.montant_n + tcr_6.montant_n)})
                recap_2 = rec.recap_ids.filtered(lambda r: r.sequence == 2)
                recap_2.write({'montant': bilan_32.year_4})
                #متوسط فترة التحصيل (يوم)

                bilan_33 = rec.bilan_id.filtered(lambda r: r.sequence == 29)
                bilan_33.write({'year_4': (actif_5.montant_n * 360) / tcr_1.montant_n if tcr_1.montant_n != 0 else 0,
                                'year_3': (actif_5.montant_n1 * 360) / tcr_1.montant_n1 if tcr_1.montant_n1 != 0 else 0})
                if tcr_1.montant_n == 0:
                    bilan_33.is_null_4 = True
                else:
                    bilan_33.is_null_4 = False
                if tcr_1.montant_n1 == 0:
                    bilan_33.is_null_3 = True
                else:
                    bilan_33.is_null_3 = False
                if tcr1_1.montant_n == 0:
                    bilan_33.is_null_2 = True
                else:
                    bilan_33.is_null_2 = False
                if tcr1_1.montant_n1 == 0:
                    bilan_33.is_null_1 = True
                else:
                    bilan_33.is_null_1 = False
                recap_1 = rec.recap_ids.filtered(lambda r: r.sequence == 1)
                recap_1.write({'montant': bilan_33.year_4})

                #متوسط مدة تسهيلات الموردين (يوم)
                bilan_34 = rec.bilan_id.filtered(lambda r: r.sequence == 30)
                bilan_34.write({'year_4': (passif_7.montant_n * 360) / (tcr_5.montant_n + tcr_6.montant_n) if (tcr_5.montant_n + tcr_6.montant_n) != 0 else 0,
                                'year_3': (passif_7.montant_n1 * 360) / (tcr_5.montant_n1 + tcr_6.montant_n1) if (tcr_5.montant_n1 + tcr_6.montant_n1) != 0 else 0
                                })
                if (tcr_5.montant_n + tcr_6.montant_n) == 0:
                    bilan_34.is_null_4 = True
                else:
                    bilan_34.is_null_4 = False
                if (tcr_5.montant_n1 + tcr_6.montant_n1) == 0:
                    bilan_34.is_null_3 = True
                else:
                    bilan_34.is_null_3 = False
                if (tcr1_5.montant_n + tcr1_6.montant_n) == 0:
                    bilan_34.is_null_2 = True
                else:
                    bilan_34.is_null_2 = False
                if (tcr1_5.montant_n1 + tcr1_6.montant_n1) == 0:
                    bilan_34.is_null_1 = True
                else:
                    bilan_34.is_null_1 = False

                recap_3 = rec.recap_ids.filtered(lambda r: r.sequence == 3)
                recap_3.write({'montant': bilan_34.year_4})
                recap_4 = rec.recap_ids.filtered(lambda r: r.sequence == 4)
                recap_4.write({'montant': (bilan_10.year_4 * 360) / tcr_1.montant_n if tcr_1.montant_n != 0 else 0})
                recap_5 = rec.recap_ids.filtered(lambda r: r.sequence == 5)
                recap_5.write({'montant': passif_5.montant_n})
                recap_to_delete = rec.recap_ids.filtered(lambda r: r.sequence in [6, 7])
                recap_to_delete.unlink()

def view_viz(data1, data2):
    year = ["N-2", "N-1", "N"]
    fig, ax = plt.subplots()
    width = 0.25
    X_axis = np.arange(len(year))
    label1 = 'NRC'
    label2 = 'CA'
    plt.rcParams['font.family'] = 'DejaVu Sans'
    rects1 = ax.bar(X_axis - (width / 2), data1, width, color="yellow", label=label1)
    rects2 = ax.bar(X_axis + (width / 2), data2, width, color="orange", label=label2)
    ax.set_ylabel('Montant')
    ax.set_title('Montant par année')
    ax.set_xticks(X_axis + width, year)
    ax.legend(loc="lower left", bbox_to_anchor=(0.8, 1.0))
    fig.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='jpeg', dpi=100)
    buf.seek(0)
    imageBase64 = base64.b64encode(buf.getvalue())
    buf.close()
    return imageBase64
