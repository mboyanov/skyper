#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys
from collections import defaultdict
import re
con = None

class skyper:

    def __init__(self):
      self.wordlist=defaultdict(lambda:defaultdict(lambda:0)) #for each word a list of documents it appears in together with the number of occurences
      self.totalcounts=defaultdict(lambda:0) #for each word how many times it appears in total
      self.documentcounts=defaultdict(lambda:0)

    def parseData(self,username):
        con = lite.connect('/media/A6D87067D870379F/Users/xaxamy/AppData/Roaming/Skype/'+str(username)+'/main.db')
        cur = con.cursor()
        cur.execute('select DISTINCT dialog_partner from messages WHERE dialog_partner!=\'None\' group by dialog_partner HAVING COUNT(body_xml)>100 ORDER BY COUNT(body_xml) ;')
        data = cur.fetchall()
        for user in data:
            text=''
            cur.execute('select * from messages WHERE dialog_partner=\''+str(user[0])+'\';')
            userdata = cur.fetchall()
            for i in userdata:
              try:
                text+= ' ' +i[17]
              except:
                  continue

            words=re.split("[.\s,?!()\[\]<>]+",text)
            words=[words[i].lower() for i in range(0,len(words)-1) ]
            self.documentcounts[user]=len(words)
            for word in words:
              self.wordlist[word][user]+=1
              self.totalcounts[word]+=1



    def getData(self,username):
        con = lite.connect('/media/A6D87067D870379F/Users/xaxamy/AppData/Roaming/Skype/'+str(username)+'/main.db')
        cur = con.cursor()
        cur.execute('select dialog_partner,COUNT(body_xml) from messages WHERE dialog_partner!=\'None\' group by dialog_partner HAVING COUNT(body_xml)>100 ORDER BY COUNT(body_xml) ;')
        data = cur.fetchall()
        skypepartners={}
        for d in data:
            skypepartners[d[0]]=d[1]

        print("SQLite version: %s" % data)
        suma=0
        cur.execute('select duration,current_video_audience from calls WHERE duration>0;')
        calls=cur.fetchall()
        print len(calls)
        for call in calls:
            partners=call[1].split()
            for partner in partners:
                try:
                    skypepartners[partner]=skypepartners[partner]+call[0]/60*100
                except:
                    continue
        for skypepartner in skypepartners:
            suma+=skypepartners[skypepartner]
        for skypepartner in skypepartners:
            skypepartners[skypepartner]=1.0*skypepartners[skypepartner]/suma*400
        print("SQLite version: %s" % data)
        return skypepartners


    #import easygui as eg
    #name=eg.enterbox("Please Enter your Skype username")
    #if (name):
      #con = lite.connect('/media/A6D87067D870379F/Users/xaxamy/AppData/Roaming/Skype/'+str(name)+'/main.db')
      #cur = con.cursor()
      #cur.execute('select dialog_partner,COUNT(body_xml) from messages WHERE dialog_partner!=\'None\' group by dialog_partner HAVING COUNT(body_xml)>100 ORDER BY COUNT(body_xml) ;')
      #data = cur.fetchall()

      #print("SQLite version: %s" % data)
      #suma=0
      #for d in data:
	  #suma+=d[1]
      #for i in range(len(data)):
	  #data[i]=(data[i][0],1.0*data[i][1]/suma*500)
      #print("SQLite version: %s" % data)

      #import pygame
      #import sys


      #pygame.init()
      #screen = pygame.display.set_mode((1280,768))
      #screen.fill((255,255,255))
      #myfont = pygame.font.SysFont("monospace", 15)
      #y=200
      #locs=[]
      #sumr=0
      #for i in range(len(data)):
	#if sumr>1024:
	  #sumr=0
	  #y+=200
	#sumr+=max(2*int(data[i][1]),100)
	#pygame.draw.circle(screen, (100,100,100), (sumr,y), int(data[i][1]), 0)
	#locs.append((sumr-30,y))
      #for i in range(len(data)):
	#label = myfont.render(data[i][0], 12, (0,0,0))
	#screen.blit(label, locs[i])
      #pygame.display.update()
      #pygame.image.save(screen,'haha.jpg')

     # choic   = eg.choicebox(msg, title, choices,image=image)

# myskyper=skyper()
# myskyper.parseData('xaxamy')
# totalcounts=myskyper.totalcounts
# import operator
# sorted_counts = sorted(totalcounts.iteritems(), key=operator.itemgetter(1))
# for i in sorted_counts[-200:-100]:
#   print i[0].encode('utf-8'),i[1]

#finally:

    #if con:
        #con.close()
