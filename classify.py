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
np.set_printoptions(threshold='nan')

http_tmp = get_array('setpoint.pcap', 'http')
mqtt_tmp = get_array('captures/mqtt_packets_tcpdump.pcap', 'DNP3')
http_dataset =  http_tmp[0][:8] + mqtt_tmp[0]
http_target = http_tmp[1][:8] + mqtt_tmp[1]
for i in range(8):
    rando = os.urandom(100)
    http_dataset.append(conv(rando))
    http_target.append("none")
vect = CountVectorizer(stop_words = None)
vect.fit(http_dataset)
simple_train_dtm = vect.transform(http_dataset)
#print simple_train_dtm.shape

clf = MultinomialNB().fit(simple_train_dtm, http_target)
import sys
print get_test_array(sys.argv[1], "")
print get_array(sys.argv[1], "MQTT")

last = [http_dataset[1], http_dataset[2], http_dataset[10], http_dataset[11], http_dataset[-1], http_dataset[-2]]
X_new_counts = vect.transform(last)
predicted = clf.predict(X_new_counts)

for i in predicted:
    print i

#print np.mean(simple_train_dtm)
#print simple_train_dtm.todense()

