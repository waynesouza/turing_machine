import argparse
import sys

from block import readFile
from machine import Machine


def usage():
    print('Simulador de Máquina de Turing ver 1.0')
    print('Desenvolvido como trabalho pratico para a disciplina de Teoria da Computação')
    print('[Augusto Amaral, Caio Melo], IFMG, 2018.\n')
    print('Modo de uso:')
    print(f'{sys.argv[0]} [opções] entrada')


def parse_args():
    parser = argparse.ArgumentParser(description='Simulador de Máquina de Turing')
    parser.add_argument('-r', '--resume', action='store_true', help='Não é possível resumir a execução')
    parser.add_argument('-v', '--verbose', action='store_true', help='Ativa modo verbose')
    parser.add_argument('-b', '--break', action='store_true', help='Ativa o modo de interrupção')
    parser.add_argument('-s', '--steps', type=int, help='Quantidade de passos para execução')
    parser.add_argument('-H', '--head', type=str, default='()', help='Define o cabeçote')
    parser.add_argument('-w', '--word', type=str, help='Define a palavra da fita')
    parser.add_argument('entrada', type=str, help='Arquivo de entrada')
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.steps:
        args.steps = 500

    if args.verbose:
        usage()

    # parse the input file
    procedures = readFile(args.entrada)
    machine = Machine(procedures, args.head)

    if not args.word:
        args.word = input('Forneça a palavra inicial: ')

    machine.start(args.word)

    while not machine.run(args.verbose, args.steps):
        ''' executa a máquina '''

        if args.__break:
            break

        args = input('Forneça opção (-r -v -s -b): ')
        args = args.split()

        try:
            args = parse_args().parse_args(args)
        except SystemExit:
            continue

        if args.steps is not None:
            if machine.steps != args.steps:
                print(f'{sys.argv[0]}: erro: não é possivel redefinir o numero de passos.')
                continue
        else:
            args.steps = machine.steps

        machine.steps = args.steps
        machine.verbose = args.verbose

        if args.resume:
            print(f'{sys.argv[0]}: erro: não é possivel resumir aqui.')
            continue

    final = machine.tape
    print(final)


if __name__ == '__main__':
    main()
