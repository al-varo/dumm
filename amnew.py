class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('line_ids.price_subtotal', 'line_ids.price_tax')
    def _compute_amount(self):
        """
        Override perhitungan total faktur untuk memastikan fixed discount diperhitungkan.
        """
        for move in self:
            amount_untaxed = sum(line.price_subtotal for line in move.line_ids)
            amount_tax = sum(line.price_tax for line in move.line_ids)
            move.amount_untaxed = amount_untaxed
            move.amount_tax = amount_tax
            move.amount_total = amount_untaxed + amount_tax
