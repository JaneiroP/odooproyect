from odoo import fields,api,models

class TaskModel(models.Model):
    _name = 'task.model'

    name = fields.Char('Task name')
    duration_interval = fields.Integer('Time')
    duration_time = fields.Selection([('minutes', 'Minutes'), ('hours', 'Hours'), ('days', 'Days')], 'Und')
    delegate_task_ids = fields.Many2many(
        comodel_name='res.users'
    )
    state = fields.Selection([('draft', 'Draft'), ('in progress', 'In progress'),
                              ('finished', 'Finished'), ('cancelled', 'Cancelled')], 'State', default="draft")

