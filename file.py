import sys
import utils.constants as const
import utils.errors as error


def read_file(directory):

    def read():
        try:
            fn = open(directory, 'U')
        except IOError:
            print(error.FILE_NOT_EXISTS.format(param=directory))
            sys.exit()

        with fn as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        return content

    def remove_comment(line):
        return line.split(';')[0] if ';' in line else line

    def identify():
        content = read()
        block = False
        mt = {}
        vet_trans = {}
        pos = 0
        i = 0
        for c in content:
            c = remove_comment(c)
            i += 1
            vet = c.split()
            if len(vet) > 0:
                if len(vet) == 2 or len(vet) > 6 or (len(vet) == 1 and const.END not in vet[0]) \
                        or (len(vet) == 3 and const.BLOCK not in vet[0] and block is False):
                    print(error.UNDEFINED_STRING_FORMAT.format(param=c, line=i))
                if block is False and vet[0] == const.BLOCK:
                    block = True
                    try:
                        mt[vet[1]] = (int(vet[2]), {})
                    except ValueError:
                        print(error.VALUE_NOT_INTEGER.format(param=vet[2], line=i))
                        sys.exit()
                    vet_trans = mt[vet[1]][1]
                    t = {}
                    s = {}
                elif vet[0] == const.END:
                    block = False
                elif block is True:
                    try:
                        state = int(vet[0])
                    except ValueError:
                        print(error.VALUE_NOT_INTEGER.format(param=vet[0], line=i))
                        sys.exit()
                    procname = vet[1]
                    target = vet[2]
                    bp = False

                    if len(vet) == 4 and vet[3] == const.BREAKPOINT:
                        bp = True
                    if len(vet) == 3 or len(vet) == 4:
                        if const.BREAKPOINT in vet[2]:
                            bp = True
                            target = target.replace(const.BREAKPOINT, const.EMPTY)

                        if target == const.CONST_STOP_TEXT:
                            target = -2
                        elif target == const.CONST_RETURN_TEXT:
                            target = -1
                        elif target == const.WILDCARD:
                            target = state
                        else:
                            try:
                                target = int(target)
                            except ValueError:
                                print(error.VALUE_NOT_INTEGER.format(param=target, line=i))
                                sys.exit()
                        vet_trans[state] = (0, procname, target, bp)

                    if len(vet) == 6 or len(vet) == 7:
                        try:
                            source = int(vet[0])
                        except ValueError:
                            print(error.VALUE_NOT_INTEGER.format(param=target, line=i))
                            sys.exit()
                        _read = vet[1]
                        write = vet[3]
                        target = vet[5]
                        bp = False

                        if _read == const.UNDERLINE:
                            _read = None
                        if write == const.UNDERLINE:
                            write = None

                        if source not in vet_trans:
                            vet_trans[source] = (1, {})

                        if vet[4] == const.IMMOBILE:
                            pos = 0
                        elif vet[4] == const.LEFT:
                            pos = -1
                        elif vet[4] == const.RIGHT:
                            pos = 1
                        if len(vet) == 7 and vet[6] == const.BREAKPOINT:
                            bp = True
                        elif const.BREAKPOINT in vet[5]:
                            bp = True
                            target = target.replace(const.BREAKPOINT, const.EMPTY)
                        else:
                            bp = False

                        if target == const.WILDCARD:
                            target = source
                        elif target == const.CONST_STOP_TEXT:
                            target = -2
                        elif target == const.CONST_RETURN_TEXT:
                            target = -1
                        else:
                            try:
                                target = int(target)
                            except ValueError:
                                print(error.VALUE_NOT_INTEGER.format(param=target, line=i))
                                sys.exit()
                        trans = (write, pos, target, bp)
                        vet_trans[source][1][_read] = trans

        return mt
    return identify()
