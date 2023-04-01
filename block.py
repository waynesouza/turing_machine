class Block:
    """
    Class that contains the block of TM instructions
    """
    RESUME = 0
    VERBOSE = 1
    STEP = 2
    NONE = 3

    @property
    def retorne(self):
        return 0

    @property
    def pare(self):
        return 1

    def __init__(self, id, initial_state, instructions):
        """
        :param id: block id
        :param initial_state: block initial state
        :param instructions: set of instructions in the format {e: {a:task}}
        """
        self.id = id
        self.initial_state = initial_state
        self.instructions = instructions
        self.list_blocks = None  # a block will have the addressing of all the others

    def add_block_in_list(self, blocks):
        self.list_blocks = blocks

    def provide_option(self, data):
        option = input('Provide an option (-r, -v, -s): ').split()

        if '-r' in option:
            data.change_flag(self.RESUME)
            data.add_computations(500)

        if '-v' in option:
            data.change_flag(self.VERBOSE)
            data.add_computations(500)

        if '-s' in option:
            try:
                data.add_computations(int(option[1]))
            except IndexError:
                print('Provide an integer after the -s argument')
                self.provide_option(data)

    def execute_block(self, tape, data):
        """
        Execute the block on the shared tape object used by all blocks.
        :param tape: a tape object
        :param data: object of data
        :return: return to the previous block or stop
        """
        # go to the initial state
        state = self.initial_state
        while True:
            if data.computations == 0:  # use the prompt to check if we can continue
                self.provide_option(data)

            if data.flag in (self.VERBOSE, self.STEP):
                format_str = "{:->25}: " + tape.printfita
                try:
                    aux_str = ('%s.{:04d}'.format(state) % self.id)
                except ValueError:
                    aux_str = ('%s.{:0>4s}'.format(state) % self.id)
                print(format_str.format(aux_str))

            # one computation done
            data.subcomputations(1)

            if state == 'retorne':
                return self.retorne
            if state == 'pare':
                print('Result: ' + tape.printfita)
                return self.pare

            state = int(state)
            instructions_state = self.id[state]

            if isinstance(instructions_state, list):  # movement instruction for some block
                flag = self.retorne
                data.call_block(instructions_state[0]).execute_block(tape, data)

                if flag == self.pare:
                    return self.pare
                state = instructions_state[1]
                continue

            character = tape.head  # character on the tape
            break_point = ''
            try:
                break_point = instructions_state[character][-1]
                tape.execute(instructions_state[character][1:3])
                state = instructions_state[character][3]
                if '!' == break_point:
                    print('breakpoint')
                    self.provide_option(data)
            except KeyError:
                try:
                    break_point = instructions_state['*'][-1]
                    tape.execute(instructions_state['*'][1:3])
                    state = instructions_state['*'][3]
                    if '!' == break_point:
                        print('breakpoint')
                        self.provide_option(data)
                except KeyError:
                    print('Error in state %s in block %s' % (state, self.id))
                    print('Character %s not recognized' % character)
                    exit(-1)
