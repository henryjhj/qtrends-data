import requests, re
from bs4 import BeautifulSoup

proxies = {'http': 'http://127.0.0.1:18080', 'https': 'http://127.0.0.1:18080'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch(url):
    r = requests.get(url, proxies=proxies, headers=headers, timeout=20, allow_redirects=True)
    return r.text

def analyze(name, url):
    print(f'\n{"="*70}\n{name}: {url}')
    html = fetch(url)
    soup = BeautifulSoup(html, 'lxml')
    seen = set()
    count = 0
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if not text or len(text) < 18 or len(text) > 200:
            continue
        if any(skip in href for skip in ['#','javascript','mailto','login','subscribe','privacy','cookie']):
            continue
        if any(skip in text for skip in ['Sign In','Subscribe','Cookie','Privacy','Terms','Menu','Search','More','Home','Advertisement']):
            continue
        key = text[:40]
        if key in seen:
            continue
        seen.add(key)
        if count < 10:
            parent = a.find_parent(['h1','h2','h3','h4','div','span','p','li','article'])
            pcls = parent.get('class', []) if parent else []
            ptag = parent.name if parent else ''
            print(f'  [{count+1}] {text[:110]}')
            print(f'      href: {href[:95]}')
            print(f'      parent: <{ptag}> class={pcls}')
            count += 1
    if count == 0:
        print('  (no links)')

analyze('Yonhap News Sport', 'https://en.yna.co.kr/sports/index')
analyze('Arirang Sport', 'https://www.arirang.com/news/list?cd=1015')
analyze('Daily PK Sport', 'https://dailypakistan.com.pk/sports')
analyze('The Nation PK Sport', 'https://www.nation.com.pk/sports')
analyze('Millennium Post Sport', 'https://www.millenniumpost.in/sports')
analyze('The Korea Herald Sport', 'https://www.koreaherald.com/sports/')
analyze('The Korea Times Sport', 'https://www.koreatimes.co.kr/www/sports/')
