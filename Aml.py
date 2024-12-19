from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_value_per_item = fields.Monetary(
        string='Discount Value per Item',
        compute='_compute_discount_value_per_item',
        currency_field='currency_id',
        store=True,
    )

    @api.depends('product_id', 'price_unit', 'quantity')
    def _compute_discount_value_per_item(self):
        for line in self:
            # Ambil harga umum (list_price) dari produk
            standard_price = line.product_id.list_price or 0.0
            # Hitung nilai potongan per item (harga umum - harga unit)
            if standard_price > line.price_unit:
                line.discount_value_per_item = standard_price - line.price_unit
            else:
                line.discount_value_per_item = 0.0
