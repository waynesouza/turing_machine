import utils.constants as const

DEFAULT_MESSAGE = f'Simulador de Máquina de Turing ver 1.0 - IFMG {const.CURRENT_YEAR}\n' \
                  f'Desenvolvido como trabalho pratico para a disciplina de Teoria da Computação\n' \
                  f'Autores: {const.FIRST_AUTHOR} e {const.SECOND_AUTHOR}\n'
OPTIONS = f'{{param}}: usage: {{param}} [options] input_file\n' \
          f' options:\n' \
          f' -?, --help :\t exibe essa tela de ajuda.\n' \
          f' -r, --resume :\t executa o programa até o fim e imprime o conteúdo final da fita.\n' \
          f' -b, --break :\t para a execução da máquina após N computações e mostra o conteúdo da fita.\n' \
          f' -s, --steps=N :\t mostra N computações, depois aguarda uma nova opção.\n' \
          f' -h, --head=DELIM :\t define os caracteres delimitadores do cabeçote\n' \
          f' -w, --word=WORD :\t define a palavra de entrada do programa.'
INPUT_OPTIONS = f'Forneça opção (-r -v -s -b): '
INPUT_WORD = f'Forneça a palavra inicial: '
