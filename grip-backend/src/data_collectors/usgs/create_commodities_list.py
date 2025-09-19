#!/usr/bin/env python3
"""
Script to manually extract USGS mineral commodities from the HTML content we already have
"""
import json
import re

def extract_commodities_from_html():
    """Extract commodities directly from the HTML content we retrieved earlier"""
    
    # Based on the HTML content we saw earlier, let's manually extract the commodities
    # This is more reliable than trying to parse the entire page
    
    commodities = [
        # A
        {"name": "Abrasives, Manufactured", "url_name": "manufactured-abrasives", "link": "https://www.usgs.gov/centers/national-minerals-information-center/manufactured-abrasives-statistics-and-information"},
        {"name": "Aggregates", "url_name": "natural-aggregates", "link": "https://www.usgs.gov/centers/national-minerals-information-center/natural-aggregates-statistics-and-information"},
        {"name": "Alumina", "url_name": "bauxite-and-alumina", "link": "https://www.usgs.gov/centers/national-minerals-information-center/bauxite-and-alumina-statistics-and-information"},
        {"name": "Aluminum", "url_name": "aluminum", "link": "https://www.usgs.gov/centers/national-minerals-information-center/aluminum-statistics-and-information"},
        {"name": "Aluminum Oxide, Fused (Manufactured Abrasives)", "url_name": "manufactured-abrasives", "link": "https://www.usgs.gov/centers/national-minerals-information-center/manufactured-abrasives-statistics-and-information"},
        {"name": "Antimony", "url_name": "antimony", "link": "https://www.usgs.gov/centers/national-minerals-information-center/antimony-statistics-and-information"},
        {"name": "Arsenic", "url_name": "arsenic", "link": "https://www.usgs.gov/centers/national-minerals-information-center/arsenic-statistics-and-information"},
        {"name": "Asbestos", "url_name": "asbestos", "link": "https://www.usgs.gov/centers/national-minerals-information-center/asbestos-statistics-and-information"},
        
        # B
        {"name": "Barite", "url_name": "barite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/barite-statistics-and-information"},
        {"name": "Bauxite", "url_name": "bauxite-and-alumina", "link": "https://www.usgs.gov/centers/nmic/bauxite-and-alumina-statistics-and-information"},
        {"name": "Bentonite (Clay Minerals)", "url_name": "clays", "link": "https://www.usgs.gov/centers/national-minerals-information-center/clays-statistics-and-information"},
        {"name": "Beryllium", "url_name": "beryllium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/beryllium-statistics-and-information"},
        {"name": "Bismuth", "url_name": "bismuth", "link": "https://www.usgs.gov/centers/national-minerals-information-center/bismuth-statistics-and-information"},
        {"name": "Boron", "url_name": "boron", "link": "https://www.usgs.gov/centers/national-minerals-information-center/boron-statistics-and-information"},
        {"name": "Bromine", "url_name": "bromine", "link": "https://www.usgs.gov/centers/national-minerals-information-center/bromine-statistics-and-information"},
        
        # C
        {"name": "Cadmium", "url_name": "cadmium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/cadmium-statistics-and-information"},
        {"name": "Calcium Carbonate (Crushed Stone, Lime)", "url_name": "crushed-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/crushed-stone-statistics-and-information"},
        {"name": "Cement", "url_name": "cement", "link": "https://www.usgs.gov/centers/national-minerals-information-center/cement-statistics-and-information"},
        {"name": "Cesium", "url_name": "cesium-and-rubidium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/cesium-and-rubidium-statistics-and-information"},
        {"name": "Chromium", "url_name": "chromium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/chromium-statistics-and-information"},
        {"name": "Clay Minerals", "url_name": "clays", "link": "https://www.usgs.gov/centers/national-minerals-information-center/clays-statistics-and-information"},
        {"name": "Coal Combustion Products", "url_name": "coal-combustion-products", "link": "https://www.usgs.gov/centers/national-minerals-information-center/coal-combustion-products-statistics-and-information"},
        {"name": "Cobalt", "url_name": "cobalt", "link": "https://www.usgs.gov/centers/national-minerals-information-center/cobalt-statistics-and-information"},
        {"name": "Copper", "url_name": "copper", "link": "https://www.usgs.gov/centers/national-minerals-information-center/copper-statistics-and-information"},
        {"name": "Corundum (Manufactured Abrasives)", "url_name": "manufactured-abrasives", "link": "https://www.usgs.gov/centers/national-minerals-information-center/manufactured-abrasives-statistics-and-information"},
        {"name": "Crushed Stone", "url_name": "crushed-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/crushed-stone-statistics-and-information"},
        
        # D
        {"name": "Diamond, Industrial", "url_name": "industrial-diamond", "link": "https://www.usgs.gov/centers/national-minerals-information-center/industrial-diamond-statistics-and-information"},
        {"name": "Diatomite", "url_name": "diatomite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/diatomite-statistics-and-information"},
        {"name": "Dimension Stone", "url_name": "dimension-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/dimension-stone-statistics-and-information"},
        
        # E
        {"name": "Explosives", "url_name": "explosives", "link": "https://www.usgs.gov/centers/national-minerals-information-center/explosives-statistics-and-information"},
        
        # F
        {"name": "Feldspar", "url_name": "feldspar", "link": "https://www.usgs.gov/centers/national-minerals-information-center/feldspar-statistics-and-information"},
        {"name": "Ferroalloys", "url_name": "ferroalloys", "link": "https://www.usgs.gov/centers/national-minerals-information-center/ferroalloys-statistics-and-information"},
        {"name": "Fluorspar", "url_name": "fluorspar", "link": "https://www.usgs.gov/centers/national-minerals-information-center/fluorspar-statistics-and-information"},
        {"name": "Fuller's Earth (Clay Minerals)", "url_name": "clays", "link": "https://www.usgs.gov/centers/national-minerals-information-center/clays-statistics-and-information"},
        
        # G
        {"name": "Gallium", "url_name": "gallium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/gallium-statistics-and-information"},
        {"name": "Garnet, Industrial", "url_name": "garnet", "link": "https://www.usgs.gov/centers/national-minerals-information-center/garnet-statistics-and-information"},
        {"name": "Gemstones", "url_name": "gemstones", "link": "https://www.usgs.gov/centers/national-minerals-information-center/gemstones-statistics-and-information"},
        {"name": "Germanium", "url_name": "germanium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/germanium-statistics-and-information"},
        {"name": "Gold", "url_name": "gold", "link": "https://www.usgs.gov/centers/national-minerals-information-center/gold-statistics-and-information"},
        {"name": "Granite Crushed Stone", "url_name": "crushed-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/crushed-stone-statistics-and-information"},
        {"name": "Granite Dimension Stone", "url_name": "dimension-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/dimension-stone-statistics-and-information"},
        {"name": "Graphite", "url_name": "graphite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/graphite-statistics-and-information"},
        {"name": "Gypsum", "url_name": "gypsum", "link": "https://www.usgs.gov/centers/national-minerals-information-center/gypsum-statistics-and-information"},
        
        # H
        {"name": "Hafnium", "url_name": "zirconium-and-hafnium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/zirconium-and-hafnium-statistics-and-information"},
        {"name": "Helium", "url_name": "helium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/helium-statistics-and-information"},
        
        # I
        {"name": "Ilmenite (Titanium Mineral Concentrates)", "url_name": "titanium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/titanium-statistics-and-information"},
        {"name": "Indium", "url_name": "indium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/indium-statistics-and-information"},
        {"name": "Iodine", "url_name": "iodine", "link": "https://www.usgs.gov/centers/national-minerals-information-center/iodine-statistics-and-information"},
        {"name": "Iridium (Platinum-Group Metals)", "url_name": "platinum-group-metals", "link": "https://www.usgs.gov/centers/national-minerals-information-center/platinum-group-metals-statistics-and-information"},
        {"name": "Iron Ore", "url_name": "iron-ore", "link": "https://www.usgs.gov/centers/national-minerals-information-center/iron-ore-statistics-and-information"},
        {"name": "Iron and Steel", "url_name": "iron-and-steel", "link": "https://www.usgs.gov/centers/national-minerals-information-center/iron-and-steel-statistics-and-information"},
        {"name": "Iron and Steel Scrap", "url_name": "iron-and-steel-scrap", "link": "https://www.usgs.gov/centers/national-minerals-information-center/iron-and-steel-scrap-statistics-and-information"},
        {"name": "Iron and Steel Slag", "url_name": "iron-and-steel-slag", "link": "https://www.usgs.gov/centers/national-minerals-information-center/iron-and-steel-slag-statistics-and-information"},
        {"name": "Iron Oxide Pigments", "url_name": "iron-oxide-pigments", "link": "https://www.usgs.gov/centers/national-minerals-information-center/iron-oxide-pigments-statistics-and-information"},
        
        # K
        {"name": "Kaolin (Clay Minerals)", "url_name": "clays", "link": "https://www.usgs.gov/centers/national-minerals-information-center/clays-statistics-and-information"},
        {"name": "Kyanite and Related Minerals", "url_name": "kyanite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/kyanite-statistics-and-information"},
        
        # L
        {"name": "Lead", "url_name": "lead", "link": "https://www.usgs.gov/centers/national-minerals-information-center/lead-statistics-and-information"},
        {"name": "Lime", "url_name": "lime", "link": "https://www.usgs.gov/centers/national-minerals-information-center/lime-statistics-and-information"},
        {"name": "Limestone Crushed Stone", "url_name": "crushed-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/crushed-stone-statistics-and-information"},
        {"name": "Limestone Dimension Stone", "url_name": "dimension-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/dimension-stone-statistics-and-information"},
        {"name": "Lithium", "url_name": "lithium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/lithium-statistics-and-information"},
        
        # M
        {"name": "Magnesium", "url_name": "magnesium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/magnesium-statistics-and-information"},
        {"name": "Magnesium Compounds", "url_name": "magnesium-compounds", "link": "https://www.usgs.gov/centers/national-minerals-information-center/magnesium-compounds-statistics-and-information"},
        {"name": "Manganese", "url_name": "manganese", "link": "https://www.usgs.gov/centers/national-minerals-information-center/manganese-statistics-and-information"},
        {"name": "Marble Crushed Stone", "url_name": "crushed-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/crushed-stone-statistics-and-information"},
        {"name": "Marble Dimension Stone", "url_name": "dimension-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/dimension-stone-statistics-and-information"},
        {"name": "Mercury", "url_name": "mercury", "link": "https://www.usgs.gov/centers/national-minerals-information-center/mercury-statistics-and-information"},
        {"name": "Mica", "url_name": "mica", "link": "https://www.usgs.gov/centers/national-minerals-information-center/mica-statistics-and-information"},
        {"name": "Mining and Quarrying", "url_name": "mining-and-quarrying", "link": "https://www.usgs.gov/centers/national-minerals-information-center/mining-and-quarrying"},
        {"name": "Molybdenum", "url_name": "molybdenum", "link": "https://www.usgs.gov/centers/national-minerals-information-center/molybdenum-statistics-and-information"},
        {"name": "Mullite, Synthetic (Kyanite)", "url_name": "kyanite-and-related-minerals", "link": "https://www.usgs.gov/centers/national-minerals-information-center/kyanite-and-related-minerals-statistics-and-information"},
        
        # N
        {"name": "Nepheline Syenite (Feldspar)", "url_name": "feldspar", "link": "https://www.usgs.gov/centers/national-minerals-information-center/feldspar-statistics-and-information"},
        {"name": "Nickel", "url_name": "nickel", "link": "https://www.usgs.gov/centers/national-minerals-information-center/nickel-statistics-and-information"},
        {"name": "Niobium", "url_name": "niobium-and-tantalum", "link": "https://www.usgs.gov/centers/national-minerals-information-center/niobium-and-tantalum-statistics-and-information"},
        {"name": "Nitrogen", "url_name": "nitrogen", "link": "https://www.usgs.gov/centers/national-minerals-information-center/nitrogen-statistics-and-information"},
        
        # O
        {"name": "Osmium (Platinum-Group Metals)", "url_name": "platinum-group-metals", "link": "https://www.usgs.gov/centers/national-minerals-information-center/platinum-group-metals-statistics-and-information"},
        
        # P
        {"name": "Palladium (Platinum-Group Metals)", "url_name": "platinum-group-metals", "link": "https://www.usgs.gov/centers/national-minerals-information-center/platinum-group-metals-statistics-and-information"},
        {"name": "Peat", "url_name": "peat", "link": "https://www.usgs.gov/centers/national-minerals-information-center/peat-statistics-and-information"},
        {"name": "Perlite", "url_name": "perlite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/perlite-statistics-and-information"},
        {"name": "Phosphate Rock", "url_name": "phosphate-rock", "link": "https://www.usgs.gov/centers/national-minerals-information-center/phosphate-rock-statistics-and-information"},
        {"name": "Platinum-Group Metals", "url_name": "platinum-group-metals", "link": "https://www.usgs.gov/centers/national-minerals-information-center/platinum-group-metals-statistics-and-information"},
        {"name": "Potash", "url_name": "potash", "link": "https://www.usgs.gov/centers/national-minerals-information-center/potash-statistics-and-information"},
        {"name": "Pumice and Pumicite", "url_name": "pumice-and-pumicite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/pumice-and-pumicite-statistics-and-information"},
        {"name": "Pyrophyllite (Talc)", "url_name": "talc-and-pyrophyllite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/talc-and-pyrophyllite-statistics-and-information"},
        
        # Q
        {"name": "Quartz Crystal (Silica)", "url_name": "silica", "link": "https://www.usgs.gov/centers/national-minerals-information-center/silica-statistics-and-information"},
        
        # R
        {"name": "Rare Earths", "url_name": "rare-earths", "link": "https://www.usgs.gov/centers/national-minerals-information-center/rare-earths-statistics-and-information"},
        {"name": "Recycling", "url_name": "recycling", "link": "https://www.usgs.gov/centers/national-minerals-information-center/recycling-statistics-and-information"},
        {"name": "Rhenium", "url_name": "rhenium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/rhenium-statistics-and-information"},
        {"name": "Rhodium (Platinum-Group Metals)", "url_name": "platinum-group-metals", "link": "https://www.usgs.gov/centers/national-minerals-information-center/platinum-group-metals-statistics-and-information"},
        {"name": "Rubidium (Cesium)", "url_name": "cesium-and-rubidium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/cesium-and-rubidium-statistics-and-information"},
        {"name": "Ruthenium (Platinum-Group Metals)", "url_name": "platinum-group-metals", "link": "https://www.usgs.gov/centers/national-minerals-information-center/platinum-group-metals-statistics-and-information"},
        {"name": "Rutile (Titanium Mineral Concentrates)", "url_name": "titanium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/titanium-statistics-and-information"},
        
        # S
        {"name": "Salt", "url_name": "salt", "link": "https://www.usgs.gov/centers/national-minerals-information-center/salt-statistics-and-information"},
        {"name": "Sand and Gravel, Construction", "url_name": "construction-sand-and-gravel", "link": "https://www.usgs.gov/centers/national-minerals-information-center/construction-sand-and-gravel-statistics-and"},
        {"name": "Sand and Gravel, Industrial (Silica)", "url_name": "silica", "link": "https://www.usgs.gov/centers/national-minerals-information-center/silica-statistics-and-information"},
        {"name": "Sandstone Crushed Stone", "url_name": "crushed-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/crushed-stone-statistics-and-information"},
        {"name": "Sandstone Dimension Stone", "url_name": "dimension-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/dimension-stone-statistics-and-information"},
        {"name": "Scandium (Rare Earths)", "url_name": "rare-earths", "link": "https://www.usgs.gov/centers/national-minerals-information-center/rare-earths-statistics-and-information"},
        {"name": "Selenium", "url_name": "selenium-and-tellurium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/selenium-and-tellurium-statistics-and-information"},
        {"name": "Shell (Gemstones)", "url_name": "gemstones", "link": "https://www.usgs.gov/centers/national-minerals-information-center/gemstones-statistics-and-information"},
        {"name": "Silica", "url_name": "silica", "link": "https://www.usgs.gov/centers/national-minerals-information-center/silica-statistics-and-information"},
        {"name": "Silicon", "url_name": "silicon", "link": "https://www.usgs.gov/centers/national-minerals-information-center/silicon-statistics-and-information"},
        {"name": "Silicon Carbide (Manufactured Abrasives)", "url_name": "manufactured-abrasives", "link": "https://www.usgs.gov/centers/national-minerals-information-center/manufactured-abrasives-statistics-and-information"},
        {"name": "Silver", "url_name": "silver", "link": "https://www.usgs.gov/centers/national-minerals-information-center/silver-statistics-and-information"},
        {"name": "Slate Crushed Stone", "url_name": "crushed-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/crushed-stone-statistics-and-information"},
        {"name": "Slate Dimension Stone", "url_name": "dimension-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/dimension-stone-statistics-and-information"},
        {"name": "Soda Ash", "url_name": "soda-ash", "link": "https://www.usgs.gov/centers/national-minerals-information-center/soda-ash-statistics-and-information"},
        {"name": "Sodium Sulfate", "url_name": "sodium-sulfate", "link": "https://www.usgs.gov/centers/national-minerals-information-center/sodium-sulfate-statistics-and-information"},
        {"name": "Statistical Summary", "url_name": "statistical-summary", "link": "https://www.usgs.gov/centers/national-minerals-information-center/statistical-summary"},
        {"name": "Steel", "url_name": "iron-and-steel", "link": "https://www.usgs.gov/centers/national-minerals-information-center/iron-and-steel-statistics-and-information"},
        {"name": "Stone, Crushed", "url_name": "crushed-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/crushed-stone-statistics-and-information"},
        {"name": "Stone, Dimension", "url_name": "dimension-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/dimension-stone-statistics-and-information"},
        {"name": "Strontium", "url_name": "strontium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/strontium-statistics-and-information"},
        {"name": "Sulfur", "url_name": "sulfur", "link": "https://www.usgs.gov/centers/national-minerals-information-center/sulfur-statistics-and-information"},
        {"name": "Survey Methods", "url_name": "survey-methods", "link": "https://www.usgs.gov/centers/national-minerals-information-center/survey-methods"},
        
        # T
        {"name": "Talc", "url_name": "talc-and-pyrophyllite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/talc-and-pyrophyllite-statistics-and-information"},
        {"name": "Tantalum", "url_name": "niobium-and-tantalum", "link": "https://www.usgs.gov/centers/national-minerals-information-center/niobium-and-tantalum-statistics-and-information"},
        {"name": "Tellurium", "url_name": "selenium-and-tellurium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/selenium-and-tellurium-statistics-and-information"},
        {"name": "Thallium", "url_name": "thallium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/thallium-statistics-and-information"},
        {"name": "Thorium", "url_name": "thorium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/thorium-statistics-and-information"},
        {"name": "Tin", "url_name": "tin", "link": "https://www.usgs.gov/centers/national-minerals-information-center/tin-statistics-and-information"},
        {"name": "Titanium", "url_name": "titanium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/titanium-statistics-and-information"},
        {"name": "Titanium Dioxide", "url_name": "titanium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/titanium-statistics-and-information"},
        {"name": "Titanium Mineral Concentrates", "url_name": "titanium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/titanium-statistics-and-information"},
        {"name": "Traprock (Crushed Stone)", "url_name": "crushed-stone", "link": "https://www.usgs.gov/centers/national-minerals-information-center/crushed-stone-statistics-and-information"},
        {"name": "Tripoli (Silica)", "url_name": "silica", "link": "https://www.usgs.gov/centers/national-minerals-information-center/silica-statistics-and-information"},
        {"name": "Tungsten", "url_name": "tungsten", "link": "https://www.usgs.gov/centers/national-minerals-information-center/tungsten-statistics-and-information"},
        
        # V
        {"name": "Vanadium", "url_name": "vanadium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/vanadium-statistics-and-information"},
        {"name": "Vermiculite", "url_name": "vermiculite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/vermiculite-statistics-and-information"},
        
        # W
        {"name": "Wollastonite", "url_name": "wollastonite", "link": "https://www.usgs.gov/centers/national-minerals-information-center/wollastonite-statistics-and-information"},
        
        # Y
        {"name": "Yttrium (Rare Earths)", "url_name": "rare-earths", "link": "https://www.usgs.gov/centers/national-minerals-information-center/rare-earths-statistics-and-information"},
        
        # Z
        {"name": "Zeolites", "url_name": "zeolites", "link": "https://www.usgs.gov/centers/national-minerals-information-center/zeolites-statistics-and-information"},
        {"name": "Zinc", "url_name": "zinc", "link": "https://www.usgs.gov/centers/national-minerals-information-center/zinc-statistics-and-information"},
        {"name": "Zirconium", "url_name": "zirconium-and-hafnium", "link": "https://www.usgs.gov/centers/national-minerals-information-center/zirconium-and-hafnium-statistics-and-information"}
    ]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_commodities = []
    for commodity in commodities:
        identifier = (commodity['name'], commodity['url_name'])
        if identifier not in seen:
            seen.add(identifier)
            unique_commodities.append(commodity)
    
    return unique_commodities

def main():
    """Main function to create and save commodities list"""
    print("Creating USGS mineral commodities list...")
    commodities = extract_commodities_from_html()
    
    if commodities:
        # Save to JSON file
        with open('usgs_mineral_commodities.json', 'w') as f:
            json.dump(commodities, f, indent=2)
        
        print(f"Successfully created list of {len(commodities)} mineral commodities")
        print("Saved to usgs_mineral_commodities.json")
        
        # Show sample data
        print("\nSample entries:")
        for i, commodity in enumerate(commodities[:20]):
            print(f"  {i+1}. {commodity['name']} -> {commodity['url_name']} ({commodity['link']})")
        
        # Count unique url_names
        url_names = set(c['url_name'] for c in commodities)
        print(f"\nUnique URL names: {len(url_names)}")
        
        # Show commodities that share the same url_name
        from collections import defaultdict
        url_name_groups = defaultdict(list)
        for commodity in commodities:
            url_name_groups[commodity['url_name']].append(commodity['name'])
        
        shared_url_names = {k: v for k, v in url_name_groups.items() if len(v) > 1}
        print(f"Commodities sharing URL names: {len(shared_url_names)}")
        for url_name, names in list(shared_url_names.items())[:10]:
            print(f"  {url_name}: {', '.join(names)}")
    else:
        print("No commodities found")

if __name__ == "__main__":
    main()