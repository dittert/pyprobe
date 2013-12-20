import requests
import json
import prtg.descriptions

from utils import GID

obj = [prtg.SensorDescription()]

payload = {
    'gid': GID,
    'key': '93e60af857ef87036e1d2608977238931e1a1d10',
    'protocol': '1',

    'name': 'macpro',
    'version': '1',
    'baseinterval': '300',
    'sensors': json.dumps(obj, cls=prtg.DescriptionJSONEncoder)
}

print("Registering with:\n")
print(print(json.dumps(obj, indent=2, cls=prtg.DescriptionJSONEncoder)))
print("\n")


#r = requests.post('https://oversight.intern.2o4.de/probe/announce', data=payload)
#
#print(r.text)
#print(r.status_code)


