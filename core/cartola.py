# -*- coding: utf-8 -*-

import os.path
import json
import httplib
import itertools
import requests
import codecs
import time



CLUBS = {
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

STATUS = {"provavel":7, "duvida":2, "suspenso":3, "contundido":5, "nulo":6}
POSITIONS = {"gol":1, "lat":2, "zag":3, "mei":4, "ata":5, "tec":6}


class Cartola:

  def __init__(self):
    self.players = sorted(self.get_players(), key=lambda k: k['media_num'], reverse=True)
    self.clubs = self.get_clubs()
    self.players_status = self.get_players_status()
    self.positions = self.get_players_positions()     

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
    
  def get_info(self, path):
    json_data = None
    data = None
    _cache_name = "%s-%s.cache" %(path[1:].replace("/", "_"), time.strftime("%d-%m-%Y"))
    cache_name = os.path.join("./cache", _cache_name)

    if (self.cached(cache_name)):
      data = self.read_from_cache(cache_name)
    else:
      r = requests.get('https://api.cartolafc.globo.com' + path)
      data = r.text      
      self.save_cache(cache_name, data)
    return json.loads(data)

  def get_players(self):
    return self.get_info("/atletas/mercado")["atletas"]
    
  def obter_partidas(self):
    return self.get_info("/partidas")["partidas"]    

  def get_players_status(self):
    return self.get_info("/atletas/mercado")["status"]

  def get_players_positions(self):
    return self.get_info("/atletas/mercado")["posicoes"]

  def get_clubs(self):
    return self.get_info("/atletas/mercado")["clubes"]

  def filter(self, cond):
    players = []
    for player in self.players:
      if player["status_id"] not in cond['status_ids']: continue
      if player["preco_num"] > cond["p_max_price"]: continue
      if player["clube_id"] not in cond["clubs_ids"]: continue
      if player["posicao_id"] not in cond["position_ids"]: continue
      if player["jogos_num"] < cond["p_num_matches"]: continue
      players.append(player)

    return players

  def show_players(self, players=None):
    if players == None: players = self.players
    print " %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s" %\
    (
      "APELIDO".center(20), 
      "POS".center(3),
      "CLUBE".center(14),
      "CONDICAO".center(10),
      "JOGOS",
      "PRECO",
      "MEDIA",
      " A ",
      " G ",
      " SG ",
      " RB ",
      "PARTIDA".center(25)
    )
    print "=" * 140
    for player in players:
      match = player['partida']
      match_fmt = ''
      match_fmt += self.clubs[str(match["clube_casa_id"])]["abreviacao"]
      match_fmt += " [%2d]" %(self.clubs[str(match["clube_casa_id"])]["posicao"])
      match_fmt += ' x '
      match_fmt += self.clubs[str(match["clube_visitante_id"])]["abreviacao"]
      match_fmt += " [%2d]" %(self.clubs[str(match["clube_visitante_id"])]["posicao"])
      
      if match["clube_casa_id"] == player["clube_id"]:
        match_fmt += " (C)"
      else:
        match_fmt += " (F)"
      
      print " %s | %s | %s | %s | %5d | %s | %s | %s | %s | %s | %s | %s" %\
      (
        player['apelido'].ljust(20), 
        self.positions[str(player["posicao_id"])]["abreviacao"].center(3),
        self.clubs[str(player["clube_id"])]["nome"].ljust(14),
        self.players_status[str(player["status_id"])]["nome"].center(10),
        player["jogos_num"],
        ("%.2f" %(player["preco_num"])).rjust(5),
        ("%.2f" %(player["media_num"])).rjust(5),
        str(player['scout']["A"] if "A" in player['scout'] else '0').rjust(3),
        str(player['scout']["G"] if "G" in player['scout'] else '0').rjust(3),
        str(player['scout']["SG"] if "SG" in player['scout'] else '0').rjust(4),
        str(player['scout']["RB"] if "RB" in player['scout'] else '0').rjust(4),
        match_fmt                                           
      )
    print "\n A - Assistência | G - Gol | SG - Jogos sem sofrer gol | RB - Roubo de bolas"

  def get_players_by_position(self, pos, top=10, players=None):
    if players == None: players = self.players
    _players = []
    for player in players:
      if self.positions[str(player["posicao_id"])]["abreviacao"] != pos: continue
      if len(_players) >= top: break
      _players.append(player)
    return _players
    
  def calc_media_comb(self, args, combs):
    res = []
    for comb in combs:
      m_real = 0.0
      extra = 0.0
      price = 0.0
      for player in comb:
        club_id = player['clube_id']
        adv_club_id = player['partida']["clube_visitante_id"]
        
        if adv_club_id == club_id:
          adv_club_id = player['partida']["clube_casa_id"]
          
        club_pos = self.clubs[str(club_id)]['posicao']   
        adv_pos = self.clubs[str(adv_club_id)]['posicao']

        # extra pontos baseado na diferença de posições dos teams
        if club_pos < adv_pos: extra += (adv_pos-club_pos) * args.extra_pos
        
        # extra pontos caso jogue em casa
        if player['partida']["clube_casa_id"] == player['clube_id']: extra += args.extra_home
          
        
        m_real += player['media_num']
        price += player['preco_num']
        
      res.append([m_real, m_real + extra, price, comb])
    return res      

  def find_teams(self, args, players):
    team = []
    price = 0.0
    lat = 0
    zag, mei, ata = args.tatic.split('-')
    zag = int(zag)
    mei = int(mei)
    ata = int(ata)
    if (zag >= 4):
      lat = 2
      zag = zag - 2
    
    top_tec = sorted(self.get_players_by_position("tec", args.top, players), key=lambda k: k['media_num'])
    top_gol = sorted(self.get_players_by_position("gol", args.top, players), key=lambda k: k['media_num']) 
    top_lat = sorted(self.get_players_by_position("lat", args.top, players), key=lambda k: k['media_num'])
    top_zag = sorted(self.get_players_by_position("zag", args.top, players), key=lambda k: k['media_num'])
    top_mei = sorted(self.get_players_by_position("mei", args.top, players), key=lambda k: k['media_num'])
    top_ata = sorted(self.get_players_by_position("ata", args.top, players), key=lambda k: k['media_num'])


    tecs_comb = self.calc_media_comb(args, itertools.combinations(top_tec, 1))
    gols_comb = self.calc_media_comb(args, itertools.combinations(top_gol, 1))
    lats_comb = self.calc_media_comb(args, itertools.combinations(top_lat, lat))    
    zags_comb = self.calc_media_comb(args, itertools.combinations(top_zag, zag))    
    meis_comb = self.calc_media_comb(args, itertools.combinations(top_mei, mei))
    atas_comb = self.calc_media_comb(args, itertools.combinations(top_ata, ata))             
    
    price = 0.0
    m_real = 0.0
    m_virtual = 0.0
    
    for t_m_real, t_m_virtual, t_price, tec in tecs_comb:
      for g_m_real, g_m_virtual, g_price, gol in gols_comb:
        for l_m_real, l_m_virtual, l_price, lats in lats_comb:
          for z_m_real, z_m_virtual, z_price, zags in zags_comb:
            for m_m_real, m_m_virtual, m_price, meis in meis_comb:
              for a_m_real, a_m_virtual, a_price, atas in atas_comb:
                temp_price = t_price + g_price + z_price + l_price + m_price + a_price
                temp_m_real = t_m_real + g_m_real + z_m_real + l_m_real + m_m_real + a_m_real
                temp_m_virtual = t_m_virtual + g_m_virtual + z_m_virtual + l_m_virtual + m_m_virtual + a_m_virtual
                
                if temp_m_virtual > m_virtual and temp_price <= args.budget:
                  m_virtual = temp_m_virtual
                  price = temp_price
                  self.show_players(tec+gol+lats+zags+meis+atas)
                  print " price: %.2f | Média Real: %.2f | Média Virtual: %.2f\n\n" %(price, temp_m_real, m_virtual) 
                
            
       
       
