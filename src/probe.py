import requests

from utils import GID

getpayload = {
    'gid': GID,
    'key': '93e60af857ef87036e1d2608977238931e1a1d10',
    'protocol': '1',
}

r = requests.get('https://oversight.intern.2o4.de/probe/tasks', params=getpayload)
print(r.text)
print(r.status_code)
