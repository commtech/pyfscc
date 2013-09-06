# Write


###### Driver Support
| Code           | Version
| -------------- | --------
| `fscc-windows` | `v2.0.0` 
| `fscc-linux`   | `v2.0.0` 


## Write
```c
int fscc_write(fscc_handle h, char *buf, unsigned size, unsigned *bytes_written, OVERLAPPED *o)
```

| Parameter    | Type             | Description
| ------------ | ---------------- | -----------------------
| `h`          | `fscc_handle`    | The handle to your port
| `buf`        | `char *`         | The data buffer to transmit
| `size`       | `unsigned`       | The number of bytes to transmit
| `bytes_read` | `unsigned *`     | How many bytes were written to the read
| `o`          | `OVERLAPPED *`   | [Overlapped IO structure](http://msdn.microsoft.com/en-us/library/windows/desktop/ms686358.aspx)

| Return Value            | Cause
| ----------------------- | ------------------------------------------------------------------
| 0                       | Success
| `FSCC_BUFFER_TOO_SMALL` | The write size exceeds the output memory usage cap
| `FSCC_TIMEOUT`          | You are executing a command that requires a transmit clock present

###### Examples
```c
#include <fscc.h>
...

char odata[] = "Hello world!";
unsigned bytes_written;

fscc_write(h, odata, sizeof(odata), &bytes_written, NULL);
```

###### Support
| Code           | Version
| -------------- | --------
| `cfscc`        | `v1.0.0`


### Additional Resources
- Complete example: [`examples\tutorial.cs`](https://github.com/commtech/netfscc/blob/master/examples/tutorial.cs)
- Implemenation details: [`src\Fscc.cs`](https://github.com/commtech/netfscc/blob/master/src/fscc.cs)
