from odoo import fields, models, api


class CreateUomWizard(models.TransientModel):
    _name = 'create.uom.wizard'

    uom_id = fields.Many2one('uom.uom', string='Base UOM')
    name = fields.Char(string='Name')
    factor = fields.Float(string='Conversion Factor')

    def create_uom(self):
        uom_obj = self.env['uom.uom']
        uom_data = {
            'name': self.name,
            'factor': self.factor,
            'category_id': self.uom_id.category_id.id,
            'uom_type': self.uom_id.uom_type,
            'rounding': self.uom_id.rounding,
            'active': True,
        }
        new_uom = uom_obj.create(uom_data)
        new_uom.factor_inv = 1.0 / self.factor
        return {'type': 'ir.actions.act_window_close'}