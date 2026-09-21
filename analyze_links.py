import requests, re
from bs4 import BeautifulSoup
from html import unescape

proxies = {'http': 'http://127.0.0.1:18080', 'https': 'http://127.0.0.1:18080'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch(url):
    r = requests.get(url, proxies=proxies, headers=headers, timeout=20, allow_redirects=True)
    return r.text

def show_links(name, url, patterns):
    """显示匹配特定 href 模式的 a 标签及其父结构"""
    print(f'\n{"="*70}\n{name}: {url}')
    html = fetch(url)
    soup = BeautifulSoup(html, 'lxml')

    seen = set()
    count = 0
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not any(p in href for p in patterns):
            continue
        text = a.get_text(strip=True)
        if not text or len(text) < 15 or len(text) > 200:
            continue
        key = text[:60]
        if key in seen:
            continue
        seen.add(key)
        if count < 10:
            # 找父级 h2/h3/h4 或 div 的 class
            parent = a.find_parent(['h1','h2','h3','h4','div','span'])
            pcls = parent.get('class', []) if parent else []
            ptag = parent.name if parent else ''
            print(f'  [{count+1}] {text[:110]}')
            print(f'      href: {href[:90]}')
            print(f'      parent: <{ptag}> class={pcls}')
            count += 1
    if count == 0:
        print('  (no matches)')

# 针对每个站点用其文章 URL 特征来分析
show_links('Cricbuzz', 'https://www.cricbuzz.com/', ['/news/', '/cricket-news/'])
show_links('The Star MY Sport', 'https://www.thestar.com.my/sport', ['/sport/'])
show_links('New Straits Times Sport', 'https://www.nst.com.my/sports', ['/sports/', '/asiangames'])
show_links('Goal.com', 'https://www.goal.com/en', ['/en/news/', '/news/'])
show_links('FourFourTwo', 'https://www.fourfourtwo.com/', ['/news/', '/features/'])
show_links('World Athletics', 'https://worldathletics.org/news', ['/news/', '/competitions/'])
show_links('BWF News', 'https://bwfbadminton.com/news/', ['/news/', 'news-single'])
show_links('FIVB News', 'https://en.volleyballworld.com/news/', ['/news/', '/articles/'])
show_links('Sports Illustrated', 'https://www.si.com/', ['/nba/', '/nfl/', '/soccer/', '/college-', '/tennis/', '/golf/', '/mlb/', '/nhl/'])
show_links('NBC Sports', 'https://www.nbcsports.com/', ['/nfl/', '/nba/', '/soccer/', '/college-', '/mlb/', '/nhl/', '/tennis/', '/golf/', '/f1/'])
show_links('CBS Sports', 'https://www.cbssports.com/', ['/news/', '/articles/'])
show_links('NBA.com', 'https://www.nba.com/news', ['/news/', '/article/'])
show_links('World Rugby', 'https://www.world.rugby/news', ['/news/', '/rugby/'])
show_links('Marca EN', 'https://www.marca.com/en/', ['/en/'])
show_links('Vavel', 'https://www.vavel.com/', ['/news/', '/article/'])
show_links('Deadspin', 'https://deadspin.com/', ['/news/', '/story/'])
