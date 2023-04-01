# the state machine:
# {
#     state: (TAPE, {
#         read: (write, go, target, BREAKPOINT)
#     }),
#     state: (CALL, procedure_name, target, BREAKPOINT)
# }

# the virtual machine:
# {
#     procedure_name: (initial, state_machine)
# }

CALL = 0
TAPE = 1

DIREITA     = 1
IMOVEL      = 0
ESQUERDA    = -1

RETORNE = -1
PARE    = -2

class VirtualMachine:

    __tape = []
    tape_pos = 0

    def __init__(self, procedures, head='()'):

        self.procedures = procedures
        self.head = head

    def start(self, word):
        ''' Prepara a máquina para ser executada sobre uma palabra '''

        self.__tape = [x for x in word]
        self.tape_pos = 0
        self.stack = [['main', self.procedures['main'][0]], ]

    def show_current_state(self):
        ''' Exibe o estado presente do cabeçote da máquina '''

        p, s = self.stack[-1]

        left = self.__tape[max(0, self.tape_pos-20 ) : self.tape_pos]
        right = self.__tape[self.tape_pos+1:min(len(self.__tape), self.tape_pos + 1 + 20)]

        for i, c in enumerate(right):
            if c == None:
                right[i] = '_'

        for i, c in enumerate(left):
            if c == None:
                left[i] = '_'

        left = ''.join(left)
        right = ''.join(right)

        _head = self.__tape[self.tape_pos]

        if _head == None:
            _head = '_'

        print(f'{p:.>16}.{s:04}:{left:_>20}{self.head[0]}{_head}{self.head[1]}{right:_<20}')

    @property
    def tape(self):
        ''' representação da fita em string '''

        for i, c in enumerate(self.__tape):
            if c == None:
                self.__tape[i] = '_'

        return ''.join(self.__tape)

    def run(self, verbose=False, steps=500):
        ''' Executa n computações dessa máquina, retorna True caso a execução
            tenha terminado '''

        while len(self.stack) > 0:

            if steps == 0:
                return False

            steps -= 1

            p, s = self.stack[-1]

            if p not in self.procedures:

                print(f'error: procedure {p} not defined.')
                return True

            if s == PARE: # para a execução da máquina
                return True

            action = self.procedures[p][1][s][0]

            if verbose:
                self.show_current_state()

            if action == CALL: # faz uma chamada de procedimento

                p_name = self.procedures[p][1][s][1]

                if p_name not in self.procedures:
                    print(f'error: procedure {p_name} not defined.')
                    return True

                p_start = self.procedures[p_name][0]

                self.stack.append([ p_name, p_start] )

                if self.procedures[p][1][s][3]:
                    return False

                continue

            read = self.__tape[self.tape_pos]
            symbols = self.procedures[p][1][s][1]

            if (read not in symbols) and ('*' in symbols):

                write, go, target, breakpoint = symbols['*']

            elif read in symbols:

                write, go, target, breakpoint = symbols[read]

            else:

                print(f'error: action for state \'{s}\' and symbol \'{read}\' is not defined.')
                return True

            if write == '*':
                write = read

            self.__tape[self.tape_pos] = write
            self.tape_pos += go

            if self.tape_pos < 0:
                self.__tape = [None,] + self.__tape
                self.tape_pos = 0
            elif self.tape_pos == len(self.__tape):
                self.__tape += [None,]

            if target == RETORNE: # remove um item do topo da pilha

                del self.stack[-1]

                if len(self.stack) > 0:
                    p, s = self.stack[-1]
                    target = self.procedures[p][1][s][2]
                else:
                    break

            self.stack[-1][1] = target

            if breakpoint:
                return False

        return True