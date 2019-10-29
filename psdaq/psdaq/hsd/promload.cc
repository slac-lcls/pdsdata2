#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include "psdaq/hsd/ModuleBase.hh"

using Pds::HSD::ModuleBase;
using Pds::HSD::FlashController;

void usage(const char* p) {
  printf("Usage: %s -d <dev> -f <file> [-r]\n",p);
}

int main(int argc, char** argv) {
  extern char* optarg;

  const char* devName = 0;
  const char* fname = 0;
  bool lread = false;
  int c;
  while ( (c=getopt( argc, argv, "d:f:rF")) != EOF ) {
    switch(c) {
    case 'd': devName = optarg; break;
    case 'f': fname = optarg; break;
    case 'r': lread = true; break;
    case 'F': FlashController::useFifo(false); break;
    default:
      break;
    }
  }

  if (!devName || !fname) {
    printf("Missing required arguments\n");
    usage(argv[0]);
    return 0;
  }

  int fd = open(devName, O_RDWR);
  if (fd<0) {
    perror("Open device failed");
    return -1;
  }

  if (lread) {
    std::vector<uint8_t> v = ModuleBase::create(fd)->flash.read (8*1024*1024);
    int ffd = open(fname, O_EXCL | O_CREAT | O_RDWR);
    write(ffd, v.data(), v.size());
    close(ffd);
  }
  else
    ModuleBase::create(fd)->flash.write(fname);

  return 0;
}
