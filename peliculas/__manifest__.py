# -*- coding:utf-8 -*-

{
    'name':'Modulo de peliculas',
    'version':'1.0',
    'depends': ['base','mail','project'],
    'author':'Janeiro Placido',
    'website':'http://www.google.com',
    'category':'Peliculas',
    'summary':'Modulo de presupuesto de peliculas',
    'description':'Este modulo va a servir para hacer presupuestos de peliculas',
    'data':[
        'security\security.xml',
        'security\ir.model.access.csv',
        'data\categoria.xml',
        'data\secuencia.xml',
        'views\servidor_actions.xml',
        'views\menu.xml',
        'views\search_view.xml',
        'views\presupuesto_views.xml',
        'data\mycron.xml',
        'wizard\myupdate_wizard_views.xml',
        'wizard\create_uom_wizard_view.xml',
    ],

}