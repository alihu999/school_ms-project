from datetime import date
from odoo import fields, models, api






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

    class_id = fields.Many2one('school.classes',
                               string='Class', required=True, tracking=True)
    educational_stage = fields.Selection([
        ('KG', 'Kindergarten'),
        ('EL', 'Elementary'),
        ('BA', 'Basic'),
        ('SE', 'Secondary'),
    ], required=True, default='KG')
    note = fields.Html(string='Note')


    #Health Information
    blood_group = fields.Selection(
        selection=[('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),
                   ('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-'),],
        string='Blood Group',required=True
    )
    medical_information=fields.Text(string='Medical Information',required=True)




    @api.model
    def create(self, vals):
        if vals.get('student_id', 'New') == 'New':
            vals['student_id'] =(self.env['ir.sequence'].
                                   next_by_code('school.student.sequence'))
        return super(SchoolStudent, self).create(vals)



    @api.depends('father_name', 'mother_name')
    def _compute_emergency_contact(self):
        for student in self:
            if self.mother_name:
                student.emergency_contact_id = self.mother_name
            elif self.father_name:
                student.emergency_contact_id = self.father_name
            else:
                student.emergency_contact_id = False

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age=today.year-rec.date_of_birth.year

    def open_change_state_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id("school_ms.open_change_state_wizard_action")
        action['context']={'name':f"{self.name} {self.last_name}" ,'state':self.state}
        return action




















