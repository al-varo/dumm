from odoo import models, api
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('price_unit')
    def _check_price_above_cost(self):
        for line in self:
            if line.product_id and line.price_unit < line.product_id.standard_price:
                raise ValidationError(
                    "Harga jual (%s) pada produk '%s' tidak boleh lebih rendah dari HPP (%s)." % (
                        line.price_unit, line.product_id.name, line.product_id.standard_price
                    )
                )
