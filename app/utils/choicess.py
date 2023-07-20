ORDER_STATUS = (
    ('A','Accepted'),
    ('C1','Completed'),
    ('C0','Canceled'),
    ('P','posted'),
    ('NP','not posted'),
)

PAYMENT_STATUS = (
    ('P', 'Paid'),
    ('TP', 'To Pay'),
    ('F', 'Failed')
)

PAYMENT_MODE = (
    ('',''),
    ('',''),
    ('',''),
    ('',''),
    ('',''),
)

PAYMENT_METHOD = (
    ('PP', 'PayPAl'),
)

DAYS = [

    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

from datetime import time

HOUR_OF_DAY_24 = [
    (time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in(0, 30)
]