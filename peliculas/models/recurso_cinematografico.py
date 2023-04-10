from odoo import fields, api, models

class RecursoCinematografico(models.Model):
    _name = 'recurso.cinematografico'

    name = fields.Char('Recurso')
    description = fields.Char('Description')
    precio = fields.Float('Precio')
    contacto_id = fields.Many2one('res.partner',
                                  domain="[('is_company','=',False)]")
    imagen = fields.Binary('imagen')