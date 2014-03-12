# Memory Cap

###### Support
| Code | Version |
| ---- | ------- |
| fscc-windows | 2.0.0 |
| fscc-linux | 2.0.0 |
| pyfscc | 1.0.0 |


## Property
```python
memory_cap = property(...)
```


## Get
###### Examples
```python
import fscc
...

input_cap = p.memory_cap.input
output_cap = p.memory_cap.output
```


## Set
###### Examples
```python
import fscc
...

p.memory_cap.input = 1000000  # 1MB
p.memory_cap.output = 1000000  # 1MB
```


### Additional Resources
- Complete example: [`examples/memory-cap.py`](../examples/memory-cap.py)
- Implementation details: [`fscc.py`](../fscc/port.py)
