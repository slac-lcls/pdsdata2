import sys
import logging

from psdaq.epicstools.PVAServer import PVAServer
import time
from datetime import datetime
import argparse
#import socket
#import json
import pdb

NDsLinks    = 7
NAmcs       = 2
NPartitions = 16

def printDb():
    global pvdb
    global prefix

    print('=========== Serving %d PVs ==============' % len(pvdb))
    for key in sorted(pvdb):
        print(prefix+key)
    print('=========================================')
    return

def addTiming(sec):
    pvdb[sec+':RxClks'     ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':TxClks'     ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':RxRsts'     ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':CrcErrs'    ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':RxDecErrs'  ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':RxDspErrs'  ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':BypassRsts' ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':BypassDones'] = {'type' : 'float', 'value': 0}
    pvdb[sec+':RxLinkUp'   ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':FIDs'       ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':SOFs'       ] = {'type' : 'float', 'value': 0}
    pvdb[sec+':EOFs'       ] = {'type' : 'float', 'value': 0}

def main():
    global pvdb
    pvdb = {}     # start with empty dictionary
    global prefix
    prefix = ''

    parser = argparse.ArgumentParser(prog=sys.argv[0], description='host PVs for XPM')

    parser.add_argument('-P', required=True, help='e.g. DAQ:LAB2:XPM:1', metavar='PREFIX')
    parser.add_argument('-v', '--verbose', action='store_true', help='be verbose')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    prefix = args.P

    # PVs
#    pvdb[':PARTITIONS'         ] = {'type' : 'int', 'value' : 255}
    pvdb[':PAddr'              ] = {'type' : 'int'}
#    pvdb[':FwBuild'            ] = {'type' : 'char', 'count':256}
    pvdb[':FwBuild'            ] = {'type' : 'string', 'value':'None' }
    pvdb[':ModuleInit'         ] = {'type' : 'int'}
    for i in range(NAmcs):
        pvdb[':DumpPll' + '%d'%i] = {'type' : 'int'}

    for i in range(2):
        pvdb[':DumpTiming%d'%i ] = {'type' : 'int'}

    pvdb[':Inhibit'            ] = {'type' : 'int'}
    pvdb[':TagStream'          ] = {'type' : 'int'}
    pvdb[':DumpSeq'            ] = {'type' : 'int'}
    pvdb[':SetVerbose'         ] = {'type' : 'int'}

    LinkEnable = [0]*32
    LinkEnable[17:19] = [1]*3  # DTIs in slots 3-5
    LinkEnable[4] = 1   # HSD on dev03
    LinkEnable[7] = 1   # HSD on dev02
    print(LinkEnable)

    for i in range(32):
        pvdb[':LinkTxDelay'  +'%d'%i] = {'type' : 'int'}
        pvdb[':LinkPartition'+'%d'%i] = {'type' : 'int'}
        pvdb[':LinkTrgSrc'   +'%d'%i] = {'type' : 'int'}
        pvdb[':LinkLoopback' +'%d'%i] = {'type' : 'int'}
        pvdb[':TxLinkReset'  +'%d'%i] = {'type' : 'int'}
        pvdb[':RxLinkReset'  +'%d'%i] = {'type' : 'int'}
        pvdb[':RxLinkDump'   +'%d'%i] = {'type' : 'int'}
        pvdb[':LinkEnable'   +'%d'%i] = {'type' : 'int', 'value' : LinkEnable[i] }
        pvdb[':LinkTxReady'  +'%d'%i] = {'type' : 'int'}
        pvdb[':LinkRxReady'  +'%d'%i] = {'type' : 'int'}
        pvdb[':LinkTxResetDone'  +'%d'%i] = {'type' : 'int'}
        pvdb[':LinkRxResetDone'  +'%d'%i] = {'type' : 'int'}
        pvdb[':LinkRxRcv'    +'%d'%i] = {'type' : 'int'}
        pvdb[':LinkRxErr'    +'%d'%i] = {'type' : 'int'}
        pvdb[':LinkIsXpm'    +'%d'%i] = {'type' : 'int'}
        pvdb[':RemoteLinkId'  +'%d'%i] = {'type' : 'int'}

    for i in range(14):
        pvdb[':LinkLabel'    +'%d'%i] = {'type' : 'string', 'value' : 'FP-%d'%i}

    for i in range(16,21):
        pvdb[':LinkLabel'    +'%d'%i] = {'type' : 'string', 'value' : 'BP-%d'%(i-13)}

    pvdb[':LinkId'] = {'type' : 'int', 'count' : 22}

    for i in range(NAmcs):
        pvdb[':PLL_LOS'       +'%d'%i] = {'type' : 'int'}
        pvdb[':PLL_LOL'       +'%d'%i] = {'type' : 'int'}
        pvdb[':PLL_BW_Select' +'%d'%i] = {'type' : 'int', 'value': 7}
        pvdb[':PLL_FreqTable' +'%d'%i] = {'type' : 'int', 'value': 2}
        pvdb[':PLL_FreqSelect'+'%d'%i] = {'type' : 'int', 'value': 89}
        pvdb[':PLL_Rate'      +'%d'%i] = {'type' : 'int', 'value': 10}
        pvdb[':PLL_PhaseInc'  +'%d'%i] = {'type' : 'int'}
        pvdb[':PLL_PhaseDec'  +'%d'%i] = {'type' : 'int'}
        pvdb[':PLL_Bypass'    +'%d'%i] = {'type' : 'int'}
        pvdb[':PLL_Reset'     +'%d'%i] = {'type' : 'int'}
        pvdb[':PLL_Skew'      +'%d'%i] = {'type' : 'int'}

    addTiming('')   # For old XPM firmware
    addTiming(':Us')
    addTiming(':Cu')

    pvdb[':RecClk'     ] = {'type' : 'float', 'value': 0}
    pvdb[':FbClk'      ] = {'type' : 'float', 'value': 0}
    pvdb[':BpClk'      ] = {'type' : 'float', 'value': 0}
    for i in range(8):
        pvdb[':PART:%d:DeadFLnk' %i] = {'type' : 'float', 'count': 32, 'value': [-1.]*32 }

    for i in range(8):
        pvdb[':PART:%d:DeadFLnk' %i] = {'type' : 'float', 'count': 32, 'value': [-1.]*32 }

    # printDb(pvdb, prefix)
    printDb()

    server = PVAServer(__name__)
    server.createPV(prefix, pvdb)

    try:
        # process PVA transactions
        server.forever()
    except KeyboardInterrupt:
        print('\nInterrupted')

if __name__ == '__main__':
    main()
