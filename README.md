# FSCC Python Library (pyfscc)
This README file is best viewed [online](http://github.com/commtech/pyfscc/).

## Installing Library

##### Downloading Library
- You can use the pre-built library files that are included with the driver
- Or, you can download the latest library version from [Github releases](https://github.com/commtech/pyfscc/releases).


##### Installing Driver
If you are not using the included Windows installer, you can install the library by using the setup script.

```
python setup.py install
```


## Quick Start Guide

Lets get started with a quick programming example for fun.

_This tutorial has already been set up for you at_ [`examples/tutorial.py`](examples/tutorial.py).

First, create a new Python file (named tutorial.py) with the following code.

```python
import fscc

if __name__ == '__main__':
    p = fscc.Port(0)

    p.write(b'Hello world!')
    print(p.read(100)[0])
```

Now attach the included loopback connector.

```
# python tutorial.py
b'Hello world!'
```

You have now transmitted and received an HDLC frame!


## API Reference

There are likely other configuration options you will need to set up for your own program. All of these options are described on their respective documentation page.

- [Connect](docs/connect.md)
- [Append Status](docs/append-status.md)
- [Append Timestamp](docs/append-timestamp.md)
- [Clock Frequency](docs/clock-frequency.md)
- [Ignore Timeout](docs/ignore-timeout.md)
- [Memory Cap](docs/memory-cap.md)
- [Purge](docs/purge.md)
- [Read](docs/read.md)
- [Registers](docs/registers.md)
- [RX Multiple](docs/rx-multiple.md)
- [Track Interrupts](docs/track-interrupts.md)
- [TX Modifiers](docs/tx-modifiers.md)
- [Writes](docs/write.md)


## Run-time Dependencies
- [Python 3](http://www.python.org/download/) (32-bit)
- [cfscc](https://github.com/commtech/cfscc/) (Included)
- OS: Windows XP+ & Linux


## API Compatibility
We follow [Semantic Versioning](http://semver.org/) when creating releases.


## License

Copyright (C) 2013 [Commtech, Inc.](http://commtech-fastcom.com)

Licensed under the [GNU General Public License v3](http://www.gnu.org/licenses/gpl.txt).
