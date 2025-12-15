from  odoo import models,fields,api


class SchoolInstallment(models.Model):
    _name = 'school.installment'
    _description = 'School Installment'

    student_id =fields.Many2one('school.students')
    due_date=fields.Date('Due Date')
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
    )
    amount=fields.Monetary('Amount',currency_field='currency_id')
    status=fields.Selection([
        ('draft','Draft'),
        ('due','Due'),
        ('paid','Paid'),
    ])
    invoice_id=fields.Many2one('account.move')
