import requests, re
from bs4 import BeautifulSoup

proxies = {'http': 'http://127.0.0.1:18080', 'https': 'http://127.0.0.1:18080'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch(url):
    r = requests.get(url, proxies=proxies, headers=headers, timeout=20, allow_redirects=True)
    return r.text

def dump_all(name, url):
    """列出所有 a 标签，看文章分布"""
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
        # 排除导航、广告
        if any(skip in href for skip in ['login','subscribe','privacy','cookie','#','javascript','mailto']):
            continue
        if any(skip in text for skip in ['Sign In','Subscribe','Cookie','Privacy','Terms','Menu','Search','More']):
            continue
        key = text[:40]
        if key in seen:
            continue
        seen.add(key)
        if count < 15:
            parent = a.find_parent(['h1','h2','h3','h4','div','span','p','li','article'])
            pcls = parent.get('class', []) if parent else []
            ptag = parent.name if parent else ''
            print(f'  [{count+1}] {text[:110]}')
            print(f'      href: {href[:95]}')
            print(f'      parent: <{ptag}> class={pcls}')
            count += 1
    if count == 0:
        print('  (none)')

dump_all('NST Sport', 'https://www.nst.com.my/sports')
dump_all('BWF News', 'https://bwfbadminton.com/news/')
dump_all('World Rugby', 'https://www.world.rugby/news')
dump_all('FourFourTwo', 'https://www.fourfourtwo.com/')
dump_all('The Star MY Sport', 'https://www.thestar.com.my/sport')
dump_all('NST Asian Games', 'https://www.nst.com.my/asiangames2026')
