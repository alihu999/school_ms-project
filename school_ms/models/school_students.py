from datetime import date
from odoo import fields, models, api
from odoo.exceptions import UserError

import random
from datetime import date, timedelta
import logging

_logger = logging.getLogger(__name__)






class SchoolStudent(models.Model):
    _name = 'school.students'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "student_id"

    student_id = fields.Char(
        string="Student ID",
        readonly=True,
        default='New',tracking=True,)
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'), ('admitted', 'Admitted'), ('active', 'Active'),
            ('alumni', 'Alumni'), ('terminated', 'Terminated'),
        ],
        string='Status',
        default='draft',
        tracking=True,
        copy=False
    )

    #Personal Information
    name = fields.Char('First Name',required=True,tracking=True)
    last_name = fields.Char('Last Name',required=True,tracking=True)
    gender=fields.Selection([('male','Male'),('female','Female')],required=True)
    date_of_birth = fields.Date(string='Date of Birth',required=True)
    age=fields.Integer('Age',compute='_compute_age',store=True,tracking=True)
    image=fields.Binary(string='Image',required=True)
    father_name = fields.Many2one('res.partner',required=True,tracking=True)
    mother_name = fields.Many2one('res.partner',required=True,tracking=True)
    nationality_id = fields.Many2one(
        'res.country',
        string='Nationality',
        default=lambda self: self.env['res.country'].search([('phone_code','=','963')]),
        required=True)
    religion = fields.Selection(
        string='Religion',
        required=True,
        default='muslim',
        tracking=True,
        selection=[('muslim','Muslim'),('christian','Christian')])

    #Academic Information
    grad = fields.Selection([
        ("first", 'First Grad'), ('second', 'Second Grad'), ('third', 'Third Grad'), ('fourth', 'Fourth Grad'),
        ('fifth', 'Fifth Grad'), ('sixth', 'Sixth Grad'), ('seventh', 'Seventh Grad'), ('eight', 'Eight Grad'),
        ('ninth', 'Ninth Grad'), ('tenth', 'Tenth Grad'), ('eleventh', 'Eleventh Grad'), ('twelfth', 'Twelfth Grad')
    ])
    class_id = fields.Many2one('school.classes',
                               string='Class', tracking=True)
    educational_stage = fields.Selection('school.classes','Educational Stage',
                                        related='class_id.educational_stage',tracking=True)
    note = fields.Html(string='Note')


    #Health Information
    blood_group = fields.Selection(
        selection=[('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),
                   ('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-'),],
        string='Blood Group',required=True
    )
    medical_information=fields.Text(string='Medical Information',required=True)
    academic_records=fields.One2many('academic.records',inverse_name='student_id')




    @api.model
    def create(self, vals):
        # Check if student_id is not provided or set to 'New'
        if vals.get('student_id', 'New') == 'New':

            # Generate a new student ID using the predefined sequence
            vals['student_id'] =(self.env['ir.sequence'].
                                   next_by_code('school.student.sequence'))

        # Call the superclass create method with the updated values
        return super(SchoolStudent, self).create(vals)




    @api.depends('date_of_birth')
    def _compute_age(self):

        # Get today's date for age calculation
        today = date.today()

        # Iterate through all records in self
        for rec in self:

            # Check if date_of_birth is set for this record
            if rec.date_of_birth:

                # Calculate age by subtracting birth year from current year
                rec.age=today.year-rec.date_of_birth.year

    def open_change_student_state_wizard(self):

        # Retrieve the XML action definition for the student state wizard
        action=self.env['ir.actions.actions']._for_xml_id("school_ms.open_change_student_state_wizard_action")

        # Add context with student's full name (combined first and last name) and current state
        action['context']={'name':f"{self.name} {self.last_name}" ,'state':self.state}

        # Return the action to open the wizard
        return action




















