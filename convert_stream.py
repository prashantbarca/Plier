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
            if pkt[proto]:
                arr.append(i)
        except:
            continue
    return arr

# pcap = pcap.pcap('/home/prashant/Downloads/setpoint.pcap')
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
        if isinstance(tcp, str) or not tcp.data:
            continue
        try:
            tmpstr = ""
            #tmparr = []
            arra.append(conv(tcp.data))
            labels.append(proto)
            rando = os.urandom(100)
            arra.append(conv(rando))
            labels.append("none")
            #arra.append(tmparr)
            #print arr
        except Exception as e:
            print e
            continue
    return (arra, labels)
