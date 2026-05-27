"""
Scan LOOBins repo for macOS tool techniques and examples.
Maps tactic names to our techniques enum.
"""
import json
import yaml
from pathlib import Path

REPO_DIR = Path("Database/LOOBins/LOOBins")
OUTPUT_PATH = Path("data/enrichment/loobins-matches.json")

# Map LOOBins tactics → our techniques enum
TACTIC_MAP = {
    "Collection": "collection",
    "Command and Control": "command-and-control",
    "Credential Access": "credential-access",
    "Defense Evasion": "defense-evasion",
    "Discovery": "discovery",
    "Execution": "execution",
    "Exfiltration": "exfiltration",
    "Lateral Movement": "lateral-movement",
    "Persistence": "persistence",
    "Privilege Escalation": "privilege-escalation",
}


def scan():
    results = {}

    if not REPO_DIR.is_dir():
        print(f"LOOBins dir not found: {REPO_DIR}")
        return results

    for yf in sorted(REPO_DIR.glob("*.yml")):
        with open(yf) as f:
            data = yaml.safe_load(f)
        if not data:
            continue

        bname = data.get("name", "").lower()
        if not bname:
            continue

        # Collect techniques from all use cases
        techniques = set()
        examples = []
        use_cases = data.get("example_use_cases", []) or []
        for uc in use_cases:
            for t in (uc.get("tactics", []) or []):
                mapped = TACTIC_MAP.get(t)
                if mapped:
                    techniques.add(mapped)
            code = uc.get("code", "")
            desc = uc.get("description", "")
            if code and desc:
                examples.append({"description": desc, "command": code})

        results[bname] = {
            "techniques": sorted(techniques),
            "examples": examples[:5],
            "contributor": data.get("author", ""),
        }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"LOOBins: scanned {len(results)} binaries")
    for name, data in sorted(results.items()):
        if data["techniques"]:
            print(f"  {name:<20} techniques={data['techniques']}")
    return results


if __name__ == "__main__":
    scan()
