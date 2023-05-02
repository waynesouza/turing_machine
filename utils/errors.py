ERROR = f'ERROR: '
IMPOSSIBLE_RESUME_EXECUTION = f'({{param}}) {ERROR} impossible to resume execution'
IMPOSSIBLE_SET_STEPS = f'({{param}}) {ERROR} it is not possible to set a number of steps for execution'
NECESSARY_TWO_CHARS = f'({{param}}) {ERROR} it is necessary to have 2 characters for the tape head. For example: "<>"'
DEFINED_TAPE_WORD = f'({{param}}) {ERROR} the tape word has already been defined'
CANNOT_RESET_NUMBER_STEPS = f'({{param}}) {ERROR} cannot reset the number of steps'
UNKNOWN_OPTION = f'({{param}}) {ERROR} unknown option'
UNDEFINED_PROCEDURE = f'{ERROR} procedure {{param}} not defined'
FILE_NOT_EXISTS = f'{ERROR} file {{param}} does not appear to exist'
VALUE_NOT_INTEGER = f'{ERROR} {{param}} is not a integer. Line [{{line}}]'

WARNING = f'WARNING: '
CANNOT_RESUME_HERE = f'({{param}}) {WARNING} cannot resume execution here'
UNDEFINED_STRING_FORMAT = f'{WARNING} {{param}} undefined string format. Line [{{line}}]'
