
#include <sys/types.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdio.h>
#include <termios.h>
#include <fcntl.h>
#include <sstream>
#include <string>
#include <iomanip>
#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <linux/types.h>

#include "../include/DmaDriver.h"
#include "PgpDaq.hh"

using namespace std;

static void usage(const char* p)
{
  printf("Usage: %s <options>\n",p);
  printf("Options:\n");
  printf("\t-d <device>  [e.g. /dev/pgpdaq0]\n");
}

int main (int argc, char **argv) {

  int          fd;
  const char*  dev = "/dev/pgpdaq0";
  int c;

  while((c=getopt(argc,argv,"d:")) != EOF) {
    switch(c) {
    case 'd': dev    = optarg; break;
    default: usage(argv[0]); return 0;
    }
  }

  if ( (fd = open(dev, O_RDWR)) <= 0 ) {
    cout << "Error opening " << dev << endl;
    return(1);
  }

  //
  //  Map the lanes to this reader and flush
  //
  {
    PgpDaq::PgpCard* p = (PgpDaq::PgpCard*)mmap(NULL, sizeof(PgpDaq::PgpCard), (PROT_READ|PROT_WRITE), (MAP_SHARED|MAP_LOCKED), fd, 0);   
    uint32_t MAX_LANES = p->nlanes();
    unsigned client    = p->nclients();
    for(unsigned i=0; i<MAX_LANES; i++)
      p->dmaLane[i].client = client;
  }

  close(fd);
  return 0;
}
