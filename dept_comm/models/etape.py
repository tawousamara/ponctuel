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

List_Bilan = [
    'حقوق الملكية',
    'رأس المال',
    'نتائج متراكمة',
    'مجموع المطلوبات',
    'التزامات بنكية قصيرة الأجل',
    'التزامات بنكية متوسطة الأجل',
    'تسهيلات الموردين',
    'مستحقات ضرائب',
    'مطلوبات أخرى متداولة',
    'Leverage',
    'مجموع الميزانية',
    'رقم الأعمال',
    'EBITDA',
    'صافي الأرباح',
    'صافي الأرباح/المبيعات',
    'قدرة التمويل الذاتي CAF',
    'صافي رأس المال العامل',
    'احتياجات رأس المال العامل',
    'نسبة التداول (السيولة)',
    'نسبة السيولة السريعة',
    'حقوق عند الزبائن',
    'المخزون',
    'متوسط دوران المخزون (يوم)',
    'متوسط فترة التحصيل (يوم)',
    'متوسط مدة تسهيلات الموردين (يوم)'
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
    etape = fields.Many2one('wk.state.ponctuel', string='Etape')

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    raison_refus = fields.Text(string='سبب طلب المراجعة')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    chiffre_affaire = fields.Monetary(string='راس المال الحالي KDA', currency_field='currency_id',
                                      related='nom_client.chiffre_affaire')
    chiffre_affaire_creation = fields.Monetary(string='راس المال التاسيسي KDA', currency_field='currency_id',
                                               related='nom_client.chiffre_affaire_creation')
    montant_demande = fields.Float(string='المبلغ المطلوب')
    # lanced = fields.Boolean(string='Traitement lancé', compute='compute_visible_states')

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
    comment_bilan = fields.Text(string='تعليق')
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

    annee_fiscal = fields.Integer(string='السنة المالية N', compute='change_annee')


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
