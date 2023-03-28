# -*- coding:utf-8 -*-
import logging
from odoo import fields,models,api

logger = logging.getLogger(__name__)

class PresupuestoModel(models.Model):
    _name='presupuesto.model'
    _inherit = 'image.mixin'
    name = fields.Char('Nombre')

    premiereDate = fields.Datetime('Fecha de estreno')
    classification = fields.Selection([
        ('G','G'), # todo publico
        ('PG', 'PG'), # Se recomienda compañia de un adulto
        ('PG-13', 'PG-13'),  # Para mayores de 13 años
        ('R', 'R'),  # Compañia de un adulto obligatoria
        ('NC-17', 'NC-17'),  # Compañia de un adulto obligatoria
    ],'Clasificacion')

    score = fields.Integer('Puntuacion', related="scoreReference")
    scoreReference = fields.Integer('Puntuacion')

    active = fields.Boolean('Activo')

    director_category_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Director',
        default = lambda self: self.env['res.partner.category'].search([('name','=','Director')])
    )
    director_id = fields.Many2one(
        comodel_name = 'res.partner',string='Director')


    genero_ids = fields.Many2many(
        comodel_name = 'genero',string='Genero')
    description = fields.Text('Descripcion')
    link_trailer = fields.Char()

    is_book = fields.Boolean('Version libro')
    book = fields.Binary('Libro')
    book_filename = fields.Char()

    state = fields.Selection([
        ("borrador","Borrador"),
        ("aprobado","Aprobado"),
        ("cancelado","Cancelado")],default="borrador",string="Estado",copy=False)
    approvedDate = fields.Datetime('Fecha aprovado', copy=False)

    def aprobar_presupuesto(self):
        logger.info('Aprobar...')
        self.state = 'aprobado'
        self.approvedDate = fields.Datetime.now()

    def cancelar_presupuesto(self):
        print('Cancelar...')
        self.state = 'cancelado'

    def unlink(self):
        logger.info('Se desparo la funcion unlink')
