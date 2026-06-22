#!/usr/bin/env python3
"""Generate MINIMAL testnet metadata JSON for the Yume Spirits collection.

Locked decision 2026-06-10: testnet exposes ONLY rarity-relevant attributes
(Rarity Tier, Tier Index, Staking Weight) + a placeholder image. Granular
visual traits (Hair, Wings, Eyes...) are withheld until mainnet reveal so the
reused art cannot be trait-sniped. Rarity tier is already public via the
on-chain rarity_map, so this leaks nothing new.

Source of truth: nfts/rarity_map_2222.json (same vector seeded on-chain).
Output: yumebet-assets/json/{id}.json  (1..=2222)
"""
import json, os

HERE = os.path.dirname(__file__)
RARITY = os.path.join(HERE, "rarity_map_2222.json")
OUT = os.path.join(HERE, "json")
PLACEHOLDER = "https://yumebetdev.github.io/yumebet-assets/images/unrevealed.png"

# tier byte -> (display name, 1-based tier index, staking weight label)
TIER = {
    0: ("Common",    1, "10,000 bps (1.0x)"),
    1: ("Rare",      2, "10,500 bps (1.05x)"),
    2: ("Epic",      3, "11,000 bps (1.1x)"),
    3: ("Legendary", 4, "12,000 bps (1.2x)"),
}
DESC = "Yume: A collection of 2222 unique Sakura spirits on the Sui blockchain. Art revealed at mainnet."

tiers = json.load(open(RARITY))
assert len(tiers) == 2222, len(tiers)
os.makedirs(OUT, exist_ok=True)

counts = {0:0,1:0,2:0,3:0}
for idx, t in enumerate(tiers):
    token_id = idx + 1
    name, tier_index, weight = TIER[t]
    counts[t] += 1
    doc = {
        "name": f"Yume Spirits #{token_id}",
        "description": DESC,
        "image": PLACEHOLDER,
        "edition": token_id,
        "attributes": [
            {"trait_type": "Rarity Tier",    "value": name},
            {"trait_type": "Tier Index",     "value": tier_index},
            {"trait_type": "Staking Weight", "value": weight},
        ],
    }
    with open(os.path.join(OUT, f"{token_id}.json"), "w", newline="\n") as f:
        json.dump(doc, f, indent=2)

print(f"wrote {len(tiers)} files to {os.path.normpath(OUT)}")
print("tier counts:", {TIER[k][0]: v for k, v in counts.items()})
