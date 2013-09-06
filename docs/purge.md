# Purge
Between the hardware FIFO and the driver's software buffers there are multiple
places data could be stored, excluding your application code. If you ever need
to clear this data and start fresh, there are a couple of methods you can use.

###### Driver Support
| Code           | Version
| -------------- | --------
| `fscc-windows` | `v2.0.0`
| `fscc-linux`   | `v2.0.0`
| `pyfscc`       | `v1.0.0`


## Execute
```python
def purge(self, tx=True, rx=True)
```

###### Examples
Purge both the transmit and receive data.
```python
using Fscc;
...

p.Purge(True, True)
```

Purge only the transmit data.
```python
using Fscc;
...

p.Purge(True, False)
```

Purge only the receive data.
```python
using Fscc;
...

p.Purge(False, True)
```


### Additional Resources
- Complete example: [`examples\purge.py`](https://github.com/commtech/pyfscc/blob/master/examples/purge.py)
- Implemenation details: [`src\fscc.py`](https://github.com/commtech/pyfscc/blob/master/src/fscc.py)