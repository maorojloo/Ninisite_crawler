from fake_useragent import UserAgent
import requests
import concurrent.futures
import random

proxies_list = proxies= [
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10001',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10002',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10003',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10004',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10005',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10006',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10007',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10008',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10009',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10010',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10011',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10012',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10013',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10014',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10015',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10016',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10017',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10018',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10019',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10020',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10021',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10022',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10023',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10024',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10025',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10026',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10027',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10028',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10029',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10030',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10031',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10032',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10033',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10034',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10035',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10036',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10037',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10038',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10039',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10040',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10041',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10042',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10043',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10044',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10045',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10046',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10047',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10048',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10049',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10050',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10051',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10052',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10053',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10054',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10055',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10056',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10057',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10058',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10059',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10060',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10061',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10062',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10063',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10064',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10065',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10066',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10067',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10068',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10069',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10070',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10071',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10072',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10073',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10074',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10075',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10076',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10077',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10078',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10079',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10080',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10081',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10082',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10083',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10084',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10085',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10086',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10087',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10088',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10089',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10090',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10091',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10092',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10093',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10094',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10095',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10096',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10097',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10098',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10099',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'},
        {'http': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@ddc.smartproxy.com:10100',
        'https': 'http://sp1ushqvsj:c6oy6kR=m1KZd5fThg@dc.smartproxy.com:10001'}
        ]


uri = 'https://www.ninisite.com/discussion/topic/'

ua = UserAgent()

def send_request():
    proxies = random.choice(proxies_list)
    identity = {'User-Agent': ua.random}
    headers = identity
    url=uri+str(random.randint(3000000, 4000000))

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        #print(f"Request sent using proxy and identity {identity}. Status code: {response.status_code}")
        print(proxies["http"],response.status_code)
    except requests.exceptions.RequestException as e:
        pass
       # print(f"Error with proxy  and identity {identity}: {e}")

# Main function to run requests in parallel
def main():
    # Number of concurrent requests
    num_concurrent_requests = 500

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        futures = [executor.submit(send_request) for _ in range(num_concurrent_requests)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()
