import requests, re
from html import unescape

proxies = {'http': 'http://127.0.0.1:18080', 'https': 'http://127.0.0.1:18080'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch(url):
    r = requests.get(url, proxies=proxies, headers=headers, timeout=20, allow_redirects=True)
    return r.text

def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = unescape(s)
    return s.strip()

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
    ('Sport EN', 'https://en.as.com/'),
    ('Sportal', 'https://sportal.bg/'),
    ('Vavel', 'https://www.vavel.com/'),
    ('Deadspin', 'https://deadspin.com/'),
]

for name, url in sites:
    print(f'\n{"="*70}\n{name}: {url}')
    try:
        html = fetch(url)
        # 找带 href 的 a 标签及其标题文本
        # 找出常见的文章链接模式
        links = re.findall(r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.S)
        seen = set()
        count = 0
        for href, inner in links:
            title = clean(inner)
            if not title or len(title) < 15 or len(title) > 200:
                continue
            if href.startswith('#') or href.startswith('javascript'):
                continue
            key = (href, title[:60])
            if key in seen:
                continue
            seen.add(key)
            if count < 8:
                print(f'  [{count+1}] {title[:100]}')
                print(f'      -> {href[:90]}')
                count += 1
        if count == 0:
            print('  (no article links found)')
    except Exception as e:
        print(f'  ERROR: {e}')
