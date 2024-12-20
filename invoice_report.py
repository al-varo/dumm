# reports/invoice_report.py
from odoo import models

class CustomInvoiceReport(models.AbstractModel):
    _name = 'report.my_invoice_custom.invoice_report'
    _description = 'Custom Invoice Report'

    def get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
        }

    def _get_report_name(self):
        return 'custom_invoice_template'

    def _get_page_size(self):
        # Example of custom paper size, you can define here like A4, Letter, etc.
        return 'A4'
