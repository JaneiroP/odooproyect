from odoo import fields,models,api

class UpdateWizard(models.TransientModel):
    _name = "update.wizard"

    name = fields.Char('Nueva descripcion')

#con search
    # def update_description(self):
    #     presupuesto_obj = self.env['presupuesto.model']
    #     presupuesto_id = presupuesto_obj.search([('id','=',self._context['active_id'])])
    #     presupuesto_id.description = self.name

#con browse

    def update_description(self):
        presupuesto_obj = self.env['presupuesto.model']
        presupuesto_id = presupuesto_obj.browse(self._context['active_id'])
        presupuesto_id.description = self.name

