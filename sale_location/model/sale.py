from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    location = fields.Many2one('stock.location' ,string="Location")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()

        for order in self:
            # Group order lines by location
            location_lines = {}
            for line in order.order_line:
                if line.location:
                    if line.location.id not in location_lines:
                        location_lines[line.location.id] = self.env['sale.order.line']
                    location_lines[line.location.id] |= line

            # Log the grouped order lines by location for debugging
            _logger.info("Order %s: Location lines: %s", order.name, location_lines)

            # Process each location group
            for location_id, lines in location_lines.items():
                picking = self.env['stock.picking'].create({
                    'partner_id': order.partner_id.id,
                    'location_id': location_id,
                    'location_dest_id': order.partner_shipping_id.property_stock_customer.id,
                    'picking_type_id': self.env.ref('stock.picking_type_out').id,
                    'origin': order.name,
                })

                for line in lines:
                    self.env['stock.move'].create({
                        'name': line.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'location_id': location_id,
                        'location_dest_id': order.partner_shipping_id.property_stock_customer.id,
                        'picking_id': picking.id,
                        'sale_line_id': line.id,
                    })

                # Confirm and assign the picking
                picking.action_confirm()
                picking.action_assign()

        return res