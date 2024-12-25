# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    amount_discount = fields.Monetary(
        string='Nilai Discount',
        compute='_compute_amount_discount',
        currency_field='currency_id',
        store=True,
    )
    
    saved_lst_price = fields.Monetary(
        string='Saved List Price',
        currency_field='currency_id',
        store=True,
    )

    @api.depends('product_id', 'price_unit', 'quantity', 'product_id.lst_price', 'discount', 'move_id.move_type')
    def _compute_amount_discount(self):
        for line in self:
            # Skip invalid entries early for better readability
            if not line.move_id or not line.product_id or not line.product_uom_id:
                line.amount_discount = 0.0
                continue
            
            # Ensure move_id type is valid before proceeding
            if line.move_id.move_type not in ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']:
                line.amount_discount = 0.0
                continue
            
            # Get basic data for discount calculation
            price = line.price_unit or 0.0
            quantity = line.quantity or 0.0
            discounted_price = price * (1 - (line.discount or 0.0) / 100.0)

            # Discount calculation for sales (out_invoice, out_refund)
            if line.move_id.move_type in ['out_invoice', 'out_refund']:
                # If it's an out_refund, use saved_lst_price, otherwise save lst_price
                if line.move_id.move_type == 'out_refund' and line.saved_lst_price:
                    standard_price = line.saved_lst_price
                else:
                    # Save lst_price for out_invoice or the first out_refund
                    if not line.saved_lst_price:
                        line.saved_lst_price = line.product_id.lst_price or 0.0
                    standard_price = line.saved_lst_price

                # Adjust for UOM factor
                uom_factor = line.product_uom_id.factor or 1.0
                standard_price /= max(uom_factor, 1.0)  # Avoid division by zero
                discount_value = (standard_price - discounted_price) * quantity
            # Discount calculation for purchases (in_invoice, in_refund)
            elif line.move_id.move_type in ['in_invoice', 'in_refund']:
                discount_value = discounted_price * quantity
            else:
                discount_value = 0.0  # Fallback case for unsupported move types

            # Ensure non-negative discount value
            line.amount_discount = max(discount_value, 0.0)
