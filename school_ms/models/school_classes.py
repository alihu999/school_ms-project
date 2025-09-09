from odoo import fields, models,api


class SchoolClass(models.Model):
    _name = 'school.classes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'School Classes'
    _rec_name = 'class_id'

    class_id = fields.Char('Name',readonly=True,tracking=True,default='New')
    educational_stage=fields.Selection([
        ('KG','Kindergarten'),
        ('EL','Elementary'),
        ('BA','Basic'),
        ('SE','Secondary'),
    ],required=True,default='KG')
    total_number=fields.Integer('Total Number of Students',required=True,tracking=True)
    current_number=fields.Integer('Current Number of Students',
                                  required=True,tracking=True,
                                  readonly=True,compute='_compute_current_number')
    state=fields.Selection([
        ('draft','Draft'),
        ('active','Active'),
        ('complete','Complete'),
        ('cancel','Cancelled'),
    ],default='draft',required=True,readonly=True,tracking=True,)
    notes=fields.Html('Notes')
    students=fields.One2many('school.students','class_id',string='Students',tracking=True)



    @api.model
    def create(self,vals):
        # Check if 'class_id' is not provided or set to 'New'
        if vals.get('class_id','New')=='New':

            # Assign sequence based on educational stage
            if vals.get('educational_stage')=='KG':
                # Get next sequence for kindergarten classes
                vals['class_id'] = self.env['ir.sequence'].next_by_code('kindergarten.classes.sequence')

            elif vals.get('educational_stage')=='EL':
                # Get next sequence for elementary classes
                vals['class_id'] = self.env['ir.sequence'].next_by_code('elementary.classes.sequence')

            elif vals.get('educational_stage')=='BA':
                # Get next sequence for basic classes
                vals['class_id'] = self.env['ir.sequence'].next_by_code('basic.classes.sequence')

            else:
                # Default to secondary classes sequence for any other stage
                vals['class_id'] = self.env['ir.sequence'].next_by_code('secondary.classes.sequence')
        # Call superclass method with updated values to create the record
        return super(SchoolClass, self).create(vals)


    @api.depends('students')
    def _compute_current_number(self):

        # Iterate through each record in the current recordset
        for rec in self:

            # Calculate current student count by getting the length of the students relation
            rec.current_number=len(rec.students)


    def open_change_class_state_wizard(self):

        # Retrieve the XML action definition for the wizard
        action=self.env['ir.actions.actions']._for_xml_id("school_ms.open_change_class_state_wizard_action")

        # Add context data to pass to the wizard (current class ID and state)
        action['context']={'class_id':self.class_id ,'state':self.state}

        # Return the action definition to open the wizard
        return action
