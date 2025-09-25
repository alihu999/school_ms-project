from odoo import fields, models,api
from datetime import datetime



class SchoolClass(models.Model):
    _name = 'school.classes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'School Classes'
    _rec_name = 'class_id'

    class_id = fields.Char('Name',readonly=True,tracking=True,default='New')
    educational_stage_id=fields.Many2one('education.stages')
    educational_stage=fields.Selection(related='educational_stage_id.education_stage',readonly=True)
    grad=fields.Selection(related='educational_stage_id.grad',readonly=True)
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
    class_schedule=fields.One2many('class.schedule','class_id',string='Class Schedule')



    @api.model
    def create(self,vals):

        res = super().create(vals)
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
        sequence_code = grad_to_code.get(res.grad)
        if vals.get('class_id','New')=='New':
            res.class_id= self.env['ir.sequence'].next_by_code(sequence_code)

        return res

    @api.depends('students')
    def _compute_current_number(self):

        # Iterate through each record in the current recordset
        for rec in self:

            # Calculate current student count by getting the length of the students relation
            rec.current_number=len(rec.students)
            if rec.current_number == rec.total_number:
                rec.state='complete'
            if rec.current_number < rec.total_number and rec.state != 'draft' and rec.state != 'cancel':
                rec.state='active'


    def open_change_class_state_wizard(self):

        # Retrieve the XML action definition for the wizard
        action=self.env['ir.actions.actions']._for_xml_id("school_ms.open_change_class_state_wizard_action")

        # Add context data to pass to the wizard (current class ID and state)
        action['context']={'class_id':self.class_id ,'state':self.state}

        # Return the action definition to open the wizard
        return action

    def download_class_schedule_pdf(self):
        data={'saturday':{},'monday':{},'tuesday':{},'wednesday':{},'thursday':{}}
        start_time_list=[]
        for class_schedule in self.class_schedule:
            start_time_list.append(class_schedule.start_time)
        start_time_list.sort()
        print(start_time_list)
