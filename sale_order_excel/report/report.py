from odoo import models

class SaleorderXlsx(models.AbstractModel):
    _name = 'report.sale_order_excel.sale_order_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('Sale Orders')
        format = workbook.add_format({
            'align': 'center',
            'font_size': 14,
            'bg_color': '#92a8d1',
            'border': 1,
        })
        format_1 = workbook.add_format({
            'align': 'center',
            'font_size': 10,
            'bg_color': '#00FF00',
            'border': 1,
        })
        format_2 = workbook.add_format({
            'align': 'center',
        })
        sheet.set_column('A:E', 20)
        row = 0
        col = 0
        sheet.merge_range(row, col, row, col+3, 'SaleOrders', format)
        row = 1
        col = 0
        sheet.write(row, col, 'Partner',format_1)
        sheet.write(row, col + 1, 'Order Date',format_1)
        sheet.write(row, col + 2, 'Order',format_1)
        sheet.write(row, col + 3, 'pricelist',format_1)
        orders = self.env['sale.order'].browse(data['orders'])
        customers = orders.mapped('partner_id')
        
        row += 1
        for customer in customers:
            customer_orders = orders.filtered(lambda o: o.partner_id == customer)
            for order in customer_orders:
                sheet.write(row, col + 1, str(order.date_order),format_2)
                sheet.write(row, col + 2, order.name,format_2)
                sheet.write(row, col , order.partner_id.name,format_2)
                sheet.write(row, col + 3, order.payment_term_id.name,format_2)
                row += 1

