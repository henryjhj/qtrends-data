import requests, re

proxies = {'http': 'http://127.0.0.1:18080', 'https': 'http://127.0.0.1:18080'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

r = requests.get('https://www.ms.now/', proxies=proxies, headers=headers, timeout=25)
print('Status:', r.status_code)
print('Final URL:', r.url)
print('Content-Length:', len(r.text))

# title
m = re.search(r'<title[^>]*>(.*?)</title>', r.text, re.S)
print('Title:', m.group(1).strip() if m else 'N/A')

# meta description
m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', r.text, re.S | re.I)
print('Meta desc:', m.group(1).strip()[:200] if m else 'N/A')

# extract <h1>, <h2>, <h3> text
for tag in ['h1', 'h2', 'h3']:
    items = re.findall(r'<' + tag + r'[^>]*>(.*?)</' + tag + r'>', r.text, re.S)
    items = [re.sub(r'<[^>]+>', '', x).strip() for x in items]
    items = [x for x in items if x]
    print(f'\n{tag} count: {len(items)}')
    for x in items[:10]:
        print(' ', x[:120])

# count <a> with href
links = re.findall(r'<a[^>]+href=["\'](https?://[^"\']+)["\']', r.text)
print('\nTotal links:', len(links))
print('Sample links:')
for u in links[:15]:
    print(' ', u)

# article-like links (contain ms.now)
ms_links = [u for u in links if 'ms.now' in u]
print(f'\nms.now links: {len(ms_links)}')
for u in ms_links[:15]:
    print(' ', u)
