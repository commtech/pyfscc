import os

# chose an implementation, depending on os
if os.name == 'nt':
    from list_ports_windows import *
elif os.name == 'posix':
    from list_ports_linux import *

if __name__ == '__main__':
    print(sorted(fsccports()))
