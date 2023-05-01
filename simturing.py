#!/usr/bin/env python3

import getopt
import sys
import utils.constants as const
import utils.messages as message
import utils.errors as error
from input import readFile
from machine import Machine


def usage():
    print(message.OPTIONS.format(param=sys.argv[0]))


if __name__ == '__main__':
    options, args = getopt.gnu_getopt(sys.argv, 'rv?bs:h:w:', const.INPUT_OPTIONS_LIST)

    steps = None
    head = '()'
    verbose = False
    word = None
    _break = False

    for opt, value in options:

        if opt in (const.HELP_SYMBOL, const.HELP):
            usage()
            sys.exit(0)

        elif opt in (const.R, const.RESUME):
            if steps:
                print(error.IMPOSSIBLE_RESUME_EXECUTION.format(param=sys.argv[0]))
                sys.exit(-1)
            steps = const.MAX_LEN_STEPS
            verbose = False

        elif opt in (const.V, const.VERBOSE):
            verbose = True

        elif opt in (const.B, const.BREAK):
            _break = True

        elif opt in (const.S, const.STEPS):
            if steps:
                print(error.IMPOSSIBLE_SET_STEPS.format(param=sys.argv[0]))
                sys.exit(-1)
            steps = int(value)
            verbose = True

        elif opt in (const.H, const.HEAD):
            if len(value) != 2:
                print(error.NECESSARY_TWO_CHARS.format(param=sys.argv[0]))
                sys.exit(-1)
            head = value

        elif opt in (const.W, const.WORD):
            if word:
                print(error.DEFINED_TAPE_WORD.format(param=sys.argv[0]))
                sys.exit(-1)
            word = value

        else:
            usage()
            sys.exit(-1)

    if len(args) != 2:
        usage()
        sys.exit(-1)

    ifile = args[1]

    if not steps:
        steps = const.MAX_LEN_STEPS

    if verbose:
        print(message.DEFAULT_MESSAGE)

    procedures = readFile(ifile)
    machine = Machine(procedures, head)

    if not word:
        word = input(message.INPUT_WORD)

    machine.start(word)

    while not machine.run(verbose, steps):

        args = input(message.INPUT_OPTIONS)
        args = args.split()

        try:
            options, _ = getopt.gnu_getopt(args, 'rvbs:', const.MACHINE_OPTIONS_LIST)
        except getopt.GetoptError as e:
            print(f'({sys.argv[0]}) ERROR: {str(e)}')
            continue

        old_steps = steps

        for opt, value in options:

            if opt in (const.R, const.RESUME):
                if steps != old_steps:
                    print(error.CANNOT_RESUME_HERE.format(param=sys.argv[0]))
                    continue
                steps = const.MAX_LEN_STEPS
                verbose = False

            elif opt in (const.V, const.VERBOSE):
                verbose = True

            elif opt in (const.B, const.BREAK):
                _break = True

            elif opt in (const.S, const.STEPS):
                if steps != old_steps:
                    print(error.CANNOT_RESET_NUMBER_STEPS.format(param=sys.argv[0]))
                    continue
                steps = int(value)

            else:
                print(error.UNKNOWN_OPTION.format(param=sys.argv[0]))

        if _break:
            break

    final = machine.tape
    print(final)
