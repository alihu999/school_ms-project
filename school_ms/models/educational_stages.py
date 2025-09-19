from odoo import fields, models,api


class EducationStages(models.Model):
    _name = 'education.stages'
    _description = 'Education Stages'
    _inherit = ['mail.thread', 'mail.activity.mixin']



    education_stage=fields.Selection([
        ('EL','Elementary'),
        ('BA','Basic'),
        ('SE','Secondary'),
    ],readonly=True)
    grad = fields.Selection([
        ("first", 'First Grad'), ('second', 'Second Grad'), ('third', 'Third Grad'), ('fourth', 'Fourth Grad'),
        ('fifth', 'Fifth Grad'), ('sixth', 'Sixth Grad'), ('seventh', 'Seventh Grad'), ('eight', 'Eight Grad'),
        ('ninth', 'Ninth Grad'), ('tenth', 'Tenth Grad'), ('eleventh', 'Eleventh Grad'), ('twelfth', 'Twelfth Grad')
    ],default='first')
    notes=fields.Html('Notes')


    class_id=fields.One2many('school.classes',
                             'educational_stage_id',string='Class ID')
    study_materials=fields.One2many('study.materials',
                                    'educational_stage_id')

    #study_material=fields.One2many()



    @api.onchange('grad')
    def _onchange_grad(self):
        pass

    @api.model
    def create(self, vals):
        print(vals)
        grad_to_code = {
            'first': 'first.grad.sequence',
            'second': 'second.grad.sequence',
            'third': 'third.grad.sequence',
            'fourth': 'fourth.grad.sequence',
            'fifth': 'fifth.grad.sequence',
            'sixth': 'sixth.grad.sequence',
            'seventh': 'seventh.grad.sequence',
            'eight': 'eight.grad.sequence',
            'ninth': 'ninth.grad.sequence',
            'tenth': 'tenth.grad.sequence',
            'eleventh': 'eleventh.grad.sequence',
            'twelfth': 'twelfth.grad.sequence',
        }
        if vals.get('grad') in list(grad_to_code.keys())[0:6]:
            vals ['education_stage'] = "EL"
        elif vals.get('grad') in list(grad_to_code.keys())[6:9]:
            vals ['education_stage'] = "BA"
        else:
            vals ['education_stage'] = "SE"
        return super(EducationStages, self).create(vals)
