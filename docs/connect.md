# Connect

Opening a handle using this API will only give you access to the synchronous functionality of the card. You will need to use the COM ports if you would like to use the asynchronous functionality.

###### Driver Support
| Code | Version |
| ---- | ------- |
| fscc-windows | 2.0.0 |
| fscc-linux | 2.0.0 |
| pyfscc | 1.0.0 |


## Connect
```python
def __init__(self, port_num, append_status=True, append_timestamp=True)
```

| Exception | Base Exception | Cause |
| --------- | -------------- |------ |
| `PortNotFoundError` | `OSError` | Port not found |
| `InvalidAccessError` | `OSError` | Insufficient permissions |

###### Examples
```python
import fscc
...

p = fscc.Port(0)
```


### Additional Resources
- Complete example: [`examples/tutorial.py`](../examples/tutorial.py)
- Implementation details: [`fscc.py`](../fscc/port.py)
