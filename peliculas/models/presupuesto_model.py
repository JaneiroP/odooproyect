# -*- coding:utf-8 -*-
import logging
from datetime import timedelta

import pytz
from odoo import fields,models,api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class PresupuestoModel(models.Model):
    _name='presupuesto.model'
    _inherit = 'image.mixin'

    @api.depends('detalle_ids')
    def _compute_total(self):
        for record in self:
            sub_total = 0
            for linea in record.detalle_ids:
                sub_total += linea.importe
            record.base = sub_total
            record.impuestos = sub_total * 0.18
            record.total = sub_total + record.impuestos

    name = fields.Char('Nombre')

    premiereDate = fields.Datetime('Fecha de estreno')
    classification = fields.Selection([
        ('G','G'), # todo publico
        ('PG', 'PG'), # Se recomienda compañia de un adulto
        ('PG-13', 'PG-13'),  # Para mayores de 13 años
        ('R', 'R'),  # Compañia de un adulto obligatoria
        ('NC-17', 'NC-17')  # Compañia de un adulto obligatoria
    ],'Clasificacion')

    classificationDesc = fields.Char('Descripcion de clasificacion')

    score = fields.Integer('Puntuacion', related="scoreReference")
    scoreReference = fields.Integer('Puntuacion')

    active = fields.Boolean('Activo')

    director_id = fields.Many2one(
        comodel_name='res.partner', string='Director')

    director_category_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Director',
        #primera version
        #default = lambda self: self.env['res.partner.category'].search([('name','=','Director')])
        #segunda version
        default=lambda self: self.env.ref('peliculas.category_director')
    )

    actor_ids = fields.Many2many(
        comodel_name='res.partner', string='Actores')

    actor_category_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Actor',
        default=lambda self: self.env.ref('peliculas.category_actor')
    )

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

    budget_number = fields.Char('Numero de presupuesto',copy=False)
    creation_date = fields.Datetime('Fecha de creacion', copy=False,
                                    default=lambda self: fields.Datetime.now())
    opinion = fields.Html('Opinion')

    detalle_ids = fields.One2many(
        comodel_name='presupuesto.detalle',
        inverse_name='presupuesto_id',
        string='Detalle'
    )

    campos_ocultos = fields.Boolean(string='Mostrar campos ocultos')

    # moneda a usar
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id
    )

    terminos = fields.Text('Terminos y condiciones')
    base = fields.Monetary(
        string='Base imponible',
        compute='_compute_total'
    )
    impuestos = fields.Monetary(
        string='Impuestos',
        compute='_compute_total'
    )
    total = fields.Monetary(
        string='Total',
        compute='_compute_total'
    )


    def aprobar_presupuesto(self):
        logger.info('Aprobar...')
        self.state = 'aprobado'
        self.approvedDate = fields.Datetime.now()

    def cancelar_presupuesto(self):
        print('Cancelar...')
        self.state = 'cancelado'

#Delete a register
    def unlink(self):
        logger.info('Se desparo la funcion unlink')
        #se utiliza bucle para poder borrar muchos registros a la vez
        for record in self:
            if record.state != 'cancelado':
                raise UserError('No se puede borrar el registro porque no se encuentra en el estado cancelado')
            super(PresupuestoModel, record).unlink()



    @api.model
    def create(self,variables):
        logger.info(f'{variables}')
        sequence_obj = self.env['ir.sequence']
        #funcion que devuelve proxima sequencia
        correlativo = sequence_obj.next_by_code('sequencia.presupuesto.pelicula')
        variables['budget_number'] = correlativo
        return super(PresupuestoModel, self).create(variables)

    def write(self,variables):
        logger.info(f'{variables}')
        if 'classification' in variables:
          raise UserError('La clasificacion no se puede editar')
        return super(PresupuestoModel, self).write(variables)

    def copy(self,default=None):
        default = dict(default or {})
        default['name']=self.name + '(copia)'
        default['scoreReference'] = 1
        return super(PresupuestoModel, self).copy(default)

    @api.onchange('classification')
    def _onchange_classificacion(self):
        if self.classification:
            if self.classification == 'G':
                self.classificationDesc = 'Todo publico'
            if self.classification == 'PG':
                self.classificationDesc = 'Se recomienda compañia de un adulto'
            if self.classification == 'PG-13':
                self.classificationDesc = 'Para mayores de 13 años'
            if self.classification == 'R':
                self.classificationDesc = 'Compañia de un adulto obligatoria'
            if self.classification == 'NC-17':
                self.classificationDesc = 'No menores de 17 años'
        else:
            self.classificationDesc = False

class PresupuestoDetalle(models.Model):
    _name = "presupuesto.detalle"

    presupuesto_id = fields.Many2one(
        comodel_name='presupuesto.model',
        string='Presupuesto'
    )
    name = fields.Many2one('recurso.cinematografico', string="Recurso")
    description = fields.Char('Descripcion', related="name.description")
    contacto_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto',
        related='name.contacto_id'
    )
    imagen = fields.Binary(
        string='Imagen',
        related='name.imagen'
    )
    cantidad = fields.Float(
        string='Cantidad',
        default=1.0,
        digits=(16, 4)
    )
    precio = fields.Float(
        string='Precio',
        digits='Product Price'
    )
    importe = fields.Monetary(
        string='Importe '
    )
    #moneda a usar
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        related='presupuesto_id.currency_id'
    )

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.precio = self.name.precio

    @api.onchange('cantidad', 'precio')
    def _onchange_importe(self):
        self.importe = self.cantidad * self.precio

    def validate_book(self):
        print('hi')
        start_date = fields.Datetime.now() - timedelta(days=1)
        finish_date = fields.Datetime.now()
        print(start_date,finish_date)
        #obtener cada registro
        pos_peliculas = self.env['presupuesto.model'].search([
             ('premiereDate', '>=', start_date),
             ('premiereDate', '<', finish_date)
        ])
        #obtener user
        user_tz = pytz.timezone(self.env.user.tz or 'UTC')
        #mostrar cada registro
        for pos_pelicula in pos_peliculas:
           print(f'{pos_pelicula.name}-{pos_pelicula.premiereDate}')
            #convertir timezone
        nextcall = start_date.astimezone(user_tz).replace(tzinfo=None)
        print(nextcall)
