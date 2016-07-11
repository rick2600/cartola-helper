# -*- coding: utf-8 -*-

import os.path
import json
import httplib
import itertools
import time
import requests
import codecs



CLUBES = {
  'america-mg' : 327,
  'atletico-mg': 282,
  'atletico-pr': 293,
  'botafogo'   : 263,
  'chapecoense': 315,
  'corinthians': 264,
  'coritiba'   : 294,
  'cruzeiro'   : 283,
  'figueirense': 316,
  'flamengo'   : 262,
  'fluminense' : 266,
  'gremio'     : 284,
  'internacional' : 285,
  'palmeiras'  : 275,
  'pontepreta' : 303,
  'santacruz'  : 344, 
  'santos'     : 277,
  'saopaulo'   : 276,
  'sport'      : 292,
  'vitoria'    : 287
}

CONDICAO = {"provavel":7, "duvida":2, "suspenso":3, "contundido":5, "nulo":6}
POSICOES = {"gol":1, "lat":2, "zag":3, "mei":4, "ata":5, "tec":6}




class Cartola:

  def __init__(self):
    self.atletas = sorted(self.obter_atletas(), key=lambda k: k['media_num'], reverse=True)
    self.clubes = self.obter_clubes()
    self.atletas_status = self.obter_atletas_status()
    self.posicoes = self.obter_atletas_posicoes()     

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
    
  def obter_info(self, path):
    json_data = None
    data = None
    cache_name = path.replace("/", "_") + '.cache'
    cache_name = "%s-%s.cache" %(path[1:].replace("/", "_"), time.strftime("%d-%m-%Y"))
    if (self.cached(cache_name)):
      data = self.read_from_cache(cache_name)
    else:
      r = requests.get('https://api.cartolafc.globo.com' + path)
      data = r.text      
      self.save_cache(cache_name, data)
    return json.loads(data)

  def obter_atletas(self):
    return self.obter_info("/atletas/mercado")["atletas"]
    
  def obter_partidas(self):
    return self.obter_info("/partidas")["partidas"]    

  def obter_atletas_status(self):
    return self.obter_info("/atletas/mercado")["status"]

  def obter_atletas_posicoes(self):
    return self.obter_info("/atletas/mercado")["posicoes"]

  def obter_clubes(self):
    return self.obter_info("/atletas/mercado")["clubes"]

  def filtrar(self, cond):
    atletas = []
    for atleta in self.atletas:
      if atleta["status_id"] not in cond['condicao_ids']: continue
      if atleta["preco_num"] > cond["jog_preco_max"]: continue
      if atleta["clube_id"] not in cond["clubes_ids"]: continue
      if atleta["posicao_id"] not in cond["posicao_ids"]: continue
      if atleta["jogos_num"] < cond["jog_num_jogos"]: continue
      atletas.append(atleta)

    return atletas

  def mostrar_atletas(self, atletas=None):
    if atletas == None: atletas = self.atletas
    print " %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s" %\
    (
      "APELIDO".center(20), 
      "POS".center(3),
      "TIME".center(14),
      "CONDICAO".center(10),
      "JOGOS",
      "PRECO",
      "MEDIA",
      " A ",
      " G ",
      " SG ",
      " RB ",
      "CONFRONTO"
    )
    print "=" * 130
    for atleta in atletas:

      confronto = self.clubes[str(atleta['partida']["clube_casa_id"])]["abreviacao"]
      confronto += ' x '
      confronto += self.clubes[str(atleta['partida']["clube_visitante_id"])]["abreviacao"]
      
      if atleta['partida']["clube_casa_id"] == atleta["clube_id"]:
        confronto += " (C)"
      else:
        confronto += " (F)"
      
      print " %s | %s | %s | %s | %5d | %s | %s | %s | %s | %s | %s | %s" %\
      (
        atleta['apelido'].ljust(20), 
        self.posicoes[str(atleta["posicao_id"])]["abreviacao"].center(3),
        self.clubes[str(atleta["clube_id"])]["nome"].ljust(14),
        self.atletas_status[str(atleta["status_id"])]["nome"].center(10),
        atleta["jogos_num"],
        ("%.2f" %(atleta["preco_num"])).rjust(5),
        ("%.2f" %(atleta["media_num"])).rjust(5),
        str(atleta['scout']["A"] if "A" in atleta['scout'] else '0').rjust(3),
        str(atleta['scout']["G"] if "G" in atleta['scout'] else '0').rjust(3),
        str(atleta['scout']["SG"] if "SG" in atleta['scout'] else '0').rjust(4),
        str(atleta['scout']["RB"] if "RB" in atleta['scout'] else '0').rjust(4),
        confronto                                           
      )
    print "\n A - Assistência | G - Gol | SG - Jogos sem sofrer gol | RB - Roubo de bolas"

  def obter_atletas_por_pos(self, pos, top=10, atletas=None):
    if atletas == None: atletas = self.atletas
    _atletas = []
    for atleta in atletas:
      if self.posicoes[str(atleta["posicao_id"])]["abreviacao"] != pos: continue
      if len(_atletas) >= top: break
      _atletas.append(atleta)
    return _atletas

  def escalar(self, formacao, top, verba, atletas):
    time = []
    preco = 0.0
    lat = 0
    zag, mei, ata = formacao.split('-')
    zag = int(zag)
    mei = int(mei)
    ata = int(ata)
    if (zag >= 4):
      lat = 2
      zag = zag - 2
    
    top_tec = sorted(self.obter_atletas_por_pos("tec", top, atletas), key=lambda k: k['media_num'])
    top_gol = sorted(self.obter_atletas_por_pos("gol", top, atletas), key=lambda k: k['media_num']) 
    top_lat = sorted(self.obter_atletas_por_pos("lat", top, atletas), key=lambda k: k['media_num'])
    top_zag = sorted(self.obter_atletas_por_pos("zag", top, atletas), key=lambda k: k['media_num'])
    top_mei = sorted(self.obter_atletas_por_pos("mei", top, atletas), key=lambda k: k['media_num'])
    top_ata = sorted(self.obter_atletas_por_pos("ata", top, atletas), key=lambda k: k['media_num'])
                  
    tecs = list(itertools.combinations(top_tec, 1))
    gols = list(itertools.combinations(top_gol, 1))    
    lats = list(itertools.combinations(top_lat, lat))
    zags = list(itertools.combinations(top_zag, zag))
    meis = list(itertools.combinations(top_mei, mei))
    atas = list(itertools.combinations(top_ata, ata))
       
    time_good = None
    cur_media = 0.0
    cur_preco = 0.0    

    for tec in tecs:
      preco = 0.0
      for atleta in tec: preco += atleta['preco_num']

      for g in gols:
        g_preco = 0.0
        for atleta in g: g_preco += atleta['preco_num']
        preco += g_preco
        if preco > verba: 
          preco -= g_preco
          continue

        for l in lats:
          l_preco = 0.0
          for atleta in l: l_preco += atleta['preco_num']
          preco += l_preco
          if preco > verba: 
            preco -= l_preco
            continue
          
          for z in zags:
            z_preco = 0.0
            for atleta in z: z_preco += atleta['preco_num']
            preco += z_preco
            if preco > verba: 
              preco -= z_preco
              continue   
            
            for m in meis:
              m_preco = 0.0
              for atleta in m: m_preco += atleta['preco_num']
              preco += m_preco
              if preco > (verba * 0.85):
              #if preco > verba: 
                preco -= m_preco
                continue   
              
              for a in atas:                        
                a_preco = 0.0
                for atleta in a: a_preco += atleta['preco_num']
                preco += a_preco
                if preco > verba: 
                  preco -= a_preco
                  continue               

                time = tec + g + l + z + m + a
                media = 0.0
                for atleta in time: media += atleta['media_num']
                
                if media > cur_media:
                  time_good = time
                  cur_media = media
                  cur_preco = preco
                  self.mostrar_atletas(time)
                  print " Preco: %.2f | Média: %.2f\n\n" %(preco, media)                  
                  
                preco -= a_preco
              preco -= m_preco
            preco -= z_preco   
          preco -= l_preco
        preco -= g_preco      