from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    fixed_discount = fields.Float(string="Fixed Discount", default=0.0)

    @api.onchange('fixed_discount', 'price_unit', 'quantity')
    def _compute_discounted_price(self):
        for line in self:
            if line.fixed_discount:
                # Hitung subtotal setelah diskon tetap
                total = (line.price_unit * line.quantity) - line.fixed_discount
                line.price_subtotal = total if total > 0 else 0.0
            else:
                # Gunakan perhitungan bawaan jika diskon tetap 0
                line.price_subtotal = line.price_unit * line.quantity

    @api.depends('price_subtotal', 'tax_ids')
    def _compute_all_prices(self):
        """
        Perhitungan pajak bawaan Odoo akan tetap berlaku, 
        kita hanya mengubah subtotal sebelum pajak.
        """
        super(AccountMoveLine, self)._compute_all_prices()
