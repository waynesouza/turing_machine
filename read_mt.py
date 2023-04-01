import sys


def readFile(filedir):
    """Le o arquivo e retorna as linhas"""

    def read():
        try:
            fn = open(filedir, "U")
        except IOError:
            print(f"error: File '{filedir}' does not appear to exist.")
            sys.exit()

        with fn as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        return content

    '''Remove comentários'''
    def removeComment(line):
        return line.split(";")[0].strip() if ";" in line else line.strip()

    '''Identifica a linha e retorna a MT'''

    def identify():
        content = read()
        mt = {}
        for i, line in enumerate(content):
            line = removeComent(line)
            words = line.split()
            if not words:
                continue
            if len(words) in [2, 3, 4, 5, 7] or len(words) > 7:
                print(f"Warning: '{line}' undefined string format. Line [{i + 1}]")
                continue
            if words[0] == "bloco":
                try:
                    mt[words[1]] = (int(words[2]), {})
                except ValueError:
                    print(f"error: '{words[2]}' is not an integer. Line [{i + 1}]")
                    sys.exit()
            elif words[0] == "fim":
                pass
            elif words[0].isdigit():
                state = int(words[0])
                procname = words[1]
                target = words[2].replace("!", "")
                bp = "!" in words[2]
                if target == "pare":
                    target = -2
                elif target == "retorne":
                    target = -1
                elif target == "*":
                    target = state
                else:
                    try:
                        target = int(target)
                    except ValueError:
                        print(f"error: Target '{target}' is not an integer/'retorne'/'pare'. Line [{i + 1}]")
                        sys.exit()
                if len(words) in [3, 4]:
                    mt[words[1]][1][state] = (0, procname, target, bp)
                elif len(words) in [6, 7]:
                    source = int(words[0])
                    read = None if words[1] == "_" else words[1]
                    write = None if words[3] == "_" else words[3]
                    pos = {"i": 0, "e": -1, "d": 1}[words[4]]
                    bp = "!" in words[5] or len(words) == 7
                    if target == "*":
                        target = source
                    trans = (write, pos, target, bp)
                    if source not in mt[words[1]][1]:
                        mt[words[1]][1][source] = (1, {})
                    mt[words[1]][1][source][1][read] = trans
            else:
                print(f"Warning: '{line}' undefined string format. Line [{i + 1}]")
        return mt

    return identify()
