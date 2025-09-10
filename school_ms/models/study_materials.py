from odoo import fields, models,api


class StudyMaterials(models.Model):
    _name = 'study.materials'
    _description = 'Study Materials'



    material_id=fields.Char('Material ID', required=True)
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    educational_stage = fields.Selection([
        ('EL', 'Elementary'),
        ('BA', 'Basic'),
        ('SE', 'Secondary'),
    ], required=True, default='EL')
    total_mark=fields.Integer('Total Mark')
    passing_mark=fields.Integer('Passing Mark')