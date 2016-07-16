# -*- coding: utf-8 -*-


from core.cartola import *
from core.chance_de_gol import *
from core.arg_parser import ArgParser


def normalize(args):
  clubs_ids = []
  status_ids = []
  position_ids = []

  for clube in args.p_clubs:
    clubs_ids.append(CLUBS[clube])

  for condname in args.p_status:
    status_ids.append(STATUS[condname])

  for position in args.p_pos:
    position_ids.append(POSITIONS[position])

  return {
    'clubs_ids': clubs_ids, 
    'status_ids': status_ids, 
    'p_num_matches': args.p_num_matches, 
    'p_max_price': args.p_max_price,
    'position_ids': position_ids
  }


def main():
  parser = ArgParser()
  args = parser.parse_args()

  print args
  cond = normalize(args)

  cartola = Cartola()
  chance_de_gol = ChanceDeGol()

  players = cartola.filter(cond)
  
  if args.show_prob:
    print "Próximos jogos:"
    chance_de_gol.show_prob_next_matches()

  if args.show:
    cartola.show_players(players)

  if args.find_teams:
    #cartola.find_teams(args.tatic, args.top, args.budget, players) 
    cartola.find_teams(args, players) 


main()
