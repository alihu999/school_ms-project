from odoo import  api, fields, models
from markupsafe import Markup

from odoo.exceptions import UserError


class ChangeStudentStateWizard(models.TransientModel):
    _name = 'change.student.state.wizard'
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
        # Retrieve the currently active student record using ID from context
        # Using sudo() to bypass security rules for this operation
        student_id = self.env['school.students'].sudo().browse(self._context.get('active_id'))

        # Check if the new state is 'admitted' (special case that requires class assignment)
        if vals.get('state')=='admitted':

            # Find an appropriate class for the student based on educational stage
            class_id=self.set_class_id(student_id.grad)

            # If no available class found, raise an error
            if not class_id:
                raise  UserError("there are not empty class")
            # Assign the student to the found class
            else:
                student_id.write({'class_id':class_id})
                student_id.create_student_installment()

        # Format the state change reason with HTML markup for display in notes
        reason=f'<li><span class="h4-fs"><strong>change state:</strong></span>{vals['reason']}</li>'

        # Update the student record with new state and append to existing notes
        # Using Markup to safely combine HTML content
        student_id.write({'state': vals['state'],
                          'note':Markup(f"{str(student_id.note)} {reason}")})

        # Call the superclass create method to complete the wizard creation
        return super(ChangeStudentStateWizard,self).create(vals)

    def set_class_id(self, grad):
        # Search for active classes that match the student's educational stage
        # Retrieve only the fields needed for capacity checking
        classes = self.env['school.classes'].search_read([
            ('grad', '=', grad),('state','=','active')
        ], ['id', 'current_number', 'total_number'])

        # Iterate through classes to find one with available capacity
        for cls in classes:
            # Check if current student count is less than total capacity
            if cls['current_number'] < cls['total_number']:
                # Return the first available class ID
                return cls['id']
        # Return None if no available classes found
        return None