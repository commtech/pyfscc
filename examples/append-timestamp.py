import fscc

if __name__ == '__main__':
    p = Port(0)

    status = p.append_timestamp

    p.append_timestamp = True
    p.append_timestamp = False
