# Memory Cap

###### Support
| Code           | Version
| -------------- | --------
| `fscc-windows` | `v2.0.0` 
| `fscc-linux`   | `v2.0.0` 
| `pyfscc`       | `v1.0.0`


## Property
```python
memory_cap = property(...)
```


## Get
###### Examples
```python
import fscc
...

input = p.memory_cap.input
output = p.memory_cap.output
```


## Set
###### Examples
```python
import fscc
...

p.memory_cap.input = 1000000
p.memory_cap.output = 2000000
```


### Additional Resources
- Complete example: [`examples\append-status.py`](https://github.com/commtech/pyfscc/blob/master/examples/append-status.py)
- Implemenation details: [`src\Fscc.py`](https://github.com/commtech/pyfscc/blob/master/fscc.py)
