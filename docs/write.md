# Write


###### Driver Support
| Code           | Version
| -------------- | --------
| `fscc-windows` | `v2.0.0` 
| `fscc-linux`   | `v2.0.0` 
| `pyfscc`       | `v1.0.0`


## Write
```python
def write(self, data):
```

| Parameter    | Type    | Description
| ------------ | ------- | ---------------------------
| `buf`        | `bytes` | The data buffer to transmit

| Return
| ---------------------------
| Number of bytes transmitted

| Exception           | Cause
| ------------------- | --------------------------------------------------------------------
| TimeoutError        | You are executing a command that requires a transmit clock present
| BufferTooSmallError | The read size is smaller than the next frame (in a frame based mode)

###### Examples
```c
import fscc
...

p.write(b'Hello world!')
```


### Additional Resources
- Complete example: [`examples\tutorial.py`](https://github.com/commtech/pyfscc/blob/master/examples/tutorial.py)
- Implemenation details: [`fscc.py`](https://github.com/commtech/pyfscc/blob/master/fscc.py)
