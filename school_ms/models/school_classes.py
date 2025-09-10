from odoo import fields, models,api


class SchoolClass(models.Model):
    _name = 'school.classes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'School Classes'
    _rec_name = 'class_id'

    class_id = fields.Char('Name',readonly=True,tracking=True,default='New')
    educational_stage=fields.Selection([
        ('EL','Elementary'),
        ('BA','Basic'),
        ('SE','Secondary'),
    ],readonly=True)
    grad=fields.Selection([
        ("first",'First Grad'),('second','Second Grad'),('third','Third Grad'),('fourth','Fourth Grad'),
        ('fifth','Fifth Grad'),('sixth','Sixth Grad'),('seventh','Seventh Grad'),('eight','Eight Grad'),
        ('ninth','Ninth Grad'),('tenth','Tenth Grad'),('eleventh','Eleventh Grad'),('twelfth','Twelfth Grad')
    ])
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
        # Map the 'grad' value to the correct sequence code
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
        sequence_code = grad_to_code.get(vals.get('grad'))
        if vals.get('class_id','New')=='New':
            vals['class_id'] = self.env['ir.sequence'].next_by_code(sequence_code)
        if vals.get('grad') in list(grad_to_code.keys())[0:6]:
            vals['educational_stage']="EL"
        elif vals.get('grad') in list(grad_to_code.keys())[6:9]:
            vals['educational_stage']="BA"
        else:
            vals['educational_stage']="SE"




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
