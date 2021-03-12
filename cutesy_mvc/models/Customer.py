from ..helpers.model import Model

class Customer(Model):
    table = 'customer'
    relations = {
        'phone': {
            'type':'hasOne',
            'model': 'Phone',
            'default': {
                'id': 0,
                'IMEI': 0,
                'customer_id': 0,
                'created_at': 1.1,
                'updated_at': 2.1
            }
        }
    }
    
    def __str__(self):
        return f'CUSTOMER: id — {self["id"]}, name — {self["name"]}'