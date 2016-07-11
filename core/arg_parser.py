# -*- coding: utf-8 -*-

import argparse

CLUBES = [
  'america-mg', 
  'atletico-mg', 
  'atletico-pr', 
  'botafogo', 
  'chapecoense', 
  'corinthians', 
  'coritiba', 
  'cruzeiro', 
  'figueirense', 
  'flamengo', 
  'fluminense', 
  'gremio', 
  'internacional', 
  'palmeiras', 
  'pontepreta', 
  'santacruz', 
  'santos', 
  'saopaulo', 
  'sport', 
  'vitoria'
]

CONDICAO = ["provavel", "duvida", "suspenso", "contundido", "nulo"]
POSICOES = ["gol", "lat", "zag", "mei", "ata", "tec"]


class ArgParser:

  def __init__(self):
    self.parser = argparse.ArgumentParser()
    #self.subparsers = self.parser.add_subparsers(
    #  title='subcommands', description='valid subcommands')

    # sub parsers
    #self.parser = self.subparsers.add_parser('cartola')
    #self.chancedegol_parser = self.subparsers.add_parser('chancedegol')

    self.parser.add_argument('--verba', 
      type=float, 
      default=0.0, 
      help='verba disponível')
    self.parser.add_argument('--formacao', 
      default="4-4-2",
      choices=["3-4-3","3-5-2","4-3-3","4-4-2","4-5-1","5-3-2","5-4-1"],
      help='formacao')
    self.parser.add_argument('--jog-condicao', 
      default=CONDICAO,
      nargs='+',
      choices=CONDICAO,
      help="condição do jogador")
    self.parser.add_argument('--jog-preco-max', 
      type=float, 
      default=100.0, 
      help='preco máximo do jogador')
    self.parser.add_argument('--jog-num-jogos', 
      type=int, 
      default=1, 
      help='filtrar por número de jogos')
    self.parser.add_argument('--jog-clube', 
      default=CLUBES,
      nargs='+',
      choices=CLUBES,
      help='filtrar por clubes')
    self.parser.add_argument('--jog-posicao', 
      default=POSICOES,
      nargs='+',
      choices=POSICOES,
      help='filtrar por posições')
    self.parser.add_argument('--mostrar', 
      action='store_true',
      help='mostrar resultado')
    self.parser.add_argument('--escalar', 
      action='store_true',
      help='encontra bons times baseado no filtro')
    self.parser.add_argument('--top', 
      type=int, 
      default=8, 
      help='escalar usando os top jogadores de cada posição')
    self.parser.add_argument('--mostrar-prob', 
      action='store_true',
      help='mostrar probabilidade de vitória dos clubes')

  def parse_args(self):
    return self.parser.parse_args()
