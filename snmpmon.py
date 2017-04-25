import argparse
import sys
import ConfigParser
from pysnmp.entity.rfc3413.oneliner import cmdgen

config = ConfigParser.RawConfigParser()

config.read('./SNMPmon.cfg')

communities = dict(config.items('Communities'))

parser = argparse.ArgumentParser(description='SNMPmon - aggregated monitoring via SNMP.')
parser.add_argument('-l', '--list', help='List all possible checks for the type of device being monitored', action='store_true')
parser.add_argument('-H', '--host', help='IP address of host being monitored', required=True)
parser.add_argument('-d', '--device', help='Set the type of device to be monitored', default='Example')
parser.add_argument('-c', '--check', help='What SNMP check to do against a device', required=True)

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

if args.list:
    print 'Possible checks that can by done against ' + args.device + ':'
    print
    print '\tName:' + '\t\t' + 'OID:'
    for item in config.items(args.device):
        print '\t' + item[0] + '\t' + item[1]
    sys.exit(0)

device = args.device.lower()
ip = args.host
check = args.check

if device == 'juniper':
    deviceobjs = dict(config.items('Juniper'))
    community = communities['juniper']
elif device == 'cisco':
    deviceobjs = dict(config.items('Cisco'))
    community = communities['cisco']
elif device == 'f5':
    deviceobjs = dict(config.items('F5'))
    community = communities['f5']
elif device == 'junipersa':
    deviceobjs = dict(config.items('Juniper SA'))
    community = communities['junipersa']

try:
    errorIndication, errorStatus, errorIndex, varBinds = \
        cmdgen.CommandGenerator().nextCmd(
        cmdgen.CommunityData('SNMPmon', community, 0),
        cmdgen.UdpTransportTarget((ip, 161)),
        deviceobjs[check]
        )

    c = 0
    retlist = []

    for o in varBinds:
        c += 1
        if c > 1:
            retlist[c] = o
        else:
            retval = o[0][1]
            print retval
            sys.exit(0)

        print retlist

except Exception as e:
    print e.message
    sys.exit(1)
