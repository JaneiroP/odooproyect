from odoo import fields,models,api

class FiscalPrinterModel(models.Model):
    _name = "pos.cron"

    @api.model
    def validate_book(self):
        print("Abcd")