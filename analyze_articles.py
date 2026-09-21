import requests, re
from bs4 import BeautifulSoup

proxies = {'http': 'http://127.0.0.1:18080', 'https': 'http://127.0.0.1:18080'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch(url):
    r = requests.get(url, proxies=proxies, headers=headers, timeout=20, allow_redirects=True)
    return r.text

def dump_article_links(name, url):
    """找所有看起来像文章的链接（含日期段或长slug）"""
    print(f'\n{"="*70}\n{name}: {url}')
    html = fetch(url)
    soup = BeautifulSoup(html, 'lxml')

    seen = set()
    count = 0
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if not text or len(text) < 20 or len(text) > 200:
            continue
        # 文章链接特征：包含年份段 /2026/ 或 /news/ 或 /article/ 或长slug
        if not re.search(r'(/202\d/|/news/|/article/|/stories/|/features/)', href):
            continue
        if href.startswith('#') or href.startswith('javascript'):
            continue
        key = text[:50]
        if key in seen:
            continue
        seen.add(key)
        if count < 12:
            parent = a.find_parent(['h1','h2','h3','h4','div','span','p','li'])
            pcls = parent.get('class', []) if parent else []
            ptag = parent.name if parent else ''
            print(f'  [{count+1}] {text[:110]}')
            print(f'      href: {href[:95]}')
            print(f'      parent: <{ptag}> class={pcls}')
            count += 1
    if count == 0:
        print('  (no article-like links found)')

sites = [
    ('The Star MY Sport', 'https://www.thestar.com.my/sport'),
    ('CBS Sports', 'https://www.cbssports.com/'),
    ('World Rugby', 'https://www.world.rugby/news'),
    ('BWF News', 'https://bwfbadminton.com/news/'),
    ('FourFourTwo', 'https://www.fourfourtwo.com/'),
    ('Vavel', 'https://www.vavel.com/'),
    ('Deadspin', 'https://deadspin.com/'),
    ('NBC Sports', 'https://www.nbcsports.com/'),
    ('New Straits Times Sport', 'https://www.nst.com.my/sports'),
    ('The Nation LK', 'https://nation.lk/online/'),
]

for name, url in sites:
    try:
        dump_article_links(name, url)
    except Exception as e:
        print(f'  ERROR: {e}')
