from datetime import date, timedelta

from odoo import http
from odoo.http import request


class SalesController(http.Controller):

    @http.route('/sales/dashboard', type='http', auth='user')
    def sales_interface(self, config_id=False, **kwargs):
        return request.render('sale_extras.index')

    @http.route('/api/sales/today', type='json', auth='user')
    def get_today_sales(self, config_id=False, **kwargs):
        today_date = date.today()

        request.cr.execute(
            f"""
            SELECT SUM(amount_total_in_currency_signed) FROM account_move WHERE
            move_type =  'out_invoice' AND
            state = 'posted' AND
            invoice_date =  '{str(today_date)}' AND
            invoice_method_type = 'CONTADO';
            """
        )
        data = request.cr.fetchall()[0][0]
        in_cash_amount = data if data is not None else 0.00

        request.cr.execute(
            f"""
            SELECT SUM(amount_total_in_currency_signed) FROM account_move WHERE
            move_type =  'out_invoice' AND
            state = 'posted' AND
            invoice_date =  '{str(today_date)}' AND
            invoice_method_type = 'CREDITO';
            """
        )
        data = request.cr.fetchall()[0][0]
        credit_amount = data if data is not None else 0.00

        charges_amount = 0
        for account_payment in request.env['account.payment'].search([
            ('payment_type', '=', 'inbound'),
            ('date', '=', today_date),
            ('state', '=', 'posted'),
            ('is_internal_transfer', '=', False),
        ]):
            charges_amount += account_payment.amount

        in_cash_count = request.env['account.move'].search_count([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '=', today_date),
            ('invoice_method_type', '=', 'CONTADO')
        ])

        credit_count = request.env['account.move'].search_count([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '=', today_date),
            ('invoice_method_type', '=', 'CREDITO')
        ])

        charges_count = request.env['account.payment'].search_count([
            ('payment_type', '=', 'inbound'),
            ('date', '=', today_date),
            ('state', '=', 'posted'),
            ('is_internal_transfer', '=', False),
        ])

        total_amount = in_cash_amount + credit_amount

        return {
            'in_cash_amount': in_cash_amount,
            'credit_amount': credit_amount,
            'charges_amount': charges_amount,
            'total_amount': total_amount,

            'in_cash_count': in_cash_count,
            'credit_count': credit_count,
            'charges_count': charges_count
        }

    @http.route('/api/sales/month', type='json', auth='user')
    def get_month_sales(self, config_id=False, **kwargs):
        register_date = date.today()
        month_sales = []

        for x in range(1, register_date.day):
            register_date = register_date - timedelta(days=1)

            request.cr.execute(
                f"""
                SELECT SUM(amount_total_in_currency_signed) FROM account_move WHERE
                move_type =  'out_invoice' AND
                state = 'posted' AND
                invoice_date = '{str(register_date)}' AND
                invoice_method_type = 'CONTADO';
                """
            )
            data = request.cr.fetchall()[0][0]
            in_cash_amount = data if data is not None else 0.00

            request.cr.execute(
                f"""
                SELECT SUM(amount_total_in_currency_signed) FROM account_move WHERE
                move_type =  'out_invoice' AND
                state = 'posted' AND
                invoice_date = '{str(register_date)}' AND
                invoice_method_type = 'CREDITO';
                """
            )
            data = request.cr.fetchall()[0][0]
            credit_amount = data if data is not None else 0.00

            charges_amount = 0.00
