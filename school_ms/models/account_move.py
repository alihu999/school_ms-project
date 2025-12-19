from  odoo import fields,models,api


class AccountMove(models.Model):
    _inherit = 'account.move'

    student_id=fields.Many2one('school.students',string='Student')

