# __manifest__.py
{
    'name': 'Custom Invoice Layout',
    'version': '1.0',
    'category': 'Accounting',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'summary': 'Custom invoice layouts with different paper sizes.',
    'depends': ['account'],
    'data': [
        'views/invoice_template.xml',
        'reports/invoice_report.xml',
    ],
    'installable': True,
    'application': False,
}
