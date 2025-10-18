from odoo import fields, models


class AcademicRecords(models.Model):
    _name = 'academic.records'
    _description = 'Academic Records'

    student_id = fields.Many2one('school.students', string='Student')
    material_name=fields.Many2one('study.materials',string='Material')
    quiz=fields.Integer('Quiz')
    exam=fields.Integer('Exam')
