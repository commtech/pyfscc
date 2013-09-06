#include <stdlib.h>
#include <fscc.h>

int main(void)
{
	fscc_handle h;
    char data[] = "Hello world!";
    unsigned bytes_written = 0;

	fscc_connect(0, 0, &h);

	fscc_write(h, data, sizeof(data), &bytes_written, 0);

	fscc_disconnect(h);

	return EXIT_SUCCESS;
}
