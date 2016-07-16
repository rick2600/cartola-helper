# -*- coding: utf-8 -*-

import argparse

CLUBS = [
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

STATUS = ["provavel", "duvida", "suspenso", "contundido", "nulo"]
POSITIONS = ["gol", "lat", "zag", "mei", "ata", "tec"]


class ArgParser:

  def __init__(self):
    self.parser = argparse.ArgumentParser()
    #self.subparsers = self.parser.add_subparsers(
    #  title='subcommands', description='valid subcommands')

    # sub parsers
    #self.parser = self.subparsers.add_parser('cartola')
    #self.chancedegol_parser = self.subparsers.add_parser('chancedegol')

    self.parser.add_argument('--budget', 
      type=float, 
      default=0.0, 
      help='available budget to buy players')
    self.parser.add_argument('--tatic', 
      default="4-4-2",
      choices=["3-4-3","3-5-2","4-3-3","4-4-2","4-5-1","5-3-2","5-4-1"],
      help='tatic')
    self.parser.add_argument('--p-status', 
      default=STATUS,
      nargs='+',
      choices=STATUS,
      help="player status")
    self.parser.add_argument('--p-max-price', 
      type=float, 
      default=100.0, 
      help='max price of a player')
    self.parser.add_argument('--p-num-matches', 
      type=int, 
      default=1, 
      help='minimum played matches of a player')
    self.parser.add_argument('--p-clubs', 
      default=CLUBS,
      nargs='+',
      choices=CLUBS,
      help='filter by clubs')
    self.parser.add_argument('--p-pos', 
      default=POSITIONS,
      nargs='+',
      choices=POSITIONS,
      help='filter by positions')
    self.parser.add_argument('--show', 
      action='store_true',
      help='show results')
    self.parser.add_argument('--find-teams', 
      action='store_true',
      help='find good ranked teams basead on filters')
    self.parser.add_argument('--top', 
      type=int, 
      default=8, 
      help='filter by top players in each position')
    self.parser.add_argument('--show-prob', 
      action='store_true',
      help='show probability of victory of clubs')
    self.parser.add_argument('--extra-pos', 
      type=float, 
      default=0.0, 
      help='extra points for player based on club vs advserary rank position')
    self.parser.add_argument('--extra-home', 
      type=float, 
      default=0.0, 
      help='extra points for player if he plays at home')
  def parse_args(self):
    return self.parser.parse_args()
