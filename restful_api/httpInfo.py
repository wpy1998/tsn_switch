import requests
from requests.auth import HTTPBasicAuth

headers = {'Content-Type': 'application/json',
           "Accept": "application/json"}
auth = HTTPBasicAuth('admin', 'admin')

def get_info(url):
    print('request: ')
    resp = requests.get(url, headers=headers, auth=auth)
    result = resp.content
    print('response: ', result)
    return result

def put_info(url, jstr):
    print('request: ' + str(jstr))
    resp = requests.put(url, jstr, headers=headers, auth=auth)
    print('response: ', resp.content)

def delete_info(url):
    print('request: ')
    resp = requests.delete(url, headers=headers, auth=auth)
    print('response: ', resp.content)

def post_info(url, jstr):
    print('request: ' + str(jstr))
    resp = requests.post(url, jstr, headers=headers, auth=auth)
    print('response: ', resp.content)