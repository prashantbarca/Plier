#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Prashant Anantharaman <prashant.anantharaman@sri.com> %>
#
"""

"""
import pyshark
import numpy as np
import os
import pcap
import dpkt
from dpkt.ip import IP
from dpkt.tcp import TCP
from dpkt.http import Request
from dpkt.http import Response

def conv(string):
    tmpstr = ""
    for char in string:
        tmpstr = tmpstr + hex(ord(char)) + " "
    return tmpstr.decode("utf-8", "ignore")

def get_array_i(pcap_file, proto):
    arr = []
    cap = pyshark.FileCapture(pcap_file)
    i = 0
    for pkt in cap:
        i = i + 1
        try:
          #print pkt['MQTT']
            if pkt[proto]:
                arr.append(i)
        except:
            continue
    return arr

# pcap = pcap.pcap('/home/prashant/Downloads/setpoint.pcap')
def get_test_array(pcap_file, proto):
    labels = []
    arra = []
    pcapa = pcap.pcap(pcap_file)

    for ts, pkt in pcapa:
        try:
            ether = Ethernet(pkt)
            ip = ether.data
            if isinstance(ip, str):
                ip = IP(ether.data)
        except Exception as e:
            try:
                ip = IP(pkt)
            except:
                continue
        if isinstance(ip.data, str):
            tcp = TCP(ip.data)
        else:
            tcp = ip.data
        tmpstr = ""
        #tmparr = []
        arra.append(conv(tcp.data))
        labels.append(proto)
    return (arra, labels)


def get_array(pcap_file, proto):
    labels = []
    arr = get_array_i(pcap_file, proto)
    arra = []
    pcapa = pcap.pcap(pcap_file)

    i = 0
    for ts, pkt in pcapa:
        i = i + 1
        if i not in arr:
            continue
        try:
            ether = Ethernet(pkt)
            ip = ether.data
            if isinstance(ip, str):
                ip = IP(ether.data)
        except Exception as e:
            try:
                ip = IP(pkt)
            except:
                continue
        tcp = ip.data
        if isinstance(tcp, str):
            print tcp.encode("hex")
            tcp = TCP(tcp)
        else:
            print str(tcp).encode("hex")
        #tmparr = []
        arra.append(conv(tcp.data))
        labels.append(proto)
    return (arra, labels)

#print get_array("captures/mqtt_packets_tcpdump.pcap", "MQTT")
