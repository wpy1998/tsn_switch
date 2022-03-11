#!/usr/bin/python
import requests
import os
import json
from requests.auth import HTTPBasicAuth

headers = {'Content-Type': 'application/json',
           "Accept": "application/json"}
auth = HTTPBasicAuth('admin', 'admin')

def get_info(url):
    print('request: ' + url)
    resp = requests.get(url, headers=headers, auth=auth)
    print('response: ', resp.content)

def put_info(url, jstr):
    print('request: ' + url)
    resp = requests.put(url, jstr, headers=headers, auth=auth)
    print('response: ', resp.content)

def delete_info(url):
    print('request: ' + url)
    resp = requests.delete(url, headers=headers, auth=auth)
    print('response: ', resp.content)

def post_info(url, jstr):
    resp = requests.post(url, jstr, headers=headers, auth=auth)
    print('response: ', resp.content)

def get_neightbor(network_card_name):
    fp = os.popen('lldpcli show neighbor ports ' + network_card_name + ' summary -f json')
    result = fp.read()
    try:
        object = json.loads(result).get('lldp').get('interface')
    except:
        object = json.loads(result).get('lldp').get('interface').get(0)
    print(object)

if __name__ == "__main__":
    url = 'http://localhost:8181/restconf/operational/network-topology:network-topology'
    # get_info(url)

    fp = os.popen("lldpcli show interface -f json",)
    result = fp.read()
    object = json.loads(result)
    array = object.get('lldp').get('interface')
    try:
        network_card_name = ''
        for var in array:
            network_card_name = var
        via = array.get('var')
        if via != 'lldp':
            print("there is no possible network card")
        print(via)
    except:
        for network_card in array:
            network_card_name = ''
            for var in network_card:
                network_card_name = var
            via = network_card.get('var')
            if via != 'lldp':
                continue
            print(via)
