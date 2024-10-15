{
    'name':'Expense',
    'author':'Odoo ',
    'website':'www.odoo.tech',
    'summary':'Oddo 16 Development',
    'depends':['mail',
                'base',
                'sale',
                'product',
                'account'
            ],
              
    'data' :[
        
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/customs.xml',
        'views/menu.xml',
        'views/invoice.xml',
        'report/ir_actions_report.xml',
        'report/expense_report.xml',    ]
}