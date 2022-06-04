# check_splunk_license_usage.py

A python3 script to check your Splunk license usage.

This script relies on you setting up Splunk Authentication Tokens as per https://docs.splunk.com/Documentation/Splunk/8.2.6/Security/CreateAuthTokens

Download and install the script to your Nagios/Icinga/etc plugin directory and then set the chmod to allow it to execute.

Usage: ./check_splunk_license_usage.py -H hostname -a token -p port -w warning -c critical

Hostname and Token are required, all other values are set to the following defaults:
1) Port = 8089
2) Warning = 80%
3) Critical = 90%
