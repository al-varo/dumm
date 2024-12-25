from odoo import models, api
from odoo.exceptions import ValidationError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.constrains('price_unit')
    def _check_price_above_cost(self):
        for line in self:
            if line.move_id.move_type in ['out_invoice', 'out_refund'] and line.product_id:
                if line.price_unit < line.product_id.standard_price:
                    raise ValidationError(
                        "Harga jual (%s) pada produk '%s' di faktur tidak boleh lebih rendah dari HPP (%s)." % (
                            line.price_unit, line.product_id.name, line.product_id.standard_price
                        )
                    )
