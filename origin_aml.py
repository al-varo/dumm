# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    disc_value_item = fields.Monetary(
        string='Nilai Disc Item',
        compute='_compute_disc_value',
        currency_field='currency_id',
        store=True,
    )
    
    disc_value_subtotal = fields.Monetary(
        string='Nilai Discount',
        compute='_compute_disc_value',
        currency_field='currency_id',
        store=True,
    )

    @api.depends('product_id', 'price_unit', 'quantity', 'product_id.lst_price', 'discount')
    def _compute_disc_value(self):
        for line in self:  # Iterasi untuk setiap record dalam recordset
            # Ambil harga umum (list_price) dari produk
            standard_price = (line.product_id.lst_price or 0.0) / (line.product_uom_id.factor or 1)
            # Potong harga line dulu jika kolom disc di isi
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            # Hitung nilai potongan per item (harga umum - harga unit)
            if standard_price > price:
                line.disc_value_item = standard_price - price
                line.disc_value_subtotal = line.disc_value_item * line.quantity
            else:
                line.disc_value_item = 0.0
                line.disc_value_subtotal = 0.0
