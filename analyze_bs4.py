import requests
from bs4 import BeautifulSoup
from html import unescape

proxies = {'http': 'http://127.0.0.1:18080', 'https': 'http://127.0.0.1:18080'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch(url):
    r = requests.get(url, proxies=proxies, headers=headers, timeout=20, allow_redirects=True)
    return r.text

def analyze(name, url):
    print(f'\n{"="*70}\n{name}: {url}')
    html = fetch(url)
    soup = BeautifulSoup(html, 'lxml')

    # 统计各种标题标签的class
    for tag in ['h1', 'h2', 'h3', 'h4']:
        items = soup.find_all(tag)
        if items:
            print(f'\n  <{tag}> count={len(items)}')
            for it in items[:12]:
                cls = it.get('class', [])
                text = it.get_text(strip=True)
                a = it.find('a')
                href = a.get('href') if a else ''
                if text and len(text) > 10:
                    print(f'    class={cls}')
                    print(f'      text: {text[:110]}')
                    print(f'      href: {href[:90]}')

sites = [
    ('Cricbuzz', 'https://www.cricbuzz.com/'),
    ('The Star MY Sport', 'https://www.thestar.com.my/sport'),
    ('New Straits Times Sport', 'https://www.nst.com.my/sports'),
    ('Goal.com', 'https://www.goal.com/en'),
    ('FourFourTwo', 'https://www.fourfourtwo.com/'),
    ('World Athletics', 'https://worldathletics.org/news'),
    ('BWF News', 'https://bwfbadminton.com/news/'),
    ('FIVB News', 'https://en.volleyballworld.com/news/'),
    ('Sports Illustrated', 'https://www.si.com/'),
    ('NBC Sports', 'https://www.nbcsports.com/'),
    ('CBS Sports', 'https://www.cbssports.com/'),
    ('NBA.com', 'https://www.nba.com/news'),
    ('World Rugby', 'https://www.world.rugby/news'),
    ('Marca EN', 'https://www.marca.com/en/'),
    ('Vavel', 'https://www.vavel.com/'),
    ('Deadspin', 'https://deadspin.com/'),
]

for name, url in sites:
    try:
        analyze(name, url)
    except Exception as e:
        print(f'  ERROR: {e}')
