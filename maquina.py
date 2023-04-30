import utils.constantes as const


class Maquina:
    def __init__(self, banco, entrada, delim='()'):
        self.entrada = entrada or '_'
        self.banco = banco
        self.ponteiro = self.entrada.find(self.entrada[0]) if self.entrada else 0
        self.bloco_atual = 'main'
        self.estado_atual = '01'
        self.lista_retorno = []
        self.bloco_anterior = None
        self.estado_anterior = None
        self.estado_final = False
        self.estado_pos_retorne = None
        self.pausa = None
        self.pausa_pos_bloco = None
        self.simbolo_verificado = 0
        self.delim = delim

    def __str__(self):
        try:
            estado_atual = '{:04d}'.format(int(self.estado_atual))
        except ValueError:
            estado_atual = self.estado_atual

        cabecote = f'{self.delim[0]}{self.entrada[self.ponteiro]}{self.delim[1]}'
        return f'{self.bloco_atual.rjust(16, ".")}.{estado_atual}: {self.retornar_esquerda_fita()}{cabecote}{self.retornar_direita_fita()}'

    def retornar_esquerda_fita(self):
        esquerda_fita = self.entrada[self.ponteiro - 20:self.ponteiro][::-1].ljust(const.TAMANHO_MAXIMO_FITA, '_')
        return esquerda_fita

    def retornar_direita_fita(self):
        direita_fita = self.entrada[self.ponteiro + 1:self.ponteiro + 20].rjust(const.TAMANHO_MAXIMO_FITA, '_')
        return direita_fita

    def verificar_transicao(self):
        for elemento in self.banco:
            if elemento["nome"] == self.bloco_atual:
                for dado in elemento["dados"]:
                    if int(dado['estado_atual']) == int(self.estado_atual):
                        if len(dado) in [5, 6]:
                            if dado["simbolo_atual"] == self.entrada[self.ponteiro] or dado["simbolo_atual"] == "*":
                                return True
                        if len(dado) in [3, 4]:
                            return True
        return False

