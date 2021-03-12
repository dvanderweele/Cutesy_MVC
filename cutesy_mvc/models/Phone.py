from ..helpers.model import Model

class Phone(Model):
    table = 'phone'
    relations = {
        'type': 'belongsTo',
        'model': 'Customer',
        'default': {
            'id': 0,
            'name': '<unassigned>'
        }
    }
    def __str__(self):
        return f'PHONE: id — {self["id"]}, IMEI — {self["IMEI"]}, customer_id — {self["customer_id"]}'