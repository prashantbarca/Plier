#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Prashant Anantharaman <prashant.anantharaman@sri.com> %>
#
"""

"""
from convert_stream import *
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
np.set_printoptions(threshold='nan')

http_tmp = get_array('setpoint.pcap', 'http')
dnp3_tmp = get_array('captures/DNP3-TestDataPart1.pcap', 'DNP3')
mqtt_tmp = get_array('captures/mqtt_packets_tcpdump.pcap', 'MQTT')
http_dataset =  http_tmp[0][:19] + dnp3_tmp[0][:19] + mqtt_tmp[0]
http_target = http_tmp[1][:19] + dnp3_tmp[1][:19] + mqtt_tmp[1]
for i in range(20):
    rando = os.urandom(100)
    http_dataset.append(conv(rando))
    http_target.append("none")
vect = CountVectorizer(stop_words = None)
vect.fit(http_dataset)
simple_train_dtm = vect.transform(http_dataset)
#print simple_train_dtm.shape

clf = MultinomialNB().fit(simple_train_dtm, http_target)
#clf = GaussianNB().fit(simple_train_dtm, http_target)

def socket_receive():
    import sys
    import socket
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket to a public host,
        # and a well-known port
    serversocket.bind(("0.0.0.0", 20001))
        #become a server socket
    serversocket.listen(5)
    print "Ready to receive now"
    while 1:
        (clientsocket, address) = serversocket.accept()
        pcap_file = clientsocket.recv(65535)
        print pcap_file
        last = get_test_array(pcap_file.rstrip(), "")[0]
        actual_arr = get_test_array(pcap_file.rstrip(), "")[2]
        actual_array = get_actuals(pcap_file.rstrip(), actual_arr)
        #print last
        X_new_counts = vect.transform(last)
        predicted = clf.predict(X_new_counts)
        #print predicted
        clientsocket.sendall(str(repr((predicted, actual_array))))
    
socket_receive()

#print np.mean(simple_train_dtm)
#print simple_train_dtm.todense()

