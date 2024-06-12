from odoo import models, fields, api, _
import datetime


class DocChecker(models.Model):
    _inherit = 'wk.document.check'
    _description = ' check documents'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    
    
class KycDetail(models.Model):
    _inherit = 'wk.kyc.details'
    _description = 'Line KYC'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class Partenaire(models.Model):
    _inherit = 'wk.partenaire'
    _description = 'Partenaire du client'
    
    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class EquipeGestion(models.Model):
    _inherit = 'wk.gestion'
    _description = 'Equipe de gestion'
    
    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    
    
class Taillefin(models.Model):
    _inherit = 'wk.taille'
    _description = 'La taille et la structure du financement requis'
    
    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class SituationBancaire(models.Model):
    _inherit = 'wk.situation'
    _description = 'Situation bancaire et obligations envers autrui'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class SituationFinanciere(models.Model):
    _inherit = 'wk.situation.fin'
    _description = 'Situation financière'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class Fournisseur(models.Model):
    _inherit = 'wk.fournisseur'
    _description = 'fournisseur'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class Client(models.Model):
    _inherit = 'wk.client'
    _description = 'clients'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class Companies(models.Model):
    _inherit = 'wk.companies'
    _description = 'Companies in relation'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class FaciliteAccorde(models.Model):
    _inherit = 'wk.facilite.accorde'
    _description = 'Détails des facilités accordées'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class Detail(models.Model):
    _inherit = 'wk.detail.garantie'
    _description = 'Detail Garantie'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class DetailGarantiePropose(models.Model):
    _inherit = 'wk.detail.garantie.propose'
    _description = 'Detail Garantie'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class Ganrantie(models.Model):
    _inherit = 'wk.garantie.conf'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    
    
class GanrantieFin(models.Model):
    _inherit = 'wk.garantie.fin'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class GanrantieAutre(models.Model):
    _inherit = 'wk.garantie.autres'
    
    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')
    

class Risque(models.Model):
    _inherit = 'wk.risque.line'
    _description = 'Risque'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class PositionTax(models.Model):
    _inherit = 'wk.position'
    _description = 'Position taxonomique'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class MouvementAction(models.Model):
    _inherit = 'wk.mouvement'
    _description = 'Mouvement et Action'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class DeclarationFisc(models.Model):
    _inherit = 'wk.companies.fisc'
    _description = 'Companies fisc'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class FaciliteExistante(models.Model):
    _inherit = 'wk.facilite.existante'
    _description = 'Facilités existantes avec la banque'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class MouvementGroupe(models.Model):
    _inherit = 'wk.mouvement.group'
    _description = 'Mouvement et Action'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class TCR(models.Model):
    _inherit = 'import.ocr.tcr'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class Passif(models.Model):
    _inherit = 'import.ocr.passif'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class Actif(models.Model):
    _inherit = 'import.ocr.actif'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class BilanFisc(models.Model):
    _inherit = 'wk.bilan'
    _description = 'Bilan fiscal'
    _order = 'sequence,id'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class Recap(models.Model):
    _inherit = 'wk.recap'
    _description = 'declaration'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class Variables(models.Model):
    _inherit = 'wk.variable'
    _description = 'variables'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class SwotWeakness(models.Model):
    _inherit = 'wk.swot.weakness'
    _description = 'swot matrice'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class SwotStrength(models.Model):
    _inherit = 'wk.swot.strength'
    _description = 'swot matrice'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class SwotThreats(models.Model):
    _inherit = 'wk.swot.threat'
    _description = 'swot matrice'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class SwotOpportunities(models.Model):
    _inherit = 'wk.swot.opportunitie'
    _description = 'swot matrice'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class FacilitePropose(models.Model):
    _inherit = 'wk.facilite.propose'
    _description = 'facilite propose'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel')


class Scoring(models.Model):
    _inherit = 'risk.scoring'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel',
                                  string='Ponctuel')


class Tracking(models.Model):
    _name = 'wk.tracking.ponctuel'

    ponctuel_id = fields.Many2one('wk.workflow.ponctuel',
                                  string='Ponctuel')
    date_debut = fields.Date(string='تاريخ البدء')
    date_fin = fields.Date(string='تاريخ الانتهاء')
    date_difference = fields.Char(string='الوقت المستغرق', compute='_compute_date')
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
