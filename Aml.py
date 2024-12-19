from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_fixed = fields.Float(string="Fixed Discount", default=0.0)
    subtotal_before_discount = fields.Monetary(string="Subtotal Before Discount", compute="_compute_subtotal_before_discount", store=True)

    @api.depends('price_unit', 'quantity')
    def _compute_subtotal_before_discount(self):
        for line in self:
            line.subtotal_before_discount = line.price_unit * line.quantity

    @api.depends('discount_fixed', 'subtotal_before_discount', 'discount', 'tax_ids')
    def _compute_amount(self):
        for line in self:
            # Perhitungan diskon tetap
            price_subtotal = line.subtotal_before_discount - line.discount_fixed
            if line.discount:
                price_subtotal -= price_subtotal * (line.discount / 100.0)
            
            line.price_subtotal = price_subtotal
            line.price_total = line.tax_ids.compute_all(price_subtotal, line.move_id.currency_id, line.quantity)['total_included']

class AccountMove(models.Model):
    _inherit = 'account.move'

    total_discount = fields.Monetary(string="Total Discount", compute="_compute_total_discount", store=True)

    @api.depends('invoice_line_ids.discount_fixed', 'invoice_line_ids.discount', 'invoice_line_ids.price_unit', 'invoice_line_ids.quantity')
    def _compute_total_discount(self):
        for move in self:
            move.total_discount = sum(line.discount_fixed for line in move.invoice_line_ids)
