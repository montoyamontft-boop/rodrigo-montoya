import requests, re, os, json, hashlib, sys
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
BASE='https://www.kipling.edu.mx/'
out=sys.argv[1]
seen={}; queue=[(BASE,0)]
S=requests.Session(); S.headers['User-Agent']='Mozilla/5.0'
def norm(u):
    u=u.split('#')[0]
    return u.replace('http://www.kipling.edu.mx','https://www.kipling.edu.mx').replace('https://kipling.edu.mx','https://www.kipling.edu.mx')
while queue and len(seen)<120:
    u,d=queue.pop(0)
    if u in seen: continue
    try:
        r=S.get(u,timeout=30)
    except Exception as e:
        seen[u]={'err':str(e)}; continue
    ct=r.headers.get('content-type','')
    if 'html' not in ct:
        seen[u]={'status':r.status_code,'ct':ct}; continue
    fn=hashlib.md5(u.encode()).hexdigest()[:10]+'.html'
    open(os.path.join(out,fn),'w').write(r.text)
    s=BeautifulSoup(r.text,'lxml'); t=s.title.string.strip() if s.title and s.title.string else ''
    seen[u]={'status':r.status_code,'file':fn,'title':t,'final':r.url}
    if d>=2: continue
    main=s.find(id='content_main') or s
    links=[a.get('href') for a in (s.find(id='sitenav_main') or s).find_all('a')] if d==0 else []
    links+=[a.get('href') for a in main.find_all('a')]
    links+=[a.get('href') for a in (s.find('footer') or s).find_all('a')]
    for h in links:
        if not h or h.startswith(('javascript','tel:','mailto:','/cdn-cgi')): continue
        v=norm(urljoin(u,h))
        if urlparse(v).netloc=='www.kipling.edu.mx' and v not in seen and not re.search(r'\.(pdf|jpg|png|jpeg|docx?)$',v,re.I):
            queue.append((v,d+1))
json.dump(seen,open(os.path.join(out,'index.json'),'w'),indent=1,ensure_ascii=False)
for k,v in seen.items(): print(v.get('status'),v.get('title'),k)
