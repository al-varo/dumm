from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    fixed_discount = fields.Monetary(string="Fixed Discount", currency_field='currency_id', default=0.0)

    @api.depends('price_unit', 'quantity', 'discount', 'fixed_discount', 'tax_ids')
    def _compute_amount(self):
        """
        Override bawaan Odoo untuk menghitung subtotal dan pajak dengan fixed discount.
        """
        for line in self:
            # Hitung subtotal sebelum diskon
            subtotal_undiscounted = line.quantity * line.price_unit

            # Hitung subtotal setelah diskon persentase
            subtotal_discounted = subtotal_undiscounted * (1 - (line.discount / 100.0))

            # Kurangi dengan fixed discount
            subtotal_with_fixed_discount = subtotal_discounted - line.fixed_discount
            line.price_subtotal = max(subtotal_with_fixed_discount, 0.0)

            # Hitung pajak
            taxes = line.tax_ids.compute_all(
                subtotal_with_fixed_discount,
                currency=line.currency_id,
                quantity=1.0,
                product=line.product_id,
                partner=line.move_id.partner_id
            )
            line.price_total = taxes['total_included']
            line.price_tax = taxes['total_included'] - taxes['total_excluded']
