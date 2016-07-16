# -*- coding: utf-8 -*-
import requests
import time
import os
import codecs
import re

class ChanceDeGol:

  def __init__(self):
    self.clubs_prob = self.obter_clubs_prob()

  def save_cache(self, filename, content):
    with codecs.open(filename, 'wb', 'latin1') as f:
      f.write(content)
  
  def read_from_cache(self, filename):
    content = None
    with codecs.open(filename, 'rb', 'latin1') as f:
      content = f.read()
    return content

  def cached(self, filename):
    return os.path.isfile(filename)
    
  def __get_prob_next_matches(self):
    data = ''
    cache_name = os.path.join("./cache", "chance_de_gol_%s.cache" %(time.strftime("%d-%m-%Y")))
    if (self.cached(cache_name)):
      data = self.read_from_cache(cache_name)
    else:
      r = requests.get('http://chancedegol.uol.com.br/br16.htm')
      data = r.text
      self.save_cache(cache_name, data)
    return data

  def normalize_name_old(self, name):
    return name.lower() \
      .replace(u"ã","a")\
      .replace(u"é","e")\
      .replace(u"ê","e")\
      .replace(u"í","i")\
      .replace(u"ó","o")\
      .replace(u" pr", "-pr")\
      .replace(u" mg", "-mg")\
      .replace(u"", "")

  def normalize_name(self, name):
    return name.replace(u" PR", "-PR").replace(u" MG", "-MG")
    
  def parse_html_chance_de_gol(self):
    data = self.__get_prob_next_matches()
    table = [] 
    flag = False       
    lines = data.split("\n")
    i = 0
    while True:
      if u'Probabilidades para os próximos jogos' in lines[i]: flag = True
      if u"Jogos realizados" in lines[i]: break
      
      if (flag):
        if "<tr bgcolor" in lines[i]:
          m = re.match('\s*<td bgcolor="#FFFFFF"> <font size="3">(.*)</font></td>', lines[i+2])
          home_team =  self.normalize_name(m.group(1))
          m = re.match('\s*<td bgcolor="#FFFFFF"> <font size="3">(.*)</font></td>', lines[i+3])
          visitant = self.normalize_name(m.group(1))
          
          m = re.match('\s*<td bgcolor="#FFFFFF" align="center"> <font size="3">(.*)\s*%</font></td>', lines[i+4])
          m_prob = m.group(1)
          m = re.match('\s*<td bgcolor="#FFFFFF" align="center"> <font size="3">(.*)\s*%</font></td>', lines[i+5])
          e_prob = m.group(1)      
          m = re.match('\s*<td bgcolor="#FFFFFF" align="center"> <font size="3">(.*)\s*%</font></td>', lines[i+6])
          v_prob = m.group(1)        
          

          table.append([unicode(home_team), unicode(visitant), float(m_prob), float(e_prob), float(v_prob)])
         
      i += 1
      if i == len(lines): break

    return table     

  def obter_clubs_prob(self):
    return self.parse_html_chance_de_gol()

  def show_prob_next_matches(self):
    clubs = {}
    clubs[u'Santa Cruz']  = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':344}
    clubs[u'Ponte Preta'] = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':303}
    clubs[u'Sport']       = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':292}
    clubs[u'Santos']      = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':277}
    clubs[u'Figueirense'] = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':316}
    clubs[u'Chapecoense'] = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':315}
    clubs[u'Atlético-PR'] = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':293}
    clubs[u'Botafogo']    = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':263}
    clubs[u'Flamengo']    = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':262}
    clubs[u'Coritiba']    = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':294}
    clubs[u'Fluminense']  = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':266}
    clubs[u'São Paulo']   = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':276}
    clubs[u'Corinthians'] = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':264}
    clubs[u'América-MG']  = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':327}
    clubs[u'Cruzeiro']    = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':283}
    clubs[u'Atlético-MG'] = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':282}
    clubs[u'Internacional'] = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':285}
    clubs[u'Grêmio']        = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':284}
    clubs[u'Vitória']       = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':287}
    clubs[u'Palmeiras']     = {u'prob_victory' : -1.0, u'adversary':'', 'local':'FORA', u'id':275}
    #clubs = []
    for match in self.clubs_prob:
      clubs[match[0]]['prob_victory'] = match[2]
      clubs[match[0]]['adversary'] = match[1]
      clubs[match[0]]['local'] = 'CASA'

      clubs[match[1]]['prob_victory'] = match[4]
      clubs[match[1]]['adversary'] = match[0]


    print "%s | %s | %s | %s "%\
    (
      "club".center(20), 
      "adversary".center(20), 
      "LOCAL".center(5),
      "PROB. VENCER"
    )
    print "=" * 80
    sorted_clubs = sorted(clubs.keys(), key=lambda y: (clubs[y]['prob_victory']), reverse=True)
    for club in sorted_clubs:
      if clubs[club]['prob_victory'] < 0.0: continue
      print "%s | %s | %s | %.2f%%" %\
      (
        club.center(20),  
        clubs[club]['adversary'].center(20),
        clubs[club]['local'].center(5),
        clubs[club]['prob_victory']
      )