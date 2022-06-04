#!/usr/bin/env python3

import requests, json, sys, urllib3, argparse
#Disable self signed or internally signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser=argparse.ArgumentParser(description="A Nagios script to check the license consumption of a Splunk instance.")
parser.add_argument("--hostname","-H",type=str,help="Your Splunk hostname",required=True)
parser.add_argument("--port","-p",type=str,help="Your Splunk REST API port. Defaults to 8089",required=False)
parser.add_argument("--api_key","-a",type=str,help="Your Splunk Authorization Token. More information can be found here: ",required=True)
parser.add_argument("--warning","-w",type=int,help="The % at which to generate a warning. Defaults to 80% of total license.",required=False)
parser.add_argument("--critical","-c",type=int,help="The % at which to generate a critical. Defaults to 90% of total license.",required=False)

args = parser.parse_args()

#Error checking early on
if (args.critical is not None):
    if (args.critical >= 100):
        print("ERROR! Your value for critical " + str(args.critical)  + "% is too high. The value should be as a percentage of available license to consume.")
        sys.exit(2)

if (args.warning is not None):
    if (args.warning >= 100):
        print("ERROR! Your value for warning " + str(args.warning)  + "% is too high. The value should be as a percentage of available license to consume.")
        sys.exit(2)

if (args.critical and args.warning is not None):
    if (args.critical <= args.warning):
        print("ERROR! Your critical value " + str(args.critical) + " is lower than your warning value " + str(args.warning) + ". You might want to check that.")
        sys.exit(2)


if (args.port is None):
    port = "8089"
else:
    port = args.port

#Build the API query
headers = {'Authorization': 'Bearer {}'.format(args.api_key)}
params = {'output_mode': 'json'}
search_api_url = 'https://' + args.hostname + ':' + port + '/services/licenser/usage'

response = requests.get(search_api_url, headers=headers, params=params, verify=False)

content = response.json()

quota = int(content["entry"][0]["content"]["quota"])
consumed = int(content["entry"][0]["content"]["slaves_usage_bytes"])
percent = round(consumed / quota * 100, 2)
consumed_str = str(percent)

if (args.warning is None):
    warning = int(quota * 0.8)
else:
    warning = int(quota * args.warning / 100)

if (args.critical is None):
    critical = int(quota * 0.9)
else:
    critical = int(quota * args.critical / 100)

#quota_readable =

if consumed >= critical:
    print ("CRITICAL: License consumption is " + consumed_str + "%")
    sys.exit(2)
elif consumed >= warning:
    print ("WARNING: License consumption is at " + consumed_str + "%")
    sys.exit(1)
else:
    print ("OK: License consumption is at " + consumed_str + "%")
    sys.exit(0)
