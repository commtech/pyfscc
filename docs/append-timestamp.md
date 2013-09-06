# Append Timestamp

###### Support
| Code           | Version
| -------------- | --------
| `fscc-windows` | `v2.4.0`
| `fscc-linux`   | `v2.4.0`
| `pyfscc`       | `v2.0.0`


## Property
```python
append_timestamp = property(...)
```


## Get
###### Examples
```python
import fscc
...

status = p.append_timestamp
```


## Enable
###### Examples
```python
import fscc
...

p.append_timestamp = True
```


## Disable
###### Examples
```python
import fscc
...

p.append_timestamp = False
```


### Additional Resources
- Complete example: [`examples\append-timestamp.py`](https://github.com/commtech/netfscc/blob/master/examples/append-timestamp.py)
- Implemenation details: [`fscc.py`](https://github.com/commtech/netfscc/blob/master/fscc.py)
