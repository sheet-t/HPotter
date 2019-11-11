import re
import requests
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
hostname = '127.0.0.1'
data = b'test'
url = 'https://127.0.0.1'

try:

	response = requests.post(url, data=data, verify=False)

	resp = re.sub('<[^<]+?>', '', response.content.decode('utf-8'))

	if response.status_code == 200:
		print("Response [{}]".format(response.status_code))
		print(resp)
	else:
		print("no response received")
except (Exception, ConnectionError) as exc:
	print("Is HPotter running?\n{}".format(exc))