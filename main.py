# -*- coding: utf-8 -*-


from core.cartola import *
from core.chance_de_gol import *
from core.arg_parser import ArgParser


def normalize(args):
  clubes_ids = []
  condicao_ids = []
  posicao_ids = []

  for clube in args.jog_clube:
    clubes_ids.append(CLUBES[clube])

  for condname in args.jog_condicao:
    condicao_ids.append(CONDICAO[condname])

  for posicao in args.jog_posicao:
    posicao_ids.append(POSICOES[posicao])

  return {
    'clubes_ids': clubes_ids, 
    'condicao_ids': condicao_ids, 
    'jog_num_jogos': args.jog_num_jogos, 
    'jog_preco_max': args.jog_preco_max,
    'posicao_ids': posicao_ids
  }


def main():
  parser = ArgParser()
  args = parser.parse_args()

  print args
  filtro = normalize(args)

  cartola = Cartola()
  chance_de_gol = ChanceDeGol()

  atletas = cartola.filtrar(filtro)
  
  if args.mostrar_prob:
    print "Próximos jogos:"
    chance_de_gol.mostrar_probabilidades_prox_jogos()

  if args.mostrar:
    cartola.mostrar_atletas(atletas)

  if args.escalar:
    cartola.escalar(args.formacao, args.top, args.verba, atletas) 


main()