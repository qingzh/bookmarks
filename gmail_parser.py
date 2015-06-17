
import gmail
import re
import datetime
import os
import ConfigParser
import urllib2
import json
from ssl import SSLError

path = os.path.dirname(os.path.realpath(__file__))
conf_file = os.path.join(path, '..', 'gmail.conf')
conf_parser = ConfigParser.ConfigParser()
conf_parser.read(conf_file)
conf_dict = conf_parser.defaults()
USERNAME = conf_dict.get('username')
PASSWORD = conf_dict.get('password')
KEYWORD = conf_dict.get('keyword')
FROM = 'gnc.com'
OUTPUT_PREFIX = conf_dict.get('output')
AFTER = conf_dict.get('after')
BEFORE = conf_dict.get('before')

# Please Update
after = AFTER and datetime.datetime.strptime(AFTER, '%Y-%m-%d')
before = BEFORE and datetime.datetime.strptime(BEFORE, '%Y-%m-%d')


reg = re.compile(
    'Shipped To:(.*)(Shipping Method:.*)Cost Summary:(.*)Billed To',
    re.MULTILINE | re.DOTALL)
# Pattern.group()
# (1): shipping_method, (2): tracking_number
GNC_SHIPMENT_RE = re.compile(
    'Shipping Method: ([^\r\n]+)\r\nTracking Number: (\S+)',
    re.MULTILINE | re.DOTALL)
# Pattern.group()
# (1): name, (2): sku, (3): size, (4): dosage_forms, (5): quantity
GNC_ITEM_RE = re.compile(
    '([^\r\n]+)\r\nItem#: (\S+).*Size: (\S+) (\S+).*Quantity: (\S+)',
    re.MULTILINE | re.DOTALL)
# Pattern
# (1): subtotal, (2): shipping, (3):tax; sum(1,2,3)
GNC_COST_RE = re.compile(
    'Subtotal:\s*\$(\S+)\s+Shipping:\s*\$(\S+)\s+Tax:\s*\$(\S+)',
    re.MULTILINE)


class GNCOrder(object):

    def __init__(self, order=None, date=None, address=None, items=None,
                 cost=None, shipping_method=None, tracking_number=None,
                 **kwargs):
        '''
        unique by tracking number
        '''
        self.order = order
        self.shipping_method = shipping_method
        self.tracking_number = tracking_number
        self.items = items
        self.address = address
        self.cost = cost
        self.date = date
        self.weight, self.signature = get_fedex_info(self.tracking_number)

    def to_csv(self):
        """ csv:
        order, tracking_number, sku, name, quantity
        """
        item = self.items[0]
        csv = [
            '\t'.join(
                [self.order, self.tracking_number, self.weight, item.sku,
                 item.name, item.quantity, self.date, self.signature]
            )
        ]
        for item in self.items[1:]:
            csv.append(
                '\t'.join(
                    ['', '', '', item.sku, item.name,  item.quantity, '', ''])
            )
        return '\n'.join(csv)


class GNCItem(object):

    def __init__(self, name=None, sku=None, size=None, dosage_forms=None,
                 quantity=None, price=None, shipping_method=None, **kwargs):
        self.name = name
        self.sku = sku
        self.size = size
        self.quantity = quantity
        self.price = price
        self.shipping_method = shipping_method
        self.dosage_forms = dosage_forms


def parse_items(item_list):
    items = []
    for item, shipping_method, price in zip(*[iter(item_list)] * 3):
        # name, sku, size, dosage_forms, quantity
        match = GNC_ITEM_RE.search(item)
        items.append(
            GNCItem(*(match.groups() + (price, shipping_method)))
        )
    return items


'''
Multi Thread
(1): fetch mail
(2): parse mail
'''


def get_fedex_info(package, lbs_only=True):
    url_pattern = 'https://www.fedex.com/trackingCal/track?action=trackpackages&location=en_US&version=1&format=json&data={"TrackPackagesRequest":{"appType":"WTRK","uniqueKey":"","processingParameters":{},"trackingInfoList":[{"trackNumberInfo":{"trackingNumber":"%s","trackingQualifier":"","trackingCarrier":""}}]}}'
    try:
        response = urllib2.urlopen(url_pattern % package, timeout=50)
    except SSLError:
        return 'TIMEOUT'
    response_dict = json.loads(response.read())
    package_response = response_dict.get('TrackPackagesResponse')
    status_code = package_response.get('errorList')[0].get('code')
    if status_code != '0':
        return 'NULL'
    package_list = package_response.get('packageList')
    if lbs_only is True:
        weight = package_list[0].get('displayPkgLbsWgt', 'NULL')
    weight = package_list[0].get('displayPkgWgt', 'NULL')
    signature = package_list[0].get('statusWithDetails', 'NULL')
    return weight, signature


def parse_gnc(mails):
    orders = []
    for m in mails:
        mail = m.fetch()
        content = mail.get_payload()[0]
        match = reg.search(content.as_string())
        order, shipment, cost_summary = match.groups()
        order_info = order.strip().split('\r\n\r\n')
        shipping_method, tracking_number = GNC_SHIPMENT_RE.search(
            shipment).groups()

        orders.append(
            GNCOrder(
                order=mail.get('subject').rsplit('#')[-1].strip(),
                date=mail.get('date'),
                address=order_info[0],
                items=parse_items(order_info[1:]),
                shipping_method=shipping_method,
                tracking_number=tracking_number,
                cost=reduce(sum_, GNC_COST_RE.search(cost_summary).groups()),
            )
        )
    return orders


def write_file(prefix, orders, filter):
    today = datetime.date.today()
    with open('%s_%s.csv' % (prefix, today.strftime('%Y%m%d')), 'w') as f:
        for order in orders:
            if filter(order.address):
                f.write(order.to_csv() + '\n')


sum_ = lambda x, y: float(x) + float(y)
g = gmail.login(USERNAME, PASSWORD)

mails = g.label('SHOP/shipment').mail(
    after=after, sender=FROM, body=KEYWORD, before=before)

orders = parse_gnc(mails)
write_file(os.path.join(path, '..', OUTPUT_PREFIX), orders,
           filter=lambda t: KEYWORD.lower() in t.lower())
