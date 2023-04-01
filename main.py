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
                if rule[2] == "pare":  # Verifica se a MT deve parar
                    break
                elif rule[2] == "retorne":  # Verifica se deve retornar para um estado anterior
                    self.state = rule[3]
                else:
                    # Atualiza o símbolo da fita
                    self.tape[self.head] = rule[2]
                    # Move o cabeçote para a direita
                    if rule[1] == "d":
                        self.head += 1
                    # Move o cabeçote para a esquerda
                    elif rule[1] == "e":
                        self.head -= 1
                    # Deixa o cabeçote na mesma posição
                    elif rule[1] == "i":
                        pass
                    # Atualiza o estado atual
                    self.state = rule[3]
            else:
                print("Erro de transição: estado {} e símbolo {}".format(self.state, self.tape[self.head]))
                break
