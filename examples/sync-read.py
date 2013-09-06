#include <stdlib.h>
#include <fscc.h>

int main(void)
{
	fscc_handle h;
    char data[20];
    unsigned bytes_read = 0;

	fscc_connect(0, 0, &h);

	fscc_read(h, data, sizeof(data), &bytes_read, 0);

	fscc_disconnect(h);

	return EXIT_SUCCESS;
}
