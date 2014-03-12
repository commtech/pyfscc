import fscc

if __name__ == '__main__':
    p = fscc.Port(0)

    p.memory_cap.input = 1000000  # 1 MB
    p.memory_cap.output = 1000000  # 1 MB

    input = p.memory_cap.input
    output = p.memory_cap.output