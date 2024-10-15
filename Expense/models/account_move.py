from odoo import api,fields,models






class  invoiceid(models.Model):

    _inherit = "account.move"


    coupen = fields.Char(string="invoice id") 
    price_after_discount=fields.Float(string="Subtotal")   
    

    # def _prepare_invoice(self):
    #     invoice_vals = super(invoiceid, self)._prepare_invoice()
    #     invoice_vals['price_after_discount'] = self.price_after_discount
    #     print("invoice vals", invoice_vals)
    #     return invoice_vals
    