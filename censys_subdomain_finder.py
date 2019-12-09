import requests
import censysparser
from useragents import UserAgents
import argparse
try:
    import simplejson as json
except ImportError:
    import json
    
class SearchNonApiCensys(object):

    def __init__(self, domain, limit):
        self.domain = self.cleanDomain(domain)
        self.urlhost = ""
        self.urlcert = ""
        self.page = ""
        self.resultshosts = ""
        self.resultcerts = ""
        self.total_resultshosts = ""
        self.total_resultscerts = ""
        self.server = 'censys.io'
        self.ips = []
        self.hostnamesall = []
        self.limit = limit
        
        self.ua = UserAgents()
    
    def cleanDomain(self, domain):
        """
        @remove wwww.
        """
        # TODO: this is primitive way of getting rid of the protocol
        #       needs a more advanced way.
        
        if("www." in domain):
            domain = domain.split(".")
            if(len(domain) > 2):
                domain.pop(0)
                return '.'.join(domain)
        return domain 
        
    def do_searchhosturl(self):
        try:
            headers = {'user-agent': self.ua.get_user_agent(), 'Accept': '*/*', 'Referer': self.urlhost}
            responsehost = requests.get(self.urlhost, headers=headers)
            self.resultshosts = responsehost.text
            self.total_resultshosts += self.resultshosts
        except Exception as e:
            print(f'Error occurred in the Censys module downloading pages from Censys - IP search: + {e}')

    def do_searchcertificateurl(self):
        try:
            headers = {'user-agent': self.ua.get_user_agent(), 'Accept': '*/*', 'Referer': self.urlcert}
            responsecert = requests.get(self.urlcert, headers=headers)
            self.resultcerts = responsecert.text
            self.total_resultscerts += self.resultcerts
        except Exception as e:
            print(f'Error occurred in the Censys module downloading pages from Censys - certificates search: {e}')

    def process(self):
        try:
            self.urlhost = 'https://' + self.server + '/ipv4/_search?q=' + str(self.domain) + '&page=1'
            self.urlcert = 'https://' + self.server + '/certificates/_search?q=' + str(self.domain) + '&page=1'
            self.do_searchhosturl()
            self.do_searchcertificateurl()
            
            counter = 2
            pages = censysparser.Parser(self)
            totalpages = pages.search_totalpageshosts()
            pagestosearch = int(self.limit / 25)  # 25 results/page
            
            if totalpages is None:
                totalpages = 0
            if totalpages <= pagestosearch:
                while counter <= totalpages:
                    try:
                        self.page = str(counter)
                        self.urlhost = 'https://' + self.server + '/ipv4/_search?q=' + str(self.domain) + '&page=' + str(
                            self.page)
                        print('\tSearching IP results page [{0}]'.format(self.page))
                        self.do_searchhosturl()
                        counter += 1
                    except Exception as e:
                        print(f'Error occurred in the Censys module requesting the pages: {e}')
            else:
                while counter <= pagestosearch:
                    try:
                        self.page = str(counter)
                        self.urlhost = 'https://' + self.server + '/ipv4/_search?q=' + str(self.domain) + '&page=' + str(
                            self.page)
                        print(f'\tSearching results page {self.page}.')
                        self.do_searchhosturl()
                        counter += 1
                    except Exception as e:
                        print(f'Error occurred in the Censys module requesting the pages: {e}')
                        
            counter = 2
            totalpages = pages.search_totalpagescerts()
            if totalpages is None:
                totalpages = 0
                
            if totalpages <= pagestosearch:
                while counter <= totalpages:
                    try:
                        self.page = str(counter)
                        self.urlhost = 'https://' + self.server + '/certificates/_search?q=' + str(
                            self.domain) + '&page=' + str(self.page)
                        print(f'\tSearching certificates results page {self.page}.')
                        self.do_searchcertificateurl()
                        counter += 1
                    except Exception as e:
                        print(f'Error occurred in the Censys module requesting the pages: {e}')
            else:
                while counter <= pagestosearch:
                    try:
                        self.page = str(counter)
                        self.urlhost = 'https://' + self.server + '/ipv4/_search?q=' + str(self.domain) + '&page=' + str(
                            self.page)
                        print('\tSearching IP results page ' + self.page + '.')
                        self.do_searchhosturl()
                        counter += 1
                    except Exception as e:
                        print(f'Error occurred in the Censys module requesting the pages: {e}')
            
            # Space in terminal display
            print("\n")
            
        except Exception as e:
            print(f'Error occurred in the main Censys module: {e}')

    def get_subdomains(self):
        try:
            ips = self.get_ipaddresses()
            headers = {'user-agent': self.ua.get_user_agent(), 'Accept': '*/*', 'Referer': self.urlcert}
            response = requests.post('https://censys.io/ipv4/getdns', json={'ips': ips}, headers=headers)
            responsejson = response.json()
            domainsfromcensys = []
            for key, jdata in responsejson.items():
                if jdata is not None:
                    domainsfromcensys.append(jdata)
                else:
                    pass
                    
            matchingdomains = [s for s in domainsfromcensys if str(self.domain) in s]
            self.hostnamesall.extend(matchingdomains)
            hostnamesfromcerts = censysparser.Parser(self)
            self.hostnamesall.extend(hostnamesfromcerts.search_hostnamesfromcerts())

            return list(set(self.hostnamesall)) # Filters unique values
            
        except Exception as e:
            print(f'Error occurred in the Censys module - hostname search: {e}')
    
    def get_ipaddresses(self):
        try:
            ips = censysparser.Parser(self)
            self.ips = ips.search_ipaddresses()
            return self.ips
        except Exception as e:
            print(f'Error occurred in the main Censys module - IP address search: {e}')
            
if __name__=="__main__":
    parser = argparse.ArgumentParser(prog="None censys subdomain finder")
    parser.add_argument('-d', '--d', help='Help', required=True)
    parser.add_argument('-l', '--l', help='Limit', type=int, required=False, default=500)
    args = parser.parse_args()
    
    cen  = SearchNonApiCensys(args.d, args.l)
    cen.process()
    subdomains = cen.get_subdomains()
    print(subdomains)
