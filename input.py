import machine
import sys

def readFile(filedir):
    '''Le o arquivo e retorna as linhas'''
    def read():
        try:
            fn=open(filedir,"U")
        except IOError:
            print(f"error: File '{filedir}' does not appear to exist.")
            sys.exit()

        with fn as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        return content

    '''Se existir comentario os remove'''
    def removeComent(linha):
        if ";" in linha:
            index = linha.index(";")
            if index == 0:
                return ""
            else:
                vet = linha.split(";")
                return vet[0]
        else:
            return linha

    '''Identifica a linha e retorna a MT'''
    def identify():
        content = read()
        bloco   = False
        mt = {}
        i = 0
        for c in content:
            c = removeComent(c)
            i += 1
            vet = c.split()
            if len(vet) > 0:
                # String maior ou menor que qualquer uma identificada
                if len(vet) == 2 or len(vet) > 6 or (len(vet) == 1 and "fim" not in vet[0]) or (len(vet) == 3 and "bloco" not in vet[0] and bloco == False):
                    print(f"Warning: '{c}' undefined string format. Line [{i}]")
                if bloco == False and vet[0] == "bloco":
                    bloco = True

                    try:
                        mt[vet[1]] = (int(vet[2]),{})
                    except Exception as e:
                        print(f"error: '{vet[2]}' is not a integer. Line [{i}]")
                        sys.exit()
                    vetTrans = mt[vet[1]][1]
                    t = {}
                    s = {}

                elif vet[0] == "fim":
                    bloco = False

                elif bloco == True:
                    try:
                        state   = int(vet[0])
                    except Exception as e:
                        print(f"error: '{vet[0]}' is not a integer. Line [{i}]")
                        sys.exit()
                    procname = vet[1]
                    target  = vet[2]
                    bp      = False

                    # Identifica CALL com breakpoint espaçado
                    if len(vet) == 4 and vet[3] == "!":
                        bp = True
                    # Identifica CALL com breakpoint ou não
                    if len(vet) == 3 or len(vet)==4:
                        if "!" in vet[2]:
                            bp = True
                            target = target.replace("!","")

                        if target == "pare":
                            target = -2
                        elif target == "retorne":
                            target = -1
                        elif target == "*":
                            target = state
                        else:
                            try:
                                target = int(target)
                            except Exception as e:
                                print(f"error: Target '{target}' is not a integer/'retorne'/'pare'. Line [{i}]")
                                sys.exit()
                        vetTrans[state] = (0,procname, target,bp)

                    # Identifica Instrução
                    if len(vet) == 6 or len(vet) == 7:
                        try:
                            source = int(vet[0])
                        except Exception as e:
                            print(f"error: Source '{target}' is not a integer. Line [{i}]")
                            sys.exit()
                        _read = vet[1]
                        write = vet[3]
                        target = vet[5]
                        bp = False

                        # Tratando caracteres especiais
                        # "_" = None
                        if _read == "_":
                            _read = None
                        if write == "_":
                            write = None

                        if source not in vetTrans:
                            vetTrans[source] = (1, {})

                        #Define a posição
                        if vet[4] == "i":
                            pos = 0
                        elif vet[4] == "e":
                            pos = -1
                        elif vet[4] == "d":
                            pos = 1
                        # Identifica Ins com Breakpoint Espaçado
                        if len(vet) == 7 and vet[6] == "!":
                            bp = True
                        # Identifica Ins com Breakpoint
                        elif "!" in vet[5]:
                            bp = True
                            target = target.replace("!","")
                        # Identifica instrução
                        else:
                            bp = False

                        # Target = *
                        if target == "*":
                            target = source
                        elif target == "pare":
                            target = -2
                        elif target == "retorne":
                            target = -1
                        else:
                            try:
                                target = int(target)
                            except Exception as e:
                                print(f"error: Target '{target}' is not a integer/'retorne'/'pare'. Line [{i}]")
                                sys.exit()
                        trans = (write, pos, target, bp)
                        vetTrans[source][1][_read] = trans


        return mt
    return identify()
