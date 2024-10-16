from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_payment(self, order):
        invoice = order._create_invoices()
        invoice.action_post()
        payment = self.env['account.payment'].create({
            'partner_id': order.partner_id.id,
            'payment_type': 'inbound',
            'amount': invoice.amount_total,
            'payment_method_id': invoice.payment_id.payment_method_id.id
        })
        payment.action_post()
        payment = self.env['account.payment.register']._reconcile_payments([{
            'payment': payment,
            'to_reconcile': invoice.line_ids,
        }])

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                delivery = self.env['stock.picking'].search([('sale_id', '=', order.id)])
                delivery.button_validate()
                self._create_payment(order)
            return res
    