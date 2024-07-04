from odoo import models, fields, api, _
import datetime
from odoo.exceptions import ValidationError



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


class Ponctuel(models.Model):
    _name = 'wk.workflow.ponctuel'
    _description = 'Workflow de demande de financement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='تاريخ البدء', default=fields.Date.today)
    date_fin = fields.Date(string='تاريخ الانتهاء')
    name = fields.Char(string='Réference')
    state = fields.Selection([('1', 'الفرع'),
                              ('2', 'إدارة الاعمال التجارية'),
                              ('3', 'إدارة  الدراسات الائتمانية للمؤسسات'),
                              ('4', 'خلية إدارة المخاطر'),
                              ('5', 'قطاع  الخزينة و العمليات المحلية و الدولية'),
                              ('6', 'خلية إدارة التمويلات'),
                              ('7', 'مستشار نائب المدير العام المكلف بالاستشراف التجاري'),
                              ('8', 'خلية التحصيل الودي و الجبري'),
                              ('9', 'نائب المدير العام'),
                              ('10', 'لجنة التسهيلات'),
                              ('11', 'طور تبليغ المتعامل'),
                              ], default='1', string='وضعية الملف')
    #demande = fields.Many2one('wk.type.demande', string='الطلب', required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    raison_refus = fields.Text(string='سبب طلب المراجعة')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    chiffre_affaire = fields.Monetary(string='راس المال الحالي KDA', currency_field='currency_id',related='nom_client.chiffre_affaire')
    chiffre_affaire_creation = fields.Monetary(string='راس المال التاسيسي KDA', currency_field='currency_id',related='nom_client.chiffre_affaire_creation')
    montant_demande = fields.Float(string='المبلغ المطلوب')
    active = fields.Boolean(default=True)
    workflow_old = fields.Many2one('wk.workflow.dashboard', string='ملف سابق',)
    explanation = fields.Text(string='الغرض من الطلب')
    lanced = fields.Boolean(string='Traitement lancé', compute='compute_visible_states')
    plan_ids = fields.One2many('wk.ponctuel.charge', 'ponctuel_id')
    nom_client = fields.Many2one('res.partner', string='اسم المتعامل',
                                 domain=lambda self: [('branche', '=', self.env.user.partner_id.branche.id),
                                                      ('is_client', '=', True)], )
    branche = fields.Many2one('wk.agence', string='الفرع', related='nom_client.branche')
    num_compte = fields.Char(string='رقم الحساب', related='nom_client.num_compte', store=True)
    demande = fields.Many2one('wk.type.demande', string='الطلب',)
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
    #images = fields.One2many('wk.documents', 'ponctuel_id', string='الصور المرفقة')
    forme_jur = fields.Many2one('wk.forme.jur', string='الشكل القانوني', related='nom_client.forme_jur')
    states = fields.One2many('wk.etape.ponctuel', 'workflow', string='المديريات')

    documents = fields.One2many('wk.document.check', 'ponctuel_id', string='التاكد من الوثائق المرفقة')

    kyc = fields.One2many('wk.kyc.details', 'ponctuel_id')
    apropos = fields.One2many('wk.partenaire', 'ponctuel_id', string='نبذة عن المتعامل')
    gestion = fields.One2many('wk.gestion', 'ponctuel_id', string='فريق التسيير')
    #employees = fields.One2many('wk.nombre.employee', 'ponctuel_id', string='عدد العمال (حسب الفئة المهنية)')
    #sieges = fields.One2many('wk.siege', 'ponctuel_id', string='مقرات تابعة للشركة')
    tailles = fields.One2many('wk.taille', 'ponctuel_id', string='حجم و هيكل التمويلات المطلوبة')
    situations = fields.One2many('wk.situation', 'ponctuel_id', string='التمويل لدى البنوك الاخرى')
    situations_fin = fields.One2many('wk.situation.fin', 'ponctuel_id',
                                     string='البيانات المالية المدققة للثلاث سنوات الأخيرة KDA')

    fournisseur = fields.One2many('wk.fournisseur', 'ponctuel_id', string='الموردين')
    client = fields.One2many('wk.client', 'ponctuel_id', string='الزبائن')
    companies = fields.One2many('wk.companies', 'ponctuel_id')

    avis_conseil = fields.Text('راي المكلف بالملف')
    recommendation_agence = fields.Text('توصية مدير الفرع')

    assigned_to_commercial = fields.Many2one('res.users', string='المكلف بالاعمال التجارية',
                                             domain=lambda self: [
                                                 ('groups_id', 'in',
                                                  self.env.ref('dept_wk.dept_wk_group_charge_commercial').id)],
                                             track_visibility='always')

    taux_change = fields.Float(string='1$ = ?DA: سعر الصرف', default=1)
    facilite_accorde = fields.One2many('wk.facilite.accorde', 'ponctuel_id',
                                       string='تفاصيل التسهيلات الممنوحة (KDA)')
    detail_garantie_actuel_ids = fields.One2many('wk.detail.garantie', 'ponctuel_id', string='الضمانات العقارية الحالية')
    garantie_actuel_comment = fields.Text(string='تعليق')
    detail_garantie_propose_ids = fields.One2many('wk.detail.garantie.propose', 'ponctuel_id',
                                                  string='الضمانات العقارية المقترحة')
    garantie_propose_comment = fields.Text(string='تعليق')
    garantie_conf = fields.One2many('wk.garantie.conf', 'ponctuel_id',
                                    string='الشروط السابقة/المقترحة و الموافق عليها من لجان التمويل')
    garantie_fin = fields.One2many('wk.garantie.fin', 'ponctuel_id', string='الشروط المالية')
    garantie_autres = fields.One2many('wk.garantie.autres', 'ponctuel_id', string='الشروط الاخرى')
    risque_central = fields.One2many('wk.risque.line', 'ponctuel_id', string='مركزية المخاطر')
    compute_risque = fields.Float(string='compute field', compute='compute_risk')
    risque_date = fields.Date(string='مركزية المخاطر بتاريخ')
    nbr_banque = fields.Integer(string='عدد البنوك المصرحة')
    comment_risk_central = fields.Text(string='تعليق')
    capture_filename = fields.Char(default='ملف مركزية المخاطر')
    risk_capture = fields.Binary(string='ملف مركزية المخاطر')
    position_tax = fields.One2many('wk.position', 'ponctuel_id', string='الوضعية الجبائية والشبه جبائية')
    mouvement = fields.One2many('wk.mouvement', 'ponctuel_id',
                                string='الحركة والأعمال الجانبية للحساب مع مصرف السلام الجزائر (KDA)')
    detail_mouvement = fields.Text(string='التوطين البنكي')

    companies_fisc = fields.One2many('wk.companies.fisc', 'ponctuel_id')
    comment_fisc = fields.Text(string='تعليق')
    visualisation2 = fields.Binary(string='visualisation')

    facitlite_existante = fields.One2many('wk.facilite.existante', 'ponctuel_id')

    mouvement_group = fields.One2many('wk.mouvement.group', 'ponctuel_id',
                                      string='الحركة والأعمال الجانبية للمجموعة مع مصرف السلام الجزائر (KDA)')
    tcr_id = fields.Many2one('import.ocr.tcr', string='TCR')
    passif_id = fields.Many2one('import.ocr.passif', string='Passif')
    actif_id = fields.Many2one('import.ocr.actif', string='Actif')
    bilan_id = fields.One2many('wk.bilan', 'ponctuel_id')
    bilan1_id = fields.One2many('wk.bilan.cat1', 'ponctuel_id')
    comment_cat1 = fields.Text(string='تعليق')
    bilan2_id = fields.One2many('wk.bilan.cat2', 'ponctuel_id')
    comment_cat2 = fields.Text(string='تعليق')
    bilan3_id = fields.One2many('wk.bilan.cat3', 'ponctuel_id')
    comment_cat3 = fields.Text(string='تعليق')
    bilan4_id = fields.One2many('wk.bilan.cat4', 'ponctuel_id')
    comment_cat4 = fields.Text(string='تعليق')
    bilan5_id = fields.One2many('wk.bilan.cat5', 'ponctuel_id')
    comment_cat5 = fields.Text(string='تعليق')
    comment_bilan = fields.Text(string='تعليق')
    analyse_secteur_act = fields.Text(string='تحليل قطاع عمل العميل')
    analyse_concurrence = fields.Text(string='تحليل المنافسة')
    ampleur_benefice = fields.Float(string='حجم الارباح PNB المتوقعة')
    analyse_relation = fields.Text(string='تحليل اهمية العلاقة على المدى المتوسط')
    recap_ids = fields.One2many('wk.recap', 'ponctuel_id')
    var_ids = fields.One2many('wk.variable', 'ponctuel_id')
    weakness_ids = fields.One2many('wk.swot.weakness', 'ponctuel_id')
    strength_ids = fields.One2many('wk.swot.strength', 'ponctuel_id')
    threat_ids = fields.One2many('wk.swot.threat', 'ponctuel_id')
    opportunitie_ids = fields.One2many('wk.swot.opportunitie', 'ponctuel_id')

    comite = fields.Many2one('wk.comite', string='اللجنة')
    recommandation_dir_fin = fields.Text(string='راي مدير ادارة التمويلات', track_visibility='always')
    facilite_propose = fields.One2many('wk.facilite.propose', 'ponctuel_id', string='التسهيلات المقترحة')
    garantie_ids = fields.Many2many('wk.garanties', string='الضمانات المقترحة')
    garanties_demande_ids = fields.Many2many('wk.garanties', 'garantie_precedente_rel', string='الضمانات')
    exception_ids = fields.Many2many('wk.exception', string='الاستثناءات مع سياسة الائتمان')
    risk_scoring = fields.Many2one('risk.scoring', string='إدارة المخاطر')

    annee_fiscal = fields.Integer(string='السنة المالية N', compute='change_annee',)
    recommendation_1 = fields.Text(string='توصية مدير إدارة الاعمال التجارية')
    recommendation_2 = fields.Text(string='توصية مدير  إدارة  الدراسات الائتمانية للمؤسسات')
    recommendation_3 = fields.Text(string='توصية رئيس  خلية إدارة المخاطر')
    recommendation_4 = fields.Text(string='توصية رئيس قطاع  الخزينة و العمليات المحلية و الدولية')
    recommendation_5 = fields.Text(string='توصية رئيس خلية إدارة التمويلات')
    recommendation_6 = fields.Text(string='توصية مستشار نائب المدير العام المكلف بالاستشراف التجاري')
    recommendation_7 = fields.Text(string='توصية رئيس خلية التحصيل الودي و الجبري')
    recommendation_8 = fields.Text(string='توصية نائب المدير العام')
    recommendation_9 = fields.Text(string='قرار لجنة التسهيلات')

    def compute_visible_states(self):
        for rec in self:
            if rec.states:
                rec.lanced = True
            else:
                rec.lanced = False
    def relance(self):
        for rec in self:
            #view_id = self.env.ref('dept_comm.confirmation_mail_send_form').id
            template = self.env.ref('dept_comm.email_template_ponctuel')
            return {
                'name': _("تاكيد"),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'confirmation.mail.send',
                'target': 'new',
                'context': {
                    'relance': True,
                    'default_folder_id': rec.id,
                    'default_mail_template_id': template.id,
                },
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
                rec.bilan_id.filtered(lambda l: l.declaration == 'السنة').write({
                    'year_1': rec.annee_fiscal - 3,
                    'year_2': rec.annee_fiscal - 2,
                    'year_3': rec.annee_fiscal - 1,
                    'year_4': rec.annee_fiscal, })


    """@api.depends('states')
    def compute_state(self):
        print('exec')
        for rec in self:
            exist = rec.states.filtered(lambda l:l.sequence == 3)
            if exist:
                rec.is_in_risk = True
            else:
                rec.is_in_risk = False

    @api.depends('states')
    def compute_state_comm(self):
        print('exec')
        for rec in self:
            exist = rec.states.filtered(lambda l:l.sequence == 4)
            if exist:
                rec.is_in_comm = True
            else:
                rec.is_in_comm = False

    def is_same_compute(self):
        for rec in self:
            if self.env.user.partner_id.branche:
                if self.env.user.partner_id.branche == rec.branche:
                    print(True)
                    rec.is_same = True
                    rec.is_same_branche = True
                else:
                    rec.is_same = False
                    rec.is_same_branche = False
            else:
                rec.is_same = False
                rec.is_same_branche = False


    def compute_type_demande(self):
        for rec in self:
            self.is_same_compute()
            if rec.demande.name == 'تسهيلات جديدة':
                rec.is_new = True
                rec.is_renew = rec.is_modify = rec.is_delete = rec.is_condition = False
            elif rec.demande.name == 'تجديد التسهيلات':
                rec.is_renew = True
                rec.is_new = rec.is_modify = rec.is_delete = rec.is_condition = False
            elif rec.demande.name == 'تعديل التسهيلات':
                rec.is_modify = True
                rec.is_new = rec.is_renew = rec.is_delete = rec.is_condition = False
            elif rec.demande.name == 'الغاء تسهيلات':
                rec.is_delete = True
                rec.is_new = rec.is_modify = rec.is_renew = rec.is_condition = False
            elif rec.demande.name == 'تعديل الشروط':
                rec.is_condition = True
                rec.is_new = rec.is_modify = rec.is_delete = rec.is_renew = False
            else:
                rec.is_new = rec.is_condition = rec.is_modify = rec.is_delete = rec.is_renew = False

    def compute_visible_states(self):
        for rec in self:
            print('not scoring')
            print(rec.risk_scoring)
            if not rec.risk_scoring:
                print('not scoring')
                rec.risk_scoring = rec.states.filtered(lambda l:l.sequence == 1).risk_scoring
            if rec.state == '2':
                rec.is_in_financial = True
            else:
                rec.is_in_financial = False
            if rec.states:
                rec.lanced = True
            else:
                rec.lanced = False

        """

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('wk.credit.ponctuel') or _('New')
        res = super(Ponctuel, self).create(vals)
        for item in List_items:
            line = self.env['wk.kyc.details'].create({'info': item, 'ponctuel_id': res.id})
        """for item in list_poste:
            line = self.env['wk.nombre.employee'].create({'name': item,
                                                          'ponctuel_id': res.id})
        for item in list_siege:
            line = self.env['wk.siege'].create({'name': item,
                                                'ponctuel_id': res.id})"""
        count = 0
        for item in list_situation:
            line = self.env['wk.situation.fin'].create({'type': item,
                                                        'sequence': count,
                                                        'ponctuel_id': res.id})
            count += 1
        res.situations_fin.filtered(lambda l: l.sequence == 0).write({
            'year1': res.annee_fiscal,
            'year2': res.annee_fiscal - 1,
            'year3': res.annee_fiscal - 2,
        })
        for item in list_garantie:
            line = self.env['wk.garantie.conf'].create({'info': item, 'ponctuel_id': res.id})
        for item in list_garantie_fisc:
            line = self.env['wk.garantie.fin'].create({'info': item, 'ponctuel_id': res.id})
        for item in list_autre_term:
            line = self.env['wk.garantie.autres'].create({'info': item, 'ponctuel_id': res.id})
        for item in List_risque:
            line = self.env['wk.risque.line'].create({'declaration': item, 'ponctuel_id': res.id})
        for item in List_position:
            line = self.env['wk.position'].create({'name': item, 'ponctuel_id': res.id})
        count = 0
        for item in list_mouvement:
            line = self.env['wk.mouvement'].create({'mouvement': item,
                                                    'ponctuel_id': res.id,
                                                    'sequence': count})
            count += 1
        res.mouvement.filtered(lambda l: l.sequence == 0).write({
            'n_dz': res.annee_fiscal,
            'n1_dz': res.annee_fiscal - 1,
            'n2_dz': res.annee_fiscal - 2,
            'n3_dz': res.annee_fiscal - 3,
        })
        self.env['wk.mouvement.group'].create({'company': 'السنة',
                                               'ponctuel_id': res.id,
                                               'n_dz': res.annee_fiscal,
                                               'n1_dz': res.annee_fiscal - 1,
                                               'n2_dz': res.annee_fiscal - 2,
                                               'sequence': 0})
        count = 0
        for item in list_fisc:
            line = self.env['wk.companies.fisc'].create({'declaration': item,
                                                         'sequence': count,
                                                         'ponctuel_id': res.id})
            count += 1
        res.companies_fisc.filtered(lambda l: l.sequence == 0).write({
            'year_4': res.annee_fiscal,
            'year_3': res.annee_fiscal - 1,
            'year_2': res.annee_fiscal - 2,
            'year_1': res.annee_fiscal - 3,
        })
        count = 1
        line = self.env['wk.bilan'].create({'declaration': 'السنة',
                                            'ponctuel_id': res.id,
                                            'sequence': 0})

        for index, item in list_bil:
            line = self.env['wk.bilan'].create({'declaration': item,
                                                'ponctuel_id': res.id,
                                                'sequence': index})
            count += 1
        count = 1
        for item in list_recap:
            line = self.env['wk.recap'].create({'declaration': item, 'ponctuel_id': res.id, 'sequence': count})
            count += 1
        count = 1
        for item in list_var:
            line = self.env['wk.variable'].create({'var': item, 'ponctuel_id': res.id, 'sequence': count})
            count += 1
        scoring = self.env['risk.scoring'].create({
            'partner_id': res.nom_client.id,
            'ponctuel_id': res.id
        })
        self.env['wk.tracking.ponctuel'].create({'ponctuel_id': res.id,
                                                 'state': '1',
                                                 'date_debut': fields.Date.today(),
                                                 'is_revision': False,
                                                 'comment': False})
        res.risk_scoring = scoring.id
        return res

    def action_open_risk(self):
        for rec in self:
            view_id = self.env.ref('dept_comm.scoring_inherit_view_form').id
            if not rec.risk_scoring:
                scoring = self.env['risk.scoring'].create({
                    'partner_id': rec.nom_client.id,
                    'ponctuel_id': rec.id
                })
                rec.risk_scoring = scoring.id
            return {
                'name': 'ادارة المخاطر',
                'res_model': 'risk.scoring',
                'view_mode': 'form',
                'res_id': rec.risk_scoring.id,
                'view_id': view_id,
                'type': 'ir.actions.act_window',
            }

    def open_messages(self):
        for rec in self:
            view_id = self.env.ref('mail.view_message_tree').id
            return {
                'name': "Messages",
                'res_model': 'mail.message',
                'view_mode': 'tree',
                'view_id': view_id,
                'domain': [('res_id', 'in', [rec.id]),
                           ('message_type', '=', 'comment'),
                           ('model', 'in', ['wk.workflow.ponctuel'])],
                'type': 'ir.actions.act_window',
            }

    def action_start(self):
        for rec in self:
            states = rec.workflow_old.states.filtered(lambda l: l.sequence in [1, 2])
            for etape in states:
                vals = get_values(rec, etape)
                vals['workflow'] = rec.id
                etape_new = self.env['wk.etape.ponctuel'].create(vals)
                vals.pop('etape')
                vals.pop('workflow')
                rec.write(vals)
                get_lists(self, rec, etape_new, etape)

    def open_tracking(self):
        self.ensure_one()
        view_id = self.env.ref('dept_comm.view_wk_tracking_tree').id
        return {
                'name': "تتبع",
                'res_model': 'wk.tracking.ponctuel',
                'view_mode': 'tree',
                'view_id': view_id,
                'domain': [('ponctuel_id', '=', self.id)],
                'type': 'ir.actions.act_window',
                'context': {'create': False,
                            'edit': False,
                            'delete': False},
            }

    def get_data_t24(self):
        for rec in self:
            print('hiio')

    def get_data(self):
        for rec in self:
            if not rec.states:
                rec.env['wk.etape.ponctuel'].create({
                    'workflow': rec.id,
                    'etape': self.env.ref('dept_comm.principe_1').id,
                    'nom_client': rec.nom_client
                })

    def _get_partner(self):
        for rec in self:
            group = self.env.ref('dept_comm.dept_comm_group_responsable_commercial')
            partner_ids = group.users
            return partner_ids

    def validate_information(self):
        for rec in self:
            #view_id = self.env.ref('dept_comm.confirmation_mail_send_form').id
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
                    'default_folder_id': rec.id,
                    'default_mail_template_id': template.id,
                },
            }

    def validate_information_function(self):
        for rec in self:
            last_state = int(rec.state)
            actuel_state = int(rec.state) + 1
            rec.state = str(actuel_state)
            rec.raison_refus = False
            last_track = self.env['wk.tracking.ponctuel'].search([('ponctuel_id', '=', rec.id),
                                                                  ('state', '=', last_state)])
            if last_track:
                last_track.date_fin = fields.Date.today()
            self.env['wk.tracking.ponctuel'].create({'ponctuel_id': rec.id,
                                            'state': rec.state,
                                            'date_debut': fields.Date.today(),
                                            'is_revision': True if rec.raison_refus else False,
                                            'comment': False})
            if actuel_state == '11':
                rec.date_fin = fields.Date.today()

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
                'context': {'default_ponctuel_id': rec.id,
                            'default_state': rec.state}
            }


def get_values(workflow, etape):
    if etape.sequence == 1:
        return {
            'etape': etape.env.ref('dept_comm.principe_1').id,
            'nom_client': etape.nom_client.id,
            'branche': etape.branche.id,
            'num_compte': etape.num_compte,
            'gerant': etape.gerant.id,
            'unit_prod': etape.unit_prod,
            'stock': etape.stock,
            'prod_company': etape.prod_company,
            'politique_comm': etape.politique_comm,
            'cycle_exploit': etape.cycle_exploit,
            'concurrence': etape.concurrence,
            'program_invest': etape.program_invest,
            'annee_fiscal_list': etape.annee_fiscal_list.id,
            'description_company': etape.description_company,
        }
    elif etape.sequence == 2:
        return {
            'etape': etape.env.ref('dept_comm.principe_2').id,
            'taux_change': etape.taux_change,
            'annee_fiscal': etape.annee_fiscal,
            'risque_date': etape.risque_date,
            'nbr_banque': etape.nbr_banque,
            'comment_risk_central': etape.comment_risk_central,
            'capture_filename': etape.capture_filename,
            'risk_capture': etape.risk_capture,
            'garanties_demande_ids': etape.garantie_ids.ids,
            'annee_fiscal_list': etape.annee_fiscal_list.id,
        }
    elif etape.sequence == 4:
        return {
            'analyse_secteur_act': etape.analyse_secteur_act,
            'analyse_concurrence': etape.analyse_concurrence,
            'ampleur_benefice': etape.ampleur_benefice,
            'analyse_relation': etape.analyse_relation,
        }


def get_lists(self, etape_new,step , etape_old):
    if etape_old.sequence == 1:
        etape_new.kyc.unlink()
        etape_new.apropos.unlink()
        etape_new.gestion.unlink()
        etape_new.situations.unlink()
        etape_new.situations_fin.unlink()
        etape_new.client.unlink()
        etape_new.fournisseur.unlink()
        step.kyc.unlink()
        step.apropos.unlink()
        step.gestion.unlink()
        step.situations.unlink()
        step.situations_fin.unlink()
        step.client.unlink()
        step.fournisseur.unlink()
        #etape_new.companies_fisc.unlink()
        for kyc in etape_old.kyc:
            self.env['wk.kyc.details'].create({'info': kyc.info,
                                               'answer': kyc.answer,
                                               'detail': kyc.detail,
                                               'ponctuel_id': etape_new.id,
                                               'step_id': step.id,
                                               })
        for a in etape_old.apropos:
            self.env['wk.partenaire'].create({'nom_partenaire': a.nom_partenaire,
                                              'age': a.age,
                                              'pourcentage': a.pourcentage,
                                              'statut_partenaire': a.statut_partenaire,
                                              'nationalite': a.nationalite.id,
                                              'ponctuel_id': etape_new.id,
                                              'step_id': step.id,
                                              })
        for g in etape_old.gestion:
            self.env['wk.gestion'].create({
                'name': g.name,
                'job': g.job,
                'niveau_etude': g.niveau_etude,
                'age': g.age,
                'experience': g.experience,
                'ponctuel_id': etape_new.id,
                'step_id': step.id,
            })
        """for empl in etape_old.employees:
            self.env['wk.nombre.employee'].create({
                'name': empl.name,
                'poste_permanent': empl.poste_permanent,
                'poste_non_permanent': empl.poste_non_permanent,
                'ponctuel_id': etape_new.id
            })
        for siege in etape_old.sieges:
            self.env['wk.siege'].create({
                'name': siege.name,
                'adresse': siege.adresse,
                'nature': siege.nature.id,
                'ponctuel_id': etape_new.id
            })"""
        for sit in etape_old.situations:
            self.env['wk.situation'].create({
                'banque': sit.banque.id,
                'type_fin': sit.type_fin.id,
                'montant': sit.montant,
                'garanties': sit.garanties,
                'ponctuel_id': etape_new.id,
                'step_id': step.id,
            })
        for sit in etape_old.situations_fin:
            self.env['wk.situation.fin'].create({
                'type': sit.type,
                'sequence': sit.sequence,
                'year1': sit.year1,
                'year2': sit.year2,
                'year3': sit.year3,
                'ponctuel_id': etape_new.id,
                'step_id': step.id,
            })
        for client in etape_old.client:
            self.env['wk.client'].create({
                'name': client.name,
                'country': client.country.id,
                'type_payment': client.type_payment.ids,
                'ponctuel_id': etape_new.id,
                'step_id': step.id,
            })
        for f in etape_old.fournisseur:
            self.env['wk.fournisseur'].create({
                'name': f.name,
                'country': f.country.id,
                'type_payment': f.type_payment.ids,
                'ponctuel_id': etape_new.id,
                'step_id': step.id,
            })
    elif etape_old.sequence == 2:
        etape_new.detail_garantie_actuel_ids.unlink()
        etape_new.detail_garantie_propose_ids.unlink()
        etape_new.garantie_conf.unlink()
        etape_new.garantie_fin.unlink()
        etape_new.garantie_autres.unlink()
        etape_new.risque_central.unlink()
        etape_new.position_tax.unlink()
        etape_new.companies.unlink()
        etape_new.bilan_id.unlink()
        etape_new.bilan1_id.unlink()
        etape_new.bilan2_id.unlink()
        etape_new.bilan3_id.unlink()
        etape_new.bilan4_id.unlink()
        etape_new.bilan5_id.unlink()
        #etape_new.companies_fisc.unlink()
        etape_new.mouvement_group.unlink()
        etape_new.recap_ids.unlink()
        etape_new.var_ids.unlink()
        etape_new.weakness_ids.unlink()
        etape_new.strength_ids.unlink()
        etape_new.threat_ids.unlink()
        etape_new.opportunitie_ids.unlink()
        etape_new.facilite_propose.unlink()
        etape_new.facilite_accorde.unlink()
        step.detail_garantie_actuel_ids.unlink()
        step.detail_garantie_propose_ids.unlink()
        step.garantie_conf.unlink()
        step.garantie_fin.unlink()
        step.garantie_autres.unlink()
        step.risque_central.unlink()
        step.position_tax.unlink()
        step.companies.unlink()
        step.bilan_id.unlink()
        step.bilan1_id.unlink()
        step.bilan2_id.unlink()
        step.bilan3_id.unlink()
        step.bilan4_id.unlink()
        step.bilan5_id.unlink()
        #step.companies_fisc.unlink()
        step.mouvement_group.unlink()
        step.recap_ids.unlink()
        step.var_ids.unlink()
        step.weakness_ids.unlink()
        step.strength_ids.unlink()
        step.threat_ids.unlink()
        step.opportunitie_ids.unlink()
        step.facilite_propose.unlink()
        step.facilite_accorde.unlink()
        for doc in etape_old.detail_garantie_actuel_ids:
            self.env['wk.detail.garantie'].create({'type_garantie': doc.type_garantie.id,
                  'type_contrat': doc.type_contrat.id,
                  'montant': doc.montant,
                  'date': doc.date,
                  'recouvrement': doc.recouvrement,
                  'niveau': doc.niveau,
                  'ponctuel_id': etape_new.id,
                  'step_id': step.id,})
        for doc in etape_old.detail_garantie_propose_ids:
            self.env['wk.detail.garantie.propose'].create({'type_garantie': doc.type_garantie.id,
                  'type_contrat': doc.type_contrat.id,
                  'montant': doc.montant,
                  'date': doc.date,
                  'recouvrement': doc.recouvrement,
                  'niveau': doc.niveau,
                  'ponctuel_id': etape_new.id,
                  'step_id': step.id,})
        for doc in etape_old.garantie_conf:
            self.env['wk.garantie.conf'].create({'info': doc.info,
                  'answer': doc.answer,
                  'detail': doc.detail,
                  'ponctuel_id': etape_new.id,
                                                 'step_id': step.id,})
        for doc in etape_old.garantie_fin:
            self.env['wk.garantie.fin'].create({'info': doc.info,
                  'answer': doc.answer,
                  'detail': doc.detail,
                  'ponctuel_id': etape_new.id,'step_id': step.id,})
        for doc in etape_old.garantie_autres:
            self.env['wk.garantie.autres'].create({'info': doc.info,
                  'answer': doc.answer,
                  'detail': doc.detail,
                  'ponctuel_id': etape_new.id,'step_id': step.id,})
        for doc in etape_old.risque_central:
            self.env['wk.risque.line'].create({'declaration': doc.declaration,
                  'montant_esalam_dz_donne': doc.montant_esalam_dz_donne,
                  'montant_esalam_dz_used': doc.montant_esalam_dz_used,
                  'montant_other_dz_donne': doc.montant_esalam_dz_used,
                  'montant_other_dz_used': doc.montant_esalam_dz_used,
                  'ponctuel_id': etape_new.id,
                  'step_id': step.id,})
        for doc in etape_old.position_tax:
            self.env['wk.position'].create({'name': doc.name,
                  'adversite': doc.adversite,
                  'non_adversite': doc.non_adversite,
                  'notes': doc.notes,
                  'ponctuel_id': etape_new.id,
                  'step_id': step.id,})
        for doc in etape_old.companies:
            self.env['wk.companies'].create({'name': doc.name,
                  'date_creation': doc.date_creation,
                  'activite': doc.activite.id,
                  'chiffre_affaire': doc.chiffre_affaire,
                  'n1_num_affaire': doc.n1_num_affaire,
                  'n_num_affaire': doc.n_num_affaire,
                  'ponctuel_id': etape_new.id,
                                             'step_id': step.id,})
        """for doc in etape_old.companies_fisc:
            self.env['wk.companies.fisc'].create({'declaration': doc.declaration,
                  'sequence': doc.sequence,
                  'year_1': doc.year_1,
                  'year_2': doc.year_2,
                  'year_3': doc.year_3,
                  'year_4': doc.year_4,
                  'variante': doc.variante,
                  'remark': doc.remark,
                  'ponctuel_id': etape_new.id})"""
        for doc in etape_old.mouvement_group:
            self.env['wk.mouvement.group'].create({'company': doc.company,
                                                      'sequence': doc.sequence,
                                                      'n2_dz': doc.n2_dz,
                                                      'n1_dz': doc.n1_dz,
                                                      'n_dz': doc.n_dz,
                                                      'remarques': doc.remarques,
                                                      'ponctuel_id': etape_new.id,
                                                   'step_id': step.id})
        for doc in etape_old.recap_ids:
            self.env['wk.recap'].create({'declaration': doc.declaration,
                  'sequence': doc.sequence,
                  'montant': doc.montant,
                  'ponctuel_id': etape_new.id,
                  'step_id': step.id})
        for doc in etape_old.var_ids:
            self.env['wk.variable'].create({'var': doc.var,
                  'sequence': doc.sequence,
                  'montant': doc.montant,
                  'ponctuel_id': etape_new.id,'step_id': step.id})
        for doc in etape_old.weakness_ids:
            self.env['wk.swot.weakness'].create({'name': doc.name,
                  'ponctuel_id': etape_new.id,
                                                 'step_id': step.id})
        for doc in etape_old.strength_ids:
            self.env['wk.swot.strength'].create({'name': doc.name,
                  'ponctuel_id': etape_new.id,'step_id': step.id})
        for doc in etape_old.threat_ids:
            self.env['wk.swot.threat'].create({'name': doc.name,
                  'ponctuel_id': etape_new.id,'step_id': step.id})
        for doc in etape_old.opportunitie_ids:
            self.env['wk.swot.opportunitie'].create({'name': doc.name,
                                                     'ponctuel_id': etape_new.id,'step_id': step.id,})
        for doc in etape_old.facilite_propose:
            self.env['wk.facilite.accorde'].create({'type_demande_ids': doc.type_demande_ids.ids,
                                                    'montant_da_demande': doc.montant_dz,
                                                    'garantie_montant': doc.preg,
                                                    'remarques': doc.condition,
                                                    'ponctuel_id': etape_new.id,'step_id': step.id,
                                                    })

        vals = {'ponctuel_id': etape_new.id,
                'step_id': step.id,
                'sequence': 0,
                'declaration': 'السنة',
                'year_1': etape_new.annee_fiscal - 3,
                'year_2': etape_new.annee_fiscal - 2,
                'year_3': etape_new.annee_fiscal - 1,
                'year_4': etape_new.annee_fiscal,
                }
        self.env['wk.bilan.cat1'].create(vals)
        self.env['wk.bilan.cat2'].create(vals)
        self.env['wk.bilan.cat3'].create(vals)
        self.env['wk.bilan.cat4'].create(vals)
        self.env['wk.bilan.cat5'].create(vals)
        for doc in etape_old.bilan_id:
            self.env['wk.bilan'].create({
                'ponctuel_id': etape_new.id,
                'step_id': step.id,
                'bilan_id': doc.id,
                'sequence': doc.sequence,
                'categorie': doc.categorie,
                'declaration': doc.declaration,
                'year_1': doc.year_1,
                'year_2': doc.year_2,
                'year_3': doc.year_3,
                'year_4': doc.year_4,
                'is_null_4': doc.is_null_4,
                'is_null_3': doc.is_null_3,
                'is_null_2': doc.is_null_2,
                'is_null_1': doc.is_null_1,
                'variante': doc.variante,
            })
        print(etape_new.bilan_id)