from odoo import fields, models, api


class CreateUomWizard(models.TransientModel):
    _name = 'create.uom.wizard'

    unit_value = fields.Float(string='Unit Value')
    uom_id = fields.Many2one('uom.uom', string='Referenced UoM')


    def create_uom(self):
        uom_obj = self.env['uom.uom']
        uom_data = {
            'name': f'{self.unit_value} {self.uom_id}',
            'factor': self.factor, #falta factor value
            'category_id': self.uom_id.category_id.id,
            'uom_type': self.uom_id.uom_type,
            'rounding': self.uom_id.rounding,
            'active': True,
        }
        new_uom = uom_obj.create(uom_data)
        new_uom.factor_inv = 1.0 / self.factor
        return {'type': 'ir.actions.act_window_close'}