import json

def analyze_usgs_commodities():
    # Read the USGS commodities file
    with open('/Users/johnny/Code/GRIP/grip-backend/data/usgs/usgs_mineral_commodities.json', 'r') as f:
        commodities = json.load(f)
    
    print(f"Total USGS commodities: {len(commodities)}")
    
    # Extract key commodities we're interested in
    key_commodities = []
    precious_metals = []
    base_metals = []
    
    for commodity in commodities:
        name = commodity['name'].lower()
        # Look for metals
        if any(metal in name for metal in ['gold', 'silver', 'platinum', 'palladium']):
            precious_metals.append(commodity)
        elif any(metal in name for metal in ['copper', 'aluminum', 'nickel', 'zinc', 'lead', 'tin']):
            base_metals.append(commodity)
        elif any(metal in name for metal in ['iron', 'lithium', 'cobalt', 'uranium', 'titanium']):
            key_commodities.append(commodity)
    
    print(f"\nPrecious Metals ({len(precious_metals)}):")
    for metal in precious_metals:
        print(f"  - {metal['name']}")
    
    print(f"\nBase Metals ({len(base_metals)}):")
    for metal in base_metals:
        print(f"  - {metal['name']}")
    
    print(f"\nOther Key Commodities ({len(key_commodities)}):")
    for commodity in key_commodities[:20]:  # Show first 20
        print(f"  - {commodity['name']}")

if __name__ == "__main__":
    analyze_usgs_commodities()