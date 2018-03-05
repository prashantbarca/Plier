#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Prashant Anantharaman <prashant.anantharaman@sri.com> %>
#
"""

"""
import sys
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

# pcap = pcap.pcap('/home/prashant/Downloads/setpoint.pcap')
def get_array(pcap_file, proto):
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
        print tcp.data.encode("hex")
        
proto = sys.argv[2]
pcap_file = sys.argv[1]
get_array(pcap_file, proto)
