from odoo import fields, models,api


class StudyMaterials(models.Model):
    _name = 'study.materials'
    _description = 'Study Materials'



    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    educational_stage_id = fields.Many2one('education.stages')
    educational_stage = fields.Selection(related='educational_stage_id.education_stage', readonly=False)
    grad = fields.Selection(related='educational_stage_id.grad', readonly=False)
    lessons_number=fields.Integer(string='Lessons')
    total_mark=fields.Integer('Total Mark')
    passing_mark=fields.Integer('Passing Mark')