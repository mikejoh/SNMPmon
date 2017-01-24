# SNMPmon
Another SNMP tool written in Python, primarily used in Nagios/OP5 plugin scripting. 

### Usage
 1. Add a file called SNMPmon.cfg in your working directory, this file will include all the OIDs that you would want to use for querying a SNMP agent. See example file.
 2. Add your SNMP communities to the file.
 3. Based on the network device you want to monitor using SNMP it will fetch the correct community.

