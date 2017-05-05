# bind_logstat.py

A simple frequency analysis script for bind9 DNS query logs.  Is able to analyze based on client IP address, DNS domain name, and DNS query type.  Uses both regular expressions, and the Counter() dictionary from the Python collections module.  Is written to demonstrate how useful the combination of a Counter() dictionary and regular expressions are.

**Usage:**

`usage: bind_logstat.py [-h] [--exclude [EXCLUDE [EXCLUDE ...]]]
                       [--qtype [QTYPE [QTYPE ...]]] [--client CLIENT]
                       [--domain DOMAIN] [--view VIEW] [--topn TOPN] [--debug]
                       filename`


**Author: Joff Thyer
Black Hills Information Security**

<a href="http://www.blackhillsinfosec.com">
<img src="http://www.blackhillsinfosec.com/wp-content/uploads/2016/03/BHIS-logo-L.png" width=200px>
</a>
