CALL = 0
TAPE = 1

DIREITA = 1
IMOVEL = 0
ESQUERDA = -1

RETORNE = -1
PARE = -2


class Machine:
    __tape = []
    tape_pos = 0

    def __init__(self, procedures, head='()'):

        self.procedures = procedures
        self.head = head

    def start(self, word):
        """
        This method defines a method called start that prepares the machine to be executed on a given
        word. The method takes a single parameter word, which is the input string that the machine
        will work on.

        First, the method initializes the tape of the machine with the characters of the word parameter.
        The tape is represented as a list of characters.

        Then, the method sets the position of the tape head to the initial position (i.e., position 0).

        Finally, the method initializes the stack of the machine with the main procedure, which is the
        starting point of the program. The stack is represented as a list of lists, where each inner
        list contains the name of a procedure and the position of the next instruction to be executed
        in that procedure.
        """
        self.__tape = [x for x in word]
        self.tape_pos = 0
        self.stack = [['main', self.procedures['main'][0]], ]

    def show_current_state(self):
        """
        This method defines a method called show_current_state that displays the current state
        of the head of a machine. It does this by accessing the internal variables
        stack and __tape of the object, and then extracting a slice of the tape to the left and right
        of the head position, of length 20 characters each. The code then replaces any None values
        in these slices with the underscore character _.

        Afterwards, the code joins the left and right slices into strings and retrieves the value
        of the tape at the current head position. If this value is None, it is replaced with an
        underscore character. Finally, the code prints out a string that includes the current
        state of the head and the extracted tape slices.
        """
        p, s = self.stack[-1]

        left = self.__tape[max(0, self.tape_pos - 20): self.tape_pos]
        right = self.__tape[self.tape_pos + 1:min(len(self.__tape), self.tape_pos + 1 + 20)]

        left = [c if c is not None else '_' for c in left]
        right = [c if c is not None else '_' for c in right]

        left = ''.join(left)
        right = ''.join(right)

        _head = self.__tape[self.tape_pos]

        if _head is None:
            _head = '_'

        print(f'{p:.>16}.{s:04}:{left:_>20}{self.head[0]}{_head}{self.head[1]}{right:_<20}')

    @property
    def tape(self):
        """
        This method defines a property called "tape", which returns a string representation of the
        tape in the Turing machine.
        The method first creates a list called "tape_str", which contains each
        character in the tape. If a character is not None, it is added to the list, otherwise,
        it is replaced by the underscore character "_". Finally,
        the method returns a string version of the "tape_str" list by joining all the elements together.
        """
        tape_str = [c if c is not None else '_' for c in self.__tape]
        return ''.join(tape_str)

    def run(self, verbose=False, steps=500):
        """
        This method defines a method called run which executes the Turing machine for a specified
        number of steps, or until it completes its execution. It operates by continuously iterating
        through the machine's stack, checking if the procedure being executed is defined and not in
        the PARE state (halted). If it is not halted, the machine reads the current symbol on the tape,
        and based on the current state and symbol, it either writes to the tape, moves the head to the
        left or right, calls another procedure, returns from a called procedure, or halts execution.

        If the verbose flag is set to True, the current state of the machine is printed after every
        operation. The method returns True if the execution completes successfully or if it encounters
        an error (such as calling an undefined procedure), and returns False if the specified number of
        steps is reached before the machine finishes executing or if it encounters a breakpoint.
        """
        while self.stack:
            if steps == 0:
                return False
            steps -= 1
            p, s = self.stack[-1]
            if p not in self.procedures:
                print(f'error: procedure {p} not defined.')
                return True
            if s == PARE:
                return True
            action = self.procedures[p][1][s][0]
            if verbose:
                self.show_current_state()
            if action == CALL:
                p_name = self.procedures[p][1][s][1]
                if p_name not in self.procedures:
                    print(f'error: procedure {p_name} not defined.')
                    return True
                p_start = self.procedures[p_name][0]
                self.stack.append([p_name, p_start])
                if self.procedures[p][1][s][3]:
                    return False
                continue
            read = self.__tape[self.tape_pos]
            symbols = self.procedures[p][1][s][1]
            if read not in symbols and '*' in symbols:
                write, go, target, breakpoint = symbols['*']
            else:
                write, go, target, breakpoint = symbols.get(read, (None, None, None, None))
            write = write if write != '*' else read
            self.__tape[self.tape_pos] = write
            self.tape_pos += go
            if self.tape_pos < 0:
                self.__tape = [None, ] + self.__tape
                self.tape_pos = 0
            elif self.tape_pos == len(self.__tape):
                self.__tape += [None, ]
            if target == RETORNE:
                self.stack.pop()
                if self.stack:
                    p, s = self.stack[-1]
                    target = self.procedures[p][1][s][2]
                else:
                    break
            self.stack[-1][1] = target
            if breakpoint:
                return False
        return True
