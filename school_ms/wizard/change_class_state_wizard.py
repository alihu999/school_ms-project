from markupsafe import Markup

from odoo import  api, fields, models


class ChangeClassStateWizard(models.TransientModel):
    _name = 'change.class.state.wizard'
    _description = 'Change Class State Wizard'


    class_id= fields.Char("Class ID",default=lambda self: self._context.get('class_id'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('complete', 'Complete'),
        ('cancel', 'Cancelled'),
    ],default=lambda self: self._context.get('state'), required=True)
    reason = fields.Char("Reason",required=True)


    @api.model
    def create(self, vals):

        # Retrieve the currently active class record using the ID from context
        # Using sudo() to bypass security rules for this operation
        class_id = self.env["school.classes"].sudo().browse(self._context.get('active_id'))

        # Format the reason with HTML markup for display in notes
        reason=f'<li><span class="h4-fs"><strong>change state:</strong></span>{vals['reason']}</li>'

        # Update the class record with new state and append to existing notes
        # Using Markup to safely combine HTML content
        class_id.write({'state': vals['state'],
                          'notes': Markup(f"{str(class_id.notes)} {reason}")})

        # Call the superclass create method to complete the wizard creation
        return super(ChangeClassStateWizard, self).create(vals)