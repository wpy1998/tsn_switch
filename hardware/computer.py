import socket
import json
import os
import time
import topology.detector as td
import topology.network_card as tn


def refresh():
    network_cards.clear()
    network_card_object = detector.get_local_interface()
    for key in network_card_object.keys():
        network_card = tn.NetworkCard(name=key, host_name=host_name)
        network_card.load_linux_object(network_card_object.get(key))
        network_cards.append(network_card)

def get_node_json():
    node = {}
    node['node-id'] = host_name + mac
    node['node-type'] = 'switch'
    node['id'] = mac.replace(":", "-")

    addresses = []
    address = {}
    addresses.append(address)
    address['id'] = 0
    address['first-seen'] = first_seen
    address['mac'] = mac.replace("-", ":")
    address['last-seen'] = int(time.time())
    address['ip'] = ip
    node['addresses'] = addresses

    termination_points = []
    node['termination-point'] = termination_points
    attachment_points = []
    node['attachment-points'] = attachment_points

    for network_card in network_cards:
        termination_points.append(network_card.get_termination_point_json())
        attachment_points.append(network_card.get_attachment_point_json())
    return node


def get_link_json():
    link = {}
    return link

topology_id = 'tsn-network'
host_name = socket.gethostname()
cuc_ip = "localhost"
urls = {
    'tsn-topology': "http://" + cuc_ip +
                    ":8181/restconf/config/network-topology:network-topology/",
    'tsn-listener': "http://" + cuc_ip +
                    ":8181/restconf/config/tsn-listener-type:stream-listener-config/devices/",
    'tsn-talker': "http://" + cuc_ip +
                  ":8181/restconf/config/tsn-talker-type:stream-talker-config/devices/"
}

first_seen = int(time.time())
port = 830
username = 'wpy'
password = '22003x'

network_cards = []
detector = td.Detector()
refresh()
ip = "0"
mac = ""
if(len(network_cards) != 0):
    ip = network_cards[0].ip
    mac = network_cards[0].mac