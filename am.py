from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    total_discount = fields.Monetary(
        string="Total Discount",
        compute="_compute_totals_with_discount",
        store=True
    )
    amount_untaxed = fields.Monetary(
        string="Subtotal (Tax Excluded)",
        compute="_compute_totals_with_discount",
        store=True
    )
    amount_tax = fields.Monetary(
        string="Taxes",
        compute="_compute_totals_with_discount",
        store=True
    )
    amount_total = fields.Monetary(
        string="Total (Tax Included)",
        compute="_compute_totals_with_discount",
        store=True
    )

    @api.depends('invoice_line_ids', 'invoice_line_ids.price_unit', 'invoice_line_ids.quantity',
                 'invoice_line_ids.discount', 'invoice_line_ids.fixed_discount', 'invoice_line_ids.tax_ids')
    def _compute_totals_with_discount(self):
        for move in self:
            total_discount = 0.0
            amount_untaxed = 0.0
            amount_tax = 0.0
            amount_total = 0.0

            for line in move.invoice_line_ids:
                # Diskon persentase
                discount_percent = (line.price_unit * line.quantity) * (line.discount / 100)
                # Diskon tetap
                discount_fixed = line.fixed_discount
                # Total diskon per baris
                line_discount = discount_percent + discount_fixed
                total_discount += line_discount

                # Subtotal baris (harga setelah diskon)
                line_subtotal = (line.price_unit * line.quantity) - line_discount
                amount_untaxed += line_subtotal

                # Pajak baris (gunakan logika pajak bawaan Odoo)
                taxes = line.tax_ids.compute_all(line_subtotal, currency=move.currency_id, quantity=1.0)['taxes']
                amount_tax += sum(tax['amount'] for tax in taxes)

            # Hitung total akhir
            amount_total = amount_untaxed + amount_tax

            # Simpan nilai
            move.total_discount = total_discount
            move.amount_untaxed = amount_untaxed
            move.amount_tax = amount_tax
            move.amount_total = amount_total
