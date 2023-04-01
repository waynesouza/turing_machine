class TuringMachine:
    def __init__(self, rules):
        self.tape = ['_'] * 1000  # Inicializa uma fita com 1000 posições vazias
        self.head = 0  # Inicializa o cabeçote na posição 0 da fita
        self.state = 0  # Inicializa o estado da MT como 0
        self.rules = rules  # Armazena as regras de transição

    def run(self):
        while True:
            # Verifica se o estado atual está na lista de regras
            if (self.state, self.tape[self.head]) in self.rules:
                rule = self.rules[(self.state, self.tape[self.head])]
                if rule[0] == "pare":  # Verifica se a MT deve parar
                    break
                elif rule[0] == "retorne":  # Verifica se deve retornar para um estado anterior
                    self.state = rule[1]
                elif isinstance(rule[0], str):
                    # Chama um bloco
                    block_id = rule[0]
                    block_rules = self.rules[block_id][3]
                    tm = TuringMachine(block_rules)
                    tm.state = self.state
                    tm.tape = self.tape[:]
                    tm.head = self.head
                    tm.run()
                    # Atualiza o estado, a fita e o cabeçote com os valores da máquina de Turing chamada
                    self.state = tm.state
                    self.tape = tm.tape[:]
                    self.head = tm.head
                else:
                    # Atualiza o símbolo da fita
                    self.tape[self.head] = rule[1]
                    # Move o cabeçote para a direita
                    if rule[2] == "d":
                        self.head += 1
                    # Move o cabeçote para a esquerda
                    elif rule[2] == "e":
                        self.head -= 1
                    # Deixa o cabeçote na mesma posição
                    elif rule[2] == "i":
                        pass
                    # Atualiza o estado atual
                    self.state = rule[0]
            else:
                print("Erro de transição: estado {} e símbolo {}".format(self.state, self.tape[self.head]))
                break

    def load_rules(self, file_name):
        with open(file_name) as f:
            current_block_id = None
            current_block_rules = {}
            for line in f:
                # Ignora comentários
                line = line.split(';')[0]
                # Divide a linha em suas partes
                parts = line.strip().split()
                if len(parts) == 5:
                    if current_block_id is not None:
                        # Adiciona a regra ao dicionário de transições do bloco atual
                        current_state, current_symbol, _, new_symbol, movement, new_state = parts
                        current_block_rules[(int(current_state), current_symbol)] = (int(new_state), new_symbol, movement)
                    else:
                        # Adiciona a regra ao dicionário de transições
                        current_state, current_symbol, _, new_symbol, movement, new_state = parts
                        self.rules[(int(current_state), current_symbol)] = (int(new_state), new_symbol, movement)
                elif len(parts) == 3 and parts[2] == 'pare':
                    if current_block_id is not None:
                        # Estado de parada no bloco atual
                        current_state, current_symbol, _ = parts
                        current_block_rules[(int(current_state), current_symbol)] = ('pare', None, None)
                    else:
                        # Estado de parada
                        current_state, current_symbol, _ = parts
                        self.rules[(int(current_state), current_symbol)] = ('pare', None, None)
                elif len(parts) == 2 and parts[1] == 'retorne':
                    if current_block_id is not None:
                        # Retorno de bloco
                        current_state, _ = parts
                        current_block_rules[(int(current_state), None)] = ('retorne', None, None)
                    else:
                        # Retorno de bloco no bloco main
                        current_state, _ = parts
                        self.rules[(int(current_state), None)] = ('retorne', None, None)
                elif len(parts) == 3 and parts[0] == 'bloco':
                    # Declaração de bloco
                    block_id, initial_state = parts[1], int(parts[2])
                    current_block_id = block_id
                    current_block_rules = {}
                elif len(parts) == 1 and parts[0] == 'fim':
                    # Fim do bloco atual
                    self.rules[(int(initial_state), None)] = (current_block_id, None, None, current_block_rules)
                    current_block_id = None
                    current_block_rules = {}
