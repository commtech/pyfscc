# Ignore Timeout

###### Support
| Code | Version |
| ---- | ------- |
| fscc-windows | 2.0.0 |
| fscc-linux | 2.0.0 |
| pyfscc | 1.0.0 |


## Property
```python
ignore_timeout = property(...)
```


## Get
###### Examples
```python
import fscc
...

status = p.ignore_timeout
```


## Enable
###### Examples
```python
import fscc
...

p.ignore_timeout = True
```


## Disable
###### Examples
```python
import fscc
...

p.ignore_timeout = False
```


### Additional Resources
- Complete example: [`examples/ignore-timeout.py`](../examples/ignore-timeout.py)
- Implementation details: [`fscc.py`](../fscc/port.py)
