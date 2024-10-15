from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    quotation_expiry_notification = fields.Boolean(
        string="Quotation Expiry Notification", config_parameter="Email_template.quotation_expiry_notification"
    )

    quotation_expiry_date = fields.Integer(
        string="Quotation Expiry Days", config_parameter="Email_template.quotation_expiry_date"
    )

    quotation_expiry_manager_id = fields.Many2one(
        'res.users', string="Expiry Quotation Manager"
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sale.quotation_expiry_notification', self.quotation_expiry_notification)
        self.env['ir.config_parameter'].sudo().set_param('sale.quotation_expiry_date', self.quotation_expiry_date)
        self.env['ir.config_parameter'].sudo().set_param('sale.quotation_expiry_manager_id', self.quotation_expiry_manager_id.id if self.quotation_expiry_manager_id else False)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        manager_id = self.env['ir.config_parameter'].sudo().get_param('sale.quotation_expiry_manager_id', default=False)
        res.update({
            'quotation_expiry_notification': self.env['ir.config_parameter'].sudo().get_param('sale.quotation_expiry_notification', default=False),
            'quotation_expiry_date': int(self.env['ir.config_parameter'].sudo().get_param('sale.quotation_expiry_date', default=0)),
            'quotation_expiry_manager_id': int(manager_id) if manager_id else False,
        })
        return res
