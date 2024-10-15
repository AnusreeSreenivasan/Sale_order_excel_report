from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def check_quotation_expiry(self):
        expiry_days = int(self.env['ir.config_parameter'].sudo().get_param('sale.quotation_expiry_days', default=5))

        manager_id = self.env['ir.config_parameter'].sudo().get_param('sale.quotation_expiry_manager_id', default=False)
        if not manager_id:
            return False  

        quotation_expiry_manager_id = self.env['res.users'].browse(int(manager_id))
        if not quotation_expiry_manager_id.exists():
            return False 
        expiry_date = (datetime.today() + timedelta(days=expiry_days)).date()

        sale_orders = self.search([
            ('state', 'in', ['draft', 'sent']),
            ('validity_date', '=', expiry_date)
        ])

        _logger.info('Orders fetched: %s', sale_orders)
        
        

        product_list = []
        for order in sale_orders:
            product_list.append({
                'name': order.name,
                'date_order': order.date_order.strftime('%Y-%m-%d'),
                'partner_id': order.partner_id.name,
                'amount_total': order.amount_total,
                'currency_id': order.currency_id
            })
        
        if product_list:
            template = self.env.ref('Email_template.quotation_mail_template')  
            for order in sale_orders:
                email_values = {
                            'email_to': quotation_expiry_manager_id.email,
                            'email_from': self.env.user.email or 'noreply@example.com',
                        }
            _logger.info('Sending email for Order: %s to: %s', order.name, quotation_expiry_manager_id.email)
            template.with_context(product_list=product_list).send_mail(
                self.id, 
                email_values=email_values, 
                force_send=True
            )
            
        