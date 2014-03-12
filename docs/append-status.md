# Append Status

It is a good idea to pay attention to the status of each frame. For example, you may want to see if the frame's CRC check succeeded or failed.

The FSCC reports this data to you by appending two additional bytes to each frame you read from the card, if you opt-in to see this data. There are a few methods of enabling this additional data.

###### Support
| Code | Version |
| ---- | ------- |
| fscc-windows | 2.0.0 |
| fscc-linux | 2.0.0 |
| pyfscc | 1.0.0 |


## Property
```python
append_status = property(...)
```


## Get
###### Examples
```python
import fscc
...

status = p.append_status
```


## Enable
###### Examples
```python
import fscc
...

p.append_status = True
```


## Disable
###### Examples
```python
import fscc
...

p.append_status = False
```


### Additional Resources
- Complete example: [`examples/append-status.py`](../examples/append-status.py)
- Implementation details: [`fscc.py`](../fscc/port.py)
