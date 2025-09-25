from odoo import fields, models,api
from datetime import datetime, timedelta,time



class ClassSchedule(models.Model):
    _name = "class.schedule"
    _description = "Class Schedule"



    class_id=fields.Many2one('school.classes', string='Class', required=True)
    grad=fields.Selection(related='class_id.grad',string='Grade',readonly=True)

    materials_id=fields.Many2one('study.materials', string='Materials', required=True)
    teacher=fields.Many2one('res.users', string='Teacher', required=True)
    day = fields.Selection([
        ('saturday', 'Saturday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
    ], string='Day', required=True)
    start_time=fields.Char(string='Start Time', required=True)
    duration = fields.Float(string='Duration (minute)',required=True)
    end_time = fields.Char(string='End Time', readonly=True ,compute='_compute_end_time')






    @api.model
    def _compute_end_time(self):
        for rec in self:
            start_time=datetime.strptime(str(rec.start_time), "%H:%M")
            rec.end_time = str((start_time + timedelta(minutes=rec.duration)).time())

