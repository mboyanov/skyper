#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys
from collections import defaultdict
import re

con = None


class skyper:
    def __init__(self, username):
        self.wordlist = defaultdict(lambda: defaultdict(lambda: 0))  #for each word a list of documents it appears in together with the number of occurences
        self.totalcounts = defaultdict(lambda: 0)  #for each word how many times it appears in total
        self.documentcounts = defaultdict(lambda: 0)
        self.username = username



    def parseData(self):
        con = lite.connect(
            '/media/A6D87067D870379F/Users/xaxamy/AppData/Roaming/Skype/' + str(self.username) + '/main.db')
        cur = con.cursor()
        cur.execute(
            'select DISTINCT dialog_partner from messages WHERE dialog_partner!=\'None\' group by dialog_partner HAVING COUNT(body_xml)>100 ORDER BY COUNT(body_xml) ;')
        data = cur.fetchall()
        for user in data:
            text = ''
            cur.execute('select * from messages WHERE dialog_partner=\'' + str(user[0]) + '\';')
            userdata = cur.fetchall()
            for i in userdata:
                try:
                    text += ' ' + i[17]

                except:
                    continue

            words = re.split("[.\s,?!()\[\]<>]+", text)
            words = [words[i].lower() for i in range(0, len(words) - 1)]
            self.documentcounts[user[0]] = len(words)
            for word in words:
                self.wordlist[word][user[0]] += 1
                self.totalcounts[word] += 1
        print 'Parsing Complete'


    def getData(self):
        con = lite.connect(
            '/media/A6D87067D870379F/Users/xaxamy/AppData/Roaming/Skype/' + str(self.username) + '/main.db')
        cur = con.cursor()
        cur.execute(
            'select dialog_partner,COUNT(body_xml) from messages WHERE dialog_partner!=\'None\' group by dialog_partner HAVING COUNT(body_xml)>100 ORDER BY COUNT(body_xml) ;')
        data = cur.fetchall()
        skypepartners = {}

        for d in data:
            skypepartners[d[0]] = d[1]

        print("%s" % data)
        suma = 0
        cur.execute('select duration,current_video_audience from calls WHERE duration>0;')
        calls = cur.fetchall()
        print len(calls)
        for call in calls:
            partners = call[1].split()
            for partner in partners:
                partner=partner
                try:
                    skypepartners[partner] = skypepartners[partner] + call[0] / 60 * 25
                except:
                    continue
        for skypepartner in skypepartners:
            suma += skypepartners[skypepartner]
        for skypepartner in skypepartners:
            skypepartners[skypepartner] = 1.0 * skypepartners[skypepartner] / suma * 400
        print("SQLite version: %s" % data)
        return skypepartners

    def getInfo(self,partner):
        result=[]
        print self.documentcounts
        print partner.encode('utf-8')
        if partner not in self.documentcounts:
            result = None
        if partner.encode('utf-8') in self.documentcounts:
            partner=partner.encode('utf-8')
        for word in self.wordlist:
            if self.wordlist[word][partner]>0.8*self.totalcounts[word] and self.totalcounts[word]>5:
               result.append(word)
        print result
        return result


# t=skyper('xaxamy')
# t.getData()
# t.parseData()
# import operator
# sorted_x = sorted(t.totalcounts.iteritems(), key=operator.itemgetter(1))
#
# for partner in t.documentcounts:
#     for word in t.wordlist:
#         if t.wordlist[word][partner]>0.8*t.totalcounts[word] and t.totalcounts[word]>5:
#             print word,partner