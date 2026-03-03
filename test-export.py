import json, urllib.request

# Fetch live memories
req = urllib.request.Request('https://clude.io/api/brain?hours=720&limit=20')
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())

nodes = data.get('nodes', data) if isinstance(data, dict) else data

pack = {
    'id': 'test-export-001',
    'name': 'Clude Full Memory Export',
    'description': 'Test export of 20 live Clude memories',
    'memories': [],
    'entities': [],
    'links': [],
    'created_at': '2026-02-28T01:47:00Z',
    'created_by': 'test',
    'memory_count': 0,
    'entity_count': 0
}

for n in nodes[:20]:
    mem = {
        'id': n.get('id'),
        'hash_id': str(n.get('id', '')),
        'memory_type': n.get('type', 'episodic'),
        'content': n.get('summary', ''),
        'summary': n.get('summary', ''),
        'tags': n.get('tags', []),
        'concepts': [],
        'emotional_valence': n.get('valence', 0),
        'importance': n.get('importance', 0.5),
        'access_count': n.get('accessCount', 0),
        'source': n.get('source', ''),
        'source_id': None,
        'related_user': None,
        'related_wallet': None,
        'metadata': {},
        'created_at': n.get('createdAt', ''),
        'last_accessed': n.get('lastAccessed', ''),
        'decay_factor': n.get('decay', 1),
        'evidence_ids': n.get('evidenceIds', []),
        'solana_signature': n.get('solanaSignature'),
        'compacted': False,
        'compacted_into': None
    }
    pack['memories'].append(mem)

pack['memory_count'] = len(pack['memories'])

# Save JSON
with open('/data/workspace/clude-dashboard/test-export.clude-pack.json', 'w') as f:
    json.dump(pack, f, indent=2)
print(f"JSON: Exported {pack['memory_count']} memories")

# Save Markdown
type_emoji = {'episodic': '📝', 'semantic': '🧠', 'procedural': '⚙️', 'self_model': '🪞'}
lines = [
    f"# {pack['name']}\n",
    f"> {pack['description']}\n",
    f"**Memories:** {pack['memory_count']} | **Exported:** {pack['created_at'][:10]}\n",
    "---\n",
]

for m in pack['memories']:
    emoji = type_emoji.get(m['memory_type'], '📝')
    summary = m['summary'][:120]
    lines.append(f"### {emoji} {summary}\n")
    lines.append(f"**Type:** {m['memory_type']} | **Importance:** {m['importance']} | **Decay:** {m['decay_factor']} | **Created:** {m['created_at'][:10]}")
    tags = ', '.join(m['tags'])
    if tags:
        lines.append(f"**Tags:** {tags}")
    sig = m.get('solana_signature')
    if sig:
        lines.append(f"**On-chain:** [{sig[:16]}...](https://solscan.io/tx/{sig})")
    lines.append("")

with open('/data/workspace/clude-dashboard/test-export.clude-pack.md', 'w') as f:
    f.write('\n'.join(lines))
print(f"Markdown: Exported {pack['memory_count']} memories")

# Verify round-trip: load JSON back
with open('/data/workspace/clude-dashboard/test-export.clude-pack.json') as f:
    reimported = json.load(f)
print(f"Round-trip: {reimported['memory_count']} memories, {len(reimported['memories'])} in array")
print(f"First memory: {reimported['memories'][0]['summary'][:80]}...")
print(f"Has Solana sig: {bool(reimported['memories'][0].get('solana_signature'))}")
