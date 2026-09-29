import json

with open('/workspace/hashtags.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def fix_order(entry):
    """Ensure correct field order: tag_id, tag, tag_cn, first_seen, last_seen, synonyms, desc, desc_cn"""
    return {
        "tag_id": entry["tag_id"],
        "tag": entry["tag"],
        "tag_cn": entry["tag_cn"],
        "first_seen": entry["first_seen"],
        "last_seen": entry["last_seen"],
        "synonyms": entry["synonyms"],
        "desc": entry["desc"],
        "desc_cn": entry["desc_cn"],
    }

# Fix field order for entries with wrong order
for i, entry in enumerate(data):
    keys = list(entry.keys())
    if keys.index('tag_cn') < keys.index('tag'):
        data[i] = fix_order(entry)
        print(f"Fixed order for tag_id {entry['tag_id']}")

# Update entry 50: US Canada Trade War
for entry in data:
    if entry['tag_id'] == 50:
        entry['last_seen'] = '2026-09-30'
        old_desc = entry['desc']
        old_desc_cn = entry['desc_cn']
        entry['desc'] = '2026 US-Canada trade war escalation. After the US imposed 50% tariffs on $20B of Canadian goods and talks collapsed on Aug 21, Canada retaliated on Sept 8. On Sept 29 the US implemented an import ban on ~$967M of Canadian alcohol, dairy and motorcycles.'
        entry['desc_cn'] = '2026年美加贸易战升级。8月21日谈判破裂后，加拿大9月8日对200亿美元美国商品加征最高50%反制关税；9月29日美国对约9.67亿美元加拿大酒类、乳制品和摩托车实施进口禁令。'
        print(f"Updated entry 50: desc {len(old_desc)} -> {len(entry['desc'])}, desc_cn {len(old_desc_cn)} -> {len(entry['desc_cn'])}")

# Update entry 4: US Iran War
for entry in data:
    if entry['tag_id'] == 4:
        entry['last_seen'] = '2026-09-30'
        old_desc = entry['desc']
        old_desc_cn = entry['desc_cn']
        entry['desc'] = 'The 2026 Iran War began Feb 28 when the U.S. and Israel struck Iran; Iran retaliated across the Middle East. In late Sept, Iran captured a U.S. underwater drone and proposed reopening Hormuz, but Trump rejected it. By Sept 30 the sides exchanged messages via mediators while keeping military options open.'
        entry['desc_cn'] = '2026年2月28日美以对伊朗发动大规模打击，伊朗反击使冲突扩大至中东。9月下旬伊朗捕获美国无人潜航器并提出重开霍尔木兹海峡方案，特朗普拒绝。9月30日双方通过调解方交换信息，但均保留军事选项。'
        print(f"Updated entry 4: desc {len(old_desc)} -> {len(entry['desc'])}, desc_cn {len(old_desc_cn)} -> {len(entry['desc_cn'])}")

# Update entry 45: 2026 Asian Games
for entry in data:
    if entry['tag_id'] == 45:
        entry['last_seen'] = '2026-09-30'
        print("Updated entry 45 last_seen")

# Update entry 53: Houthi Yemen Offensive
for entry in data:
    if entry['tag_id'] == 53:
        entry['last_seen'] = '2026-09-30'
        old_desc = entry['desc']
        old_desc_cn = entry['desc_cn']
        entry['desc'] = "In Sept 2026, Yemen's Houthi movement captured Red Sea port Mocha and Perim Island, controlling Yemen's entire Red Sea coast. Houthis fired missiles/drones at Saudi capital Riyadh and Yanbu energy hub Sept 19-20 (first direct strike on Riyadh) and again Sept 24. France's Macron announced troops, radars, defense systems to protect Yanbu oil facilities; Brent crude topped $100/bbl. Saudi launched retaliatory airstrikes on Sept 29."
        entry['desc_cn'] = '2026年9月也门胡塞武装攻占红海港口摩卡及丕林岛，控制也门红海沿岸。胡塞9月19-20日及24日多次袭击沙特利雅得、延布阿美设施和吉赞军事目标，系首次袭击沙特首都。法国马克龙宣布派兵保护延布石油设施；布伦特原油破百美元。9月29日沙特发动报复性空袭反击。'
        print(f"Updated entry 53: desc {len(old_desc)} -> {len(entry['desc'])}, desc_cn {len(old_desc_cn)} -> {len(entry['desc_cn'])}")

# Add new entry 84: OpenAI Safety Pause
new_entry = {
    "tag_id": 84,
    "tag": "OpenAI Safety Pause",
    "tag_cn": "OpenAI安全暂停",
    "first_seen": "2026-09-30",
    "last_seen": "2026-09-30",
    "synonyms": [
        "OpenAI暂停发布模型",
        "OpenAI model halt",
        "OpenAI safety halt",
        "OpenAI暂停新模型"
    ],
    "desc": "OpenAI announced on September 30, 2026, that it would pause the release of new AI models due to unresolved safety concerns, sparking global debate over AI development guardrails and corporate responsibility.",
    "desc_cn": "OpenAI于2026年9月30日宣布因安全问题暂停发布新AI模型，引发全球对AI发展安全护栏与企业责任的广泛讨论。"
}
data.append(new_entry)
print(f"Added new entry 84: tag='{new_entry['tag']}', desc={len(new_entry['desc'])}, desc_cn={len(new_entry['desc_cn'])}")

# Sort by tag_id to maintain order
data.sort(key=lambda x: x['tag_id'])

with open('/workspace/hashtags.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done. Max tag_id:", max(e['tag_id'] for e in data))
