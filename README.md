
# censys-subdomain-finder-none-api
Using censys to [find subdomains](https://www.nmmapper.com/sys/tools/subdomainfinder/) but without the APIs. Censys is a a known service offering lots of information on a variety of networks. That is what we use on our online service, only if we have hit the limit given to us. Thanks to Censys search.

[![N|Solid](https://www.nmmapper.com/static/img/logo.png)](https://www.nmmapper.com/sys/tools/subdomainfinder/)

Part of this code is taken from theharvester as it currently uses the none api approach.
- [theHarvester online](https://www.nmmapper.com/kalitools/theharvester/email-harvester-tool/online/)

- [theHarvester repo](https://github.com/laramies/theHarvester)
- [Censys is hosted online](https://www.nmmapper.com/sys/tools/subdomainfinder/)

# Dependencies!
   - beautifulsoup4
   - censys
   - dnspython
   - requests
```sh
$ pip3 install -r requirements.txt
```
```sh
$ python3 censys_subdomain_finder.py  -d nmmapper.com
	Searching certificates results page 2.
	Searching certificates results page 3.
	Searching certificates results page 4.
	Searching certificates results page 5.

[
    "p352931.goaccess.nmmapper.com",
    "clk.nmmapper.com",
    "d1.nmmapper.com",
    "*.nmmapper.com",
    "celery.nmmapper.com",
    "www.nmmapper.com",
    "a2.nmmapper.com",
    "p352931.nmmapper.com",
    "analytics.nmmapper.com",
    "p352931-cdn.nmmapper.com",
    "upstream.d.nmmapper.com",
    "p0-cdn.nmmapper.com",
    "upstream.nmmapper.com",
    "mail.nmmapper.com",
    "goaccess.nmmapper.com",
    "a1.nmmapper.com",
    "nmmapper.com"
]
```

Limiting the query with 
```sh
$ python3 censys_subdomain_finder.py  --d nmmapper.com  -l 2000
```
### Cross-Selling
If you like this project you might also be interested in
* [Dnsdumpster](https://github.com/wangoloj/dnsdumpster)
* [Python3-nmap](https://github.com/wangoloj/python3-nmap)
* [Spyse subdomain finder](https://github.com/wangoloj/spyse-subdomain-finder)
* [8 Online subdomain finder tool](https://www.nmmapper.com/sys/tools/subdomainfinder/) 

