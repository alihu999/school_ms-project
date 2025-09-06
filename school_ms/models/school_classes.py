from odoo import fields, models,api
from odoo.tools.which import defpath


class SchoolClass(models.Model):
    _name = 'school.classes'
    _description = 'School Classes'
    _rec_name = 'class_id'

    class_id = fields.Char('Name',readonly=True,tracking=True,default='New')
    educational_stage=fields.Selection([
        ('KG','Kindergarten'),
        ('EL','Elementary'),
        ('BA','Basic'),
        ('SE','Secondary'),
    ],required=True,default='KG')
    total_number=fields.Integer('Total Number of Students',required=True)
    current_number=fields.Integer('Current Number of Students',required=True)
    state=fields.Selection([
        ('draft','Draft'),
        ('active','Active'),
        ('complete','Complete'),
        ('cancel','Cancelled'),
    ],default='draft',required=True,readonly=True)
    students=fields.One2many('school.students','class_id',string='Students')



    @api.model
    def create(self,vals):
        print(vals)
        if vals.get('class_id','New')=='New':
            if vals.get('educational_stage')=='KG':
                vals['class_id'] = self.env['ir.sequence'].next_by_code('kindergarten.classes.sequence')
            elif vals.get('educational_stage')=='EL':
                vals['class_id'] = self.env['ir.sequence'].next_by_code('elementary.classes.sequence')
            elif vals.get('educational_stage')=='BA':
                vals['class_id'] = self.env['ir.sequence'].next_by_code('basic.classes.sequence')
            else:
                vals['class_id'] = self.env['ir.sequence'].next_by_code('secondary.classes.sequence')
        return super(SchoolClass, self).create(vals)

    @api.onchange('students')
    def _onchange_class_id(self):
        print('_onchange_class_id')
        self.current_number=len(self.students)