from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

base = 'https://www.mltframework.org/plugins/PluginsFilters/'
template = '''
def {funcname}(self, {funcparams}):
    self.fx('{realname}', {args})
    return self
'''

def get_links():
    links = BeautifulSoup(requests.get(base).text, "html.parser").select('li a')
    urls = [urljoin(base, l.get('href')) for l in links]
    return urls

def get_page(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    realname = soup.select('h3')[0].string.split('Filter: ')[-1].strip()
    functionname = realname.split('.')[-1].strip()
    params = [h.text.strip() for h in soup.select('h3')[1:]]
    paragraphs = [p.text.strip() for p in soup.select('p')]
    meta = paragraphs[0]
    param_descripts = paragraphs[1:]
    for a, b in zip(params, param_descripts):
        print(a, b)
        # b = b.split('\n')
        # param_d = b[1]
    # print(template.format(funcname=functionname, realname=realname, funcparams='', args=''))
    print(realname, functionname)

# urls = get_links()[0]
# for url in urls:
#     get_page(url)

get_page('https://www.mltframework.org/plugins/FilterDynamic_loudness/')
