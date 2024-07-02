import base64
from odoo import api, fields, models, tools, _, Command
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang


class ConfirmationDemandeCreditSend(models.TransientModel):
    _name = 'confirmation.mail.send'
    _description = "Confirmation Demande Credit Send"

    company_id = fields.Many2one(comodel_name='res.company', compute='_compute_company_id', store=True)
    demande_credit_ids = fields.Many2many(comodel_name='wk.workflow.ponctuel')
    folder_id = fields.Many2one(comodel_name='wk.workflow.ponctuel')
    step_id = fields.Many2one(comodel_name='wk.etape.ponctuel')

    # == PRINT ==
    enable_download = fields.Boolean(compute='_compute_enable_download')
    checkbox_download = fields.Boolean(
        string="Download",
        compute='_compute_checkbox_download',
        store=True,
        readonly=False,
    )

    # == MAIL ==
    enable_send_mail = fields.Boolean(compute='_compute_enable_send_mail')
    checkbox_send_mail = fields.Boolean(
        string="Email",
        compute='_compute_checkbox_send_mail',
        store=True,
        readonly=False,
    )
    mail_template_id = fields.Many2one(
        comodel_name='mail.template',
        string="استخدم هذا النموذج",
        domain="[('model', '=', 'wk.workflow.ponctuel')]",
    )
    mail_lang = fields.Char(
        string="Lang",
        compute='_compute_mail_lang',
    )
    mail_partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string="Destinataires",
        compute='_compute_mail_partner_ids',
        store=True,
        readonly=False,
    )
    mail_subject = fields.Char(
        string="موضوع",
        compute='_compute_mail_subject_body',
        store=True,
        readonly=False,
    )
    mail_body = fields.Html(
        string="المحتوى",
        sanitize_style=True,
        compute='_compute_mail_subject_body',
        store=True,
        readonly=False,
    )
    '''mail_attachments_widget = fields.Json(
        compute='_compute_mail_attachments_widget',
        store=True,
        readonly=False,
    )
'''
    @api.model
    def _get_mail_default_field_value_from_template(self, mail_template, lang, demande_credit, field, **kwargs):
        if not mail_template:
            return
        return mail_template\
            .with_context(lang=lang)\
            ._render_field(field, demande_credit.ids, **kwargs)[demande_credit._origin.id]

    def _get_default_mail_lang(self, demande_credit, mail_template=None):
        return mail_template._render_lang([demande_credit.id]).get(demande_credit.id) if mail_template else get_lang(self.env).code

    def _get_default_mail_body(self, demande_credit, mail_template, mail_lang):
        return self._get_mail_default_field_value_from_template(
            mail_template,
            mail_lang,
            demande_credit,
            'body_html',
            options={'post_process': True},
        )

    def _get_default_mail_subject(self, demande_credit, mail_template, mail_lang):
        return self._get_mail_default_field_value_from_template(
            mail_template,
            mail_lang,
            demande_credit,
            'subject',
        )

    def _get_default_mail_partner_ids(self, demande_credit, mail_template, mail_lang):
        partners = self.env['res.partner'].with_company(demande_credit.company_id)
        if mail_template.email_to:
            for mail_data in tools.email_split(mail_template.email_to):
                partners |= partners.find_or_create(mail_data)
        if mail_template.email_cc:
            for mail_data in tools.email_split(mail_template.email_cc):
                partners |= partners.find_or_create(mail_data)
        if mail_template.partner_to:
            partner_to = self._get_mail_default_field_value_from_template(mail_template, mail_lang, demande_credit, 'partner_to')
            partner_ids = mail_template._parse_partner_to(partner_to)
            partners |= self.env['res.partner'].sudo().browse(partner_ids).exists()
        return partners

    def _get_default_mail_attachments_widget(self, demande_credit, mail_template):
       return self._get_placeholder_mail_attachments_data(demande_credit) \
            + self._get_mail_template_attachments_data(mail_template)

    def _get_wizard_values(self):
        self.ensure_one()
        return {
            'mail_template_id': self.mail_template_id.id,
            'download': self.checkbox_download,
            'send_mail': self.checkbox_send_mail,
        }

    def _get_mail_demande_credit_values(self, demande_credit, wizard=None):
        mail_template_id = demande_credit.send_and_print_values and demande_credit.send_and_print_values.get('mail_template_id')
        mail_template = wizard and wizard.mail_template_id or self.env['mail.template'].browse(mail_template_id)
        mail_lang = self._get_default_mail_lang(demande_credit, mail_template)

        return {
            'mail_template_id': mail_template,
            'mail_lang': mail_lang,
            'mail_body': wizard and wizard.mail_body or self._get_default_mail_body(demande_credit, mail_template, mail_lang),
            'mail_subject': wizard and wizard.mail_subject or self._get_default_mail_subject(demande_credit, mail_template, mail_lang),
            'mail_partner_ids': wizard and wizard.mail_partner_ids or self._get_default_mail_partner_ids(demande_credit, mail_template, mail_lang),
            #'mail_attachments_widget': wizard and wizard.mail_attachments_widget or self._get_default_mail_attachments_widget(demande_credit, mail_template),
        }

    def _get_placeholder_mail_attachments_data(self, demande_credit):
        #if demande_credit.credit_pdf_report_id:
        return []

        filename = demande_credit._get_credit_report_filename()
        return [{
            'id': f'placeholder_{filename}',
            'name': filename,
            'mimetype': 'application/pdf',
            'placeholder': True,
        }]

    """@api.model
    def _get_demande_credit_extra_attachments(self, demande_credit):
        #return demande_credit.credit_pdf_report_id
        return False"""


    """@api.model
    def _get_demande_credit_extra_attachments_data(self, demande_credit):

        return [
            {
                'id': attachment.id,
                'name': attachment.name,
                'mimetype': attachment.mimetype,
                'placeholder': False,
                'protect_from_deletion': True,
            }
            for attachment in self._get_demande_credit_extra_attachments(demande_credit)
        ]"""

    @api.model
    def _get_mail_template_attachments_data(self, mail_template):
        self.generate_and_attach_report()
        return [
            {
                'id': attachment.id,
                'name': attachment.name,
                'mimetype': attachment.mimetype,
                'placeholder': False,
                'mail_template_id': mail_template.id,
            }
            for attachment in mail_template.attachment_ids
        ]

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('demande_credit_ids')
    def _compute_company_id(self):
        for wizard in self:
            if len(wizard.demande_credit_ids.company_id) > 1:
                raise UserError(_("You can only send from the same company."))
            wizard.company_id = wizard.demande_credit_ids.company_id.id

    @api.depends('demande_credit_ids')
    def _compute_enable_download(self):
        for wizard in self:
            wizard.enable_download = bool(wizard.demande_credit_ids)

    @api.depends('enable_download')
    def _compute_checkbox_download(self):
        for wizard in self:
            wizard.checkbox_download = wizard.enable_download and wizard.company_id.invoice_is_download

    @api.depends('demande_credit_ids')
    def _compute_enable_send_mail(self):
        for wizard in self:
            wizard.enable_send_mail = bool(wizard.demande_credit_ids)

    @api.depends('enable_send_mail')
    def _compute_checkbox_send_mail(self):
        for wizard in self:
            wizard.checkbox_send_mail = wizard.company_id.invoice_is_email and not wizard.send_mail_readonly

    @api.depends('checkbox_send_mail')
    def _compute_mail_lang(self):
        for wizard in self:
            wizard.mail_lang = wizard.company_id.partner_id.lang or get_lang(self.env).code

    @api.depends('folder_id')
    def _compute_mail_partner_ids(self):
        for wizard in self:
                partners = self.env['res.partner']
                partners |= wizard.folder_id.partner_id
                wizard.mail_partner_ids = partners

    @api.depends('mail_template_id')
    def _compute_mail_subject_body(self):
        for wizard in self:
            demande_credit = wizard.folder_id
            mail_template = wizard.mail_template_id
            mail_lang = wizard.mail_lang
            wizard.mail_subject = self._get_default_mail_subject(demande_credit, mail_template, mail_lang)
            wizard.mail_body = self._get_default_mail_body(demande_credit, mail_template, mail_lang)

    @api.depends('folder_id')
    def _compute_mail_attachments_widget(self):
        for wizard in self:
            if wizard.folder_id:
                demande_credit = wizard.folder_id
                mail_template = wizard.mail_template_id
                wizard.mail_attachments_widget = self._get_default_mail_attachments_widget(demande_credit, mail_template)

    def action_send_and_print(self):
        self.ensure_one()
        email_template = self.mail_template_id
        email_template.send_mail(self.folder_id.id, force_send=True)
        print(self.env.context)
        if not self.env.context.get('relance'):
            self.folder_id.validate_information_function()
        if 'is_step' in self.env.context:
            if self.env.context.get('is_step'):
                self.step_id.validate_information_function()


class RevoirState(models.TransientModel):
    _name = "wk.ponctuel.retour"

    ponctuel_id = fields.Many2one("wk.workflow.ponctuel", string="Request")
    raison = fields.Text(string="Reason")
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

    def cancel(self):
        return {'type': 'ir.actions.act_window_close'}

    def send(self):
        for rec in self:
            actuel_state = int(rec.state) - 1
            rec.ponctuel_id.state = str(actuel_state)
            last_track = self.env['wk.tracking.ponctuel'].search([('ponctuel_id', '=', rec.ponctuel_id.id),
                                                                  ('state', '=', str(actuel_state + 1))],)[-1]

            if last_track:
                last_track.date_fin = fields.Date.today()
            rec.ponctuel_id.raison_refus = rec.raison
            self.env['wk.tracking.ponctuel'].create({'ponctuel_id': rec.ponctuel_id.id,
                                                     'state': str(actuel_state),
                                                     'date_debut': fields.Date.today(),
                                                     'is_revision': True if rec.raison else False,
                                                     'comment': False})


