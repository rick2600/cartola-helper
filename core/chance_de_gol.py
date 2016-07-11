# -*- coding: utf-8 -*-
import requests
import time
import os
import codecs
import re

class ChanceDeGol:

  def __init__(self):
    self.clubes_prob = self.obter_clubes_prob()

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
    
  def __obter_prob_for_next_matches(self):
    data = ''
    cache_name = "chance_de_gol_%s.cache" %(time.strftime("%d-%m-%Y"))
    if (self.cached(cache_name)):
      data = self.read_from_cache(cache_name)
      #data = self.read_from_cache("a.html")      
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
    data = self.__obter_prob_for_next_matches()
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
          mandante =  self.normalize_name(m.group(1))
          m = re.match('\s*<td bgcolor="#FFFFFF"> <font size="3">(.*)</font></td>', lines[i+3])
          visitante = self.normalize_name(m.group(1))
          
          m = re.match('\s*<td bgcolor="#FFFFFF" align="center"> <font size="3">(.*)\s*%</font></td>', lines[i+4])
          m_prob = m.group(1)
          m = re.match('\s*<td bgcolor="#FFFFFF" align="center"> <font size="3">(.*)\s*%</font></td>', lines[i+5])
          e_prob = m.group(1)      
          m = re.match('\s*<td bgcolor="#FFFFFF" align="center"> <font size="3">(.*)\s*%</font></td>', lines[i+6])
          v_prob = m.group(1)        
          

          table.append([unicode(mandante), unicode(visitante), float(m_prob), float(e_prob), float(v_prob)])
         
      i += 1
      if i == len(lines): break

    return table     

  def obter_clubes_prob(self):
    return self.parse_html_chance_de_gol()

  def mostrar_probabilidades_prox_jogos(self):
    clubes = {}
    clubes[u'Santa Cruz']  = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':344}
    clubes[u'Ponte Preta'] = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':303}
    clubes[u'Sport']       = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':292}
    clubes[u'Santos']      = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':277}
    clubes[u'Figueirense'] = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':316}
    clubes[u'Chapecoense'] = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':315}
    clubes[u'Atlético-PR'] = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':293}
    clubes[u'Botafogo']    = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':263}
    clubes[u'Flamengo']    = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':262}
    clubes[u'Coritiba']    = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':294}
    clubes[u'Fluminense']  = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':266}
    clubes[u'São Paulo']   = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':276}
    clubes[u'Corinthians'] = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':264}
    clubes[u'América-MG']  = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':327}
    clubes[u'Cruzeiro']    = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':283}
    clubes[u'Atlético-MG'] = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':282}
    clubes[u'Internacional'] = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':285}
    clubes[u'Grêmio']        = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':284}
    clubes[u'Vitória']       = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':287}
    clubes[u'Palmeiras']     = {u'prob_vitoria' : -1.0, u'adversario':'', 'local':'FORA', u'id':275}
    #clubes = []
    for partida in self.clubes_prob:
      clubes[partida[0]]['prob_vitoria'] = partida[2]
      clubes[partida[0]]['adversario'] = partida[1]
      clubes[partida[0]]['local'] = 'CASA'

      clubes[partida[1]]['prob_vitoria'] = partida[4]
      clubes[partida[1]]['adversario'] = partida[0]


    print "%s | %s | %s | %s "%\
    (
      "CLUBE".center(20), 
      "ADVERSARIO".center(20), 
      "LOCAL".center(5),
      "PROB. VENCER"
    )
    print "=" * 80
    sorted_clubes = sorted(clubes.keys(), key=lambda y: (clubes[y]['prob_vitoria']), reverse=True)
    for clube in sorted_clubes:
      if clubes[clube]['prob_vitoria'] < 0.0: continue
      print "%s | %s | %s | %.2f%%" %\
      (
        clube.center(20),  
        clubes[clube]['adversario'].center(20),
        clubes[clube]['local'].center(5),
        clubes[clube]['prob_vitoria']
      )