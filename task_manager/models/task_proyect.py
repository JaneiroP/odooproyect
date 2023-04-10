from odoo import fields,models,api

class TaskProyect(models.Model):
    _name = 'task.proyect'

    name = fields.Char('Proyect name',required=True)
    description = fields.Text('Description')
    start_date = fields.Datetime('Start Date')
    finish_date = fields.Datetime('Finish Date')
    state = fields.Selection([('draft', 'Draft'), ('in progress', 'In progress'),
                             ('finished', 'Finished'), ('cancelled', 'Cancelled')], 'State', default="draft")
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string='responsable'
    )
    delegate_ids = fields.Many2many(
        comodel_name='res.users',
        string='delegates'
    )
    def to_draft(self):
        self.state = "draft"

    def to_in_progress(self):
        self.state = "in progress"

    def to_cancelled(self):
        self.state = "cancelled"

    def to_finished(self):
        self.state = "finished"

