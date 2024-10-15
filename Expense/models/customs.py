from odoo import api,fields,models
from odoo.exceptions import ValidationError

class ExpenseVoucher(models.Model):
    _name = "custom.expense"

    _description = "Expense Records"

    name = fields.Many2one('res.partner',string="Name")
    ref = fields.Char(string="Reference:", default=lambda self:('New'))
    age = fields.Integer(string="Age")
    gender = fields.Selection([('male','Male'),('female','Female')],string="Gender")
    phone = fields.Char(string="Phone no")
    product_ids = fields.One2many(comodel_name ="product.list",inverse_name ="cust_id",string ="product")
    total = fields.Integer(compute="_total_price",string="Total Amount$", store=True)
    invoice_count = fields.Integer(string="invoice count:",compute="_compute_invoice_count")
    discount = fields.Float(string='Discount Amount')
    price_after_discount=fields.Integer(string="Subtotal")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
                    ], string="Status")
    
    discount_type = fields.Selection([
        ('percentage', 'percentage'),
        ('Fixed','Fixed'),
    ], string='Selection Field')
    
    @api.model_create_multi
    def create(self,val):
        for vals in val:
            vals['ref']=self.env['ir.sequence'].next_by_code('custom.expense')
            print(vals)
        return super(ExpenseVoucher,self).create(val)

    @api.onchange('discount')
    def _onchange_discount(self):
        for line in self:
            if line.discount_type =='Fixed':
                if line.discount >= 0:
                    line.price_after_discount = line.total - line.discount
            elif line.discount_type =='percentage':
               
               line.price_after_discount = line.total * (line.discount / 100) 
               line.price_after_discount = (line.discount / 100) + line.total

            else:
                line.price_after_discount=0.0
    
    @api.depends('invoice_count')
    def _compute_invoice_count(self):
            
            self.invoice_count = self.env['account.move'].search_count([('coupen', '=', self.id)])

    
    def action_confirm(self):
        invoice_vals = {
            'move_type': 'out_invoice',
            'invoice_user_id': self.env.user.id,
            'partner_id': self.name.id,
            'coupen':self.id,
            'price_after_discount': self.price_after_discount,

        }
        invoice_line_ids = []
        for line in self.product_ids:
            invoice_line_ids += [(0, 0, {
                'name': 'll',
                'price_unit': line.price,
                'quantity': line.quantity,
                'product_id': line.products_id.id,
                
            })]
            
        invoice_vals['invoice_line_ids'] = invoice_line_ids
        self.env['account.move'].sudo().create(invoice_vals)
        
       
        self.state = "confirm"
        return
 
                


    def action_view_invoice(self):
        view_id = self.env['account.move'].search([('coupen','=',self.id)])
        return {
            'type':'ir.actions.act_window',
            'name': ('invoice'),
            'domain':[('coupen','=',self.id)],
            'res_model':'account.move',
            'view_mode':'tree,form',
            'view_type':'form',
            # 'res_id':view_id.id

        }           
    @api.depends('product_ids')
    def _total_price(self):
        for record in self:
            record.total = sum(record.product_ids.mapped('price')) 

    # def my_button_function(self):
    #     invoice_vals = {
    #         'move_type': 'out_invoice',
    #         'invoice_user_id': self.env.user.id,
    #         'partner_id': self.name.id,
    #     }
    #     invoice_line_ids = []
    #     for line in self.product_ids:
    #         invoice_line_ids += [(0, 0, {
    #             'name': 'll',
    #             'price_unit': line.price,
    #             'quantity': line.quantity,
    #             'product_id': line.products_id.id,
    #         })]
            
    #     invoice_vals['invoice_line_ids'] = invoice_line_ids
    #     inv = self.env['account.move'].sudo().create(invoice_vals)
    #     inv.action_post()

    
       
class ProductList(models.Model):
    _name = "product.list"


    products_id = fields.Many2one('product.product',string="product")
    cust_id = fields.Many2one("custom.expense")
    quantity = fields.Integer(string="Quantity",default=1)
    delivered = fields.Integer(string="Delivered")
    price = fields.Float(string="Price",compute="_update_quantity")
    unit_price = fields.Float(string='Unit Price', compute='_compute_unit_price',related='products_id.lst_price' ,store=True)
    # discount_price = fields.Float(string="discount")
    # discount= fields.Float(string='Discount')
    
    
    @api.depends('lst_price')
    def _compute_unit_price(self):
        for products_id in self:
            products_id.unit_price = products_id.lst_price

        
    @api.depends('products_id','quantity')
    def _update_quantity(self):
            for record in self: 
                record.price = (record.quantity * record.products_id.lst_price)
      
    
    
    


                

   
    