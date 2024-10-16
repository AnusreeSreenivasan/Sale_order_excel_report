from odoo import api, fields, models

class SalesReportWizard(models.TransientModel):
    _name = "sale.report.wizard"
    _description = "Sale Report Wizard"

    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime(required=True)
    customer_id= fields.Many2one('res.partner', string="Customer")

    
    def action_print_excel_report(self):
        domain = []
        customer_id = self.customer_id
        if customer_id:
            domain += [('partner_id','=',customer_id.ids)]

        date_start = self.start_date
        if date_start:
            domain += [('date_order','>=',date_start)] 

        date_end = self.end_date
        if date_end:
            domain += [('date_order','<=',date_end)]
        
        sale = self.env['sale.order'].search(domain)

        data = {
            'orders':sale.ids,
            'form_data':self.read()[0]

        }

        return self.env.ref('sale_order_excel.action_report_sale_order').report_action(self,data=data)
      
