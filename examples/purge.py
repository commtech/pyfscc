import fscc

if __name__ == '__main__':
    p = fscc.Port(0)

    # Purge TX
    p.purge(True, False)

    # Purge RX
    p.purge(False, True)

    # Purge both TX & RX
    p.purge(True, True)
