from odoo import models, fields, api, _
import datetime


class DocChecker(models.Model):
    _inherit = 'wk.document.check'
    _description = ' check documents'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class KycDetail(models.Model):
    _inherit = 'wk.kyc.details'
    _description = 'Line KYC'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class Partenaire(models.Model):
    _inherit = 'wk.partenaire'
    _description = 'Partenaire du client'
    
    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class EquipeGestion(models.Model):
    _inherit = 'wk.gestion'
    _description = 'Equipe de gestion'
    
    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    
    
class Taillefin(models.Model):
    _inherit = 'wk.taille'
    _description = 'La taille et la structure du financement requis'
    
    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    

class SituationBancaire(models.Model):
    _inherit = 'wk.situation'
    _description = 'Situation bancaire et obligations envers autrui'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')

class SituationFinanciere(models.Model):
    _inherit = 'wk.situation.fin'
    _description = 'Situation financière'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    

class Fournisseur(models.Model):
    _inherit = 'wk.fournisseur'
    _description = 'fournisseur'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    

class Client(models.Model):
    _inherit = 'wk.client'
    _description = 'clients'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class Companies(models.Model):
    _inherit = 'wk.companies'
    _description = 'Companies in relation'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    

class FaciliteAccorde(models.Model):
    _inherit = 'wk.facilite.accorde'
    _description = 'Détails des facilités accordées'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    

class Detail(models.Model):
    _inherit = 'wk.detail.garantie'
    _description = 'Detail Garantie'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    

class DetailGarantiePropose(models.Model):
    _inherit = 'wk.detail.garantie.propose'
    _description = 'Detail Garantie'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    

class Ganrantie(models.Model):
    _inherit = 'wk.garantie.conf'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    
    
class GanrantieFin(models.Model):
    _inherit = 'wk.garantie.fin'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    

class GanrantieAutre(models.Model):
    _inherit = 'wk.garantie.autres'
    
    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    

class Risque(models.Model):
    _inherit = 'wk.risque.line'
    _description = 'Risque'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class PositionTax(models.Model):
    _inherit = 'wk.position'
    _description = 'Position taxonomique'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class MouvementAction(models.Model):
    _inherit = 'wk.mouvement'
    _description = 'Mouvement et Action'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class DeclarationFisc(models.Model):
    _inherit = 'wk.companies.fisc'
    _description = 'Companies fisc'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class FaciliteExistante(models.Model):
    _inherit = 'wk.facilite.existante'
    _description = 'Facilités existantes avec la banque'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class MouvementGroupe(models.Model):
    _inherit = 'wk.mouvement.group'
    _description = 'Mouvement et Action'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class TCR(models.Model):
    _inherit = 'import.ocr.tcr'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')

    @api.model
    def create(self, vals):
        if 'step_id' in self.env.context:
            vals['step_id'] = self.env.context.get('step_id')
        res = super(TCR, self).create(vals)
        if res.step_id:
            res.step_id.tcr_id = res.id
        return res


class Passif(models.Model):
    _inherit = 'import.ocr.passif'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')

    @api.model
    def create(self, vals):
        if 'step_id' in self.env.context:
            vals['step_id'] = self.env.context.get('step_id')
        res = super(Passif, self).create(vals)
        if res.step_id:
            res.step_id.passif_id = res.id
        return res


class Actif(models.Model):
    _inherit = 'import.ocr.actif'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')

    @api.model
    def create(self, vals):
        if 'step_id' in self.env.context:
            vals['step_id'] = self.env.context.get('step_id')
        res = super(Actif, self).create(vals)
        if res.step_id:
            res.step_id.actif_id = res.id
        return res

class BilanFisc(models.Model):
    _inherit = 'wk.bilan'
    _description = 'Bilan fiscal'
    _order = 'sequence,id'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    @api.model
    def create(self, vals):
        res = super(BilanFisc, self).create(vals)
        if 'bilan_id' in vals:
            vals.pop('bilan_id')
        if 'step_id' in vals:
            vals['bilan'] = res.id
            if res.categorie == '1':
                self.env['wk.bilan.cat1'].create(vals)
            if res.categorie == '2':
                self.env['wk.bilan.cat2'].create(vals)
            if res.categorie == '3':
                self.env['wk.bilan.cat3'].create(vals)
            if res.categorie == '4':
                self.env['wk.bilan.cat4'].create(vals)
            if res.categorie == '5':
                self.env['wk.bilan.cat5'].create(vals)
        return res


class BilanFisc1(models.Model):
    _inherit = 'wk.bilan.cat1'
    _description = 'Bilan fiscal'
    _order = 'sequence,id'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class BilanFisc2(models.Model):
    _inherit = 'wk.bilan.cat2'
    _description = 'Bilan fiscal'
    _order = 'sequence,id'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class BilanFisc3(models.Model):
    _inherit = 'wk.bilan.cat3'
    _description = 'Bilan fiscal'
    _order = 'sequence,id'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class BilanFisc4(models.Model):
    _inherit = 'wk.bilan.cat4'
    _description = 'Bilan fiscal'
    _order = 'sequence,id'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class BilanFisc5(models.Model):
    _inherit = 'wk.bilan.cat5'
    _description = 'Bilan fiscal'
    _order = 'sequence,id'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class Recap(models.Model):
    _inherit = 'wk.recap'
    _description = 'declaration'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class Variables(models.Model):
    _inherit = 'wk.variable'
    _description = 'variables'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class SwotWeakness(models.Model):
    _inherit = 'wk.swot.weakness'
    _description = 'swot matrice'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class SwotStrength(models.Model):
    _inherit = 'wk.swot.strength'
    _description = 'swot matrice'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class SwotThreats(models.Model):
    _inherit = 'wk.swot.threat'
    _description = 'swot matrice'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class SwotOpportunities(models.Model):
    _inherit = 'wk.swot.opportunitie'
    _description = 'swot matrice'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class FacilitePropose(models.Model):
    _inherit = 'wk.facilite.propose'
    _description = 'facilite propose'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class Scoring(models.Model):
    _inherit = 'risk.scoring'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel',
                                  string='Ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')


class Tracking(models.Model):
    _name = 'wk.tracking.ponctuel'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel',
                                  string='Ponctuel')
    step_id = fields.Many2one('wk.etape.ponctuel')
    date_debut = fields.Date(string='تاريخ البدء')
    date_fin = fields.Date(string='تاريخ الانتهاء')
    date_difference = fields.Char(string='الوقت المستغرق', compute='_compute_date')
    state = fields.Selection([('1', 'الفرع'),
                                ('2', 'الاعمال التجارية'),
                                ('3', 'مدير الدراسات الائتماني '),
                                ('4', 'رئيس خلية ادارة التمويلات'),
                                ('5', 'رئيس قطاع الخزينة ' ),
                                ('6', 'رئيس خلية ادارة المخاطر '),
                                ('7', 'مستشار نائب المدير العام المكلف بالاستشراف التجاري'),
                                ('8', 'نائب المدير العام'),
                                ('9', 'المدير العام'),
                                ('10','طور تبليغ المتعامل'),
                              ], string='حالة الملف')
    comment = fields.Text(string='التعليق')
    raison_a_revoir = fields.Text(string='التعليق')
    is_revision = fields.Boolean()
    time = fields.Integer(string='الاجال', related='time_id.time')
    difference = fields.Integer(string='الاجال', )
    time_id = fields.Many2one('wk.time', string='الاجال', compute='compute_time')
    depasse = fields.Boolean(string='depasse')

    def _compute_date(self):
        for rec in self:
            if rec.date_fin:
                rec.difference = (rec.date_fin - rec.date_debut).days
                rec.date_difference = str(rec.difference) + 'يوم'
                if rec.difference > rec.time:
                    rec.depasse = True
                else:
                    rec.depasse = False
            else:
                rec.date_difference = 'طور الانجاز'

    def compute_time(self):
        for rec in self:
            time_id = self.env['wk.time'].search([('state', '=', rec.state)])
            if time_id:
                rec.time_id = time_id.id
            else:
                rec.time_id = False


class States(models.Model):
    _name = 'wk.state.ponctuel'

    name = fields.Char(string='Nom')
    sequence = fields.Integer(string='Nom')


class PlanCharge(models.Model):
    _name = 'wk.ponctuel.charge'

    name = fields.Char(string='العميل')
    contrat_type = fields.Selection([('soumission', 'En soumission'),
                                     ('attribu', 'Attribué'),
                                     ('signature', 'En signature'),
                                     ('realisation', 'En réalisation')],
                                    string='حالة الصفقة')
    montant_ht = fields.Float(string='المبلغ H.T KDA')
    date_debut = fields.Date(string='تاريخ البدء')
    niveau = fields.Float(string='مستوى الانجاز %')
    besoin = fields.Float(string='الاحتياجات التمويلية')
    ponctuel_id = fields.Many2one('wk.workflow.ponctuel',
                                  string='Ponctuel')

