from odoo import  api, fields, models

class ChangeStateWizard(models.TransientModel):
    _name = 'change.state.wizard'
    _description = 'Change State Wizard'


    name=fields.Char(default=lambda self: self._context.get('name'),string='Student name')
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'), ('admitted', 'Admitted'), ('active', 'Active'),
            ('alumni', 'Alumni'), ('terminated', 'Terminated'),
        ],required=True,
        default = lambda self: self._context.get('state')
    )
    reason=fields.Text(string='Reason',required=True)


    @api.model
    def create(self, vals):
        student_id = self.env['school.students'].sudo().browse(self._context.get('active_id'))
        print(student_id.note)
        #student_id.write({'state': vals['state'],'reason':""})
        return super(ChangeStateWizard,self).create(vals)