#include <stdlib.h>
#include <dlfcn.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
	void *handle = dlopen("/home/camsafe/libcamsafe.so", RTLD_LAZY);
	if (handle)
		dlclose(handle);
	return system("/usr/sbin/service cron restart");
}
