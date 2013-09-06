import fscc

if __name__ == '__main__':
    p = Port(0)

    p.registers.CCR0 = 0x0011201c
    p.registers.BGR = 10

    ccr1 = p.registers.CCR1
    ccr2 = p.registers.CCR2

    p.ignore_timeout = True
    p.ignore_timeout = False
