import datetime
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'

def add(items, title, amount, expiration_date=None):

    if expiration_date is not None:
        expiration_date = datetime.datetime.strptime(expiration_date, DATE_FORMAT).date()
    
    if title not in items:
        items[title] = []

    new_batch = {
        'amount': amount,
        'expiration_date' : expiration_date
    }
    items[title].append(new_batch)

def add_by_note(items, note):

    parts = note.split()

    try:
        datetime.datetime.strptime(parts[-1], DATE_FORMAT)

        expiration_date = parts[-1]
        amount = Decimal(parts[-2])
        title = ' '.join(parts[:-2])

    except ValueError:
        expiration_date = None
        amount = Decimal(parts[-1])
        title = ' '.join(parts[:-1])

    add(items, title, amount, expiration_date)


def find(items, needle):

    result = []
    needle_lower = needle.lower()

    for title in items:

        if needle_lower in title.lower():
            result.append(title)

    return result

#
def get_amount(items, needle):
    
    product_amount = Decimal('0')

    for found_title in find(items, needle):
        for part in items[found_title]:
            product_amount += part['amount']

    return product_amount

def get_expired(items, in_advance_days=0):
    result = []
    today = datetime.date.today()
    threshold = today + datetime.timedelta(days=in_advance_days)

    for title, parts in items.items():
        amount = Decimal('0')
        
        for part in parts:
            exp_date = part['expiration_date']
            if exp_date is not None and exp_date <= threshold:
                amount += part['amount']
        
        if amount > 0:
            result.append((title, amount))

    return result

goods = {
    'Пельмени Универсальные': [
        {'amount': Decimal('0.5'), 'expiration_date': datetime.date(2023, 7, 15)},
        {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 1)},
    ],
    'Вода': [
        {'amount': Decimal('1.5'), 'expiration_date': None}
    ],
}


