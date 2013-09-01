# TX Modifiers

It is a good idea to pay attention to the status of each frame. For example,
you may want to see if the frame's CRC check succeeded or failed.

The FSCC reports this data to you by appending two additional bytes to each
frame you read from the card, if you opt-in to see this data. There are a few
methods of enabling this additional data.

###### Support
| Code           | Version
| -------------- | --------
| `fscc-windows` | `v2.0.0`
| `fscc-linux`   | `v2.0.0`
| `pyfscc`       | `v1.0.0`


## Property
```python
tx_modifiers = property(...)
```


## Get
###### Examples
```python
import fscc
...

status = p.tx_modifiers
```


## Set
###### Examples
```python
import fscc
...

p.tx_modifiers = XF | XREP
```


### Additional Resources
- Complete example: [`examples\tx-modifiers.py`](https://github.com/commtech/netfscc/blob/master/examples/tx-modifiers.py)
- Implemenation details: [`fscc.py`](https://github.com/commtech/netfscc/blob/master/fscc.py)
