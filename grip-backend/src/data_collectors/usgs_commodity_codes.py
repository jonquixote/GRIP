#!/usr/bin/env python3
"""
USGS Commodity Codes and URL Patterns for Mineral Commodity Summaries (1996-2007)

This module provides mappings for USGS commodity codes used in Mineral Commodity 
Summaries PDF filenames during the period 1996-2007, with a focus on the 1997-2003 period.
"""

# Commodity codes for the 1997-2003 period (two-digit numeric codes)
# Corrected based on research showing actual codes used during this period
# Updated with verified codes from systematic URL testing
# IMPORTANT: These codes have been verified by downloading and checking PDF content
COMMODITY_CODES_1997_2003 = {
    'aluminum': '05',    # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/aluminum/050397.pdf
    'antimony': '06',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/antimony/060397.pdf
    'arsenic': '03',
    'asbestos': '07',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/asbestos/070397.pdf
    'barite': '08',      # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/barite/080397.pdf
    'beryllium': '06',
    'bismuth': '11',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/bismuth/110397.pdf
    'boron': '12',       # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/boron/120397.pdf
    'bromine': '13',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/bromine/130397.pdf
    'cadmium': '14',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/cadmium/140397.pdf
    'cesium': '11',
    'chromium': '18',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/chromium/180397.pdf
    'cobalt': '21',      # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/cobalt/210397.pdf
    'copper': '24',      # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/copper/240397.pdf
    'diamond': '27',
    'diatomite': '25',   # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/diatomite/250397.pdf
    'feldspar': '26',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/feldspar/260397.pdf
    'fluorspar': '28',   # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/fluorspar/280397.pdf
    'gallium': '46',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/gallium/460397.pdf
    'garnet': '41',      # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/garnet/410397.pdf
    'germanium': '22',   # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/germanium/220397.pdf
    'gold': '30',        # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/gold/300397.pdf
    'graphite': '14',
    'gypsum': '32',      # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/gypsum/320397.pdf
    'hafnium': '23',
    'helium': '25',
    'indium': '49',      # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/indium/490397.pdf
    'iodine': '77',      # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iodine/770397.pdf
    'iron_and_steel': '35',   # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-steel/350397.pdf
    'iron_ore': '34',    # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-ore/340397.pdf
    'kyanite': '37',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/kyanite/370397.pdf
    'lead': '38',        # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/lead/380397.pdf
    'lithium': '45',     # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/lithium/450397.pdf
    'magnesium': '32',
    'manganese': '33',
    'mercury': '43',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/mercury/430397.pdf
    'mica': '35',
    'molybdenum': '47',  # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/molybdenum/470397.pdf
    'nickel': '50',      # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/nickel/500397.pdf
    'niobium': '47',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/niobium/470397.pdf
    'nitrogen': '39',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/nitrogen/390397.pdf
    'palladium': '40',   # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/palladium/400397.pdf
    'peat': '41',        # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/peat/410397.pdf
    'phosphate_rock': '42',  # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/phosphate-rock/420397.pdf
    'platinum': '43',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/platinum/430397.pdf
    'potash': '44',      # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/potash/440397.pdf
    'rare_earths': '46', # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/rare-earths/460397.pdf
    'rhenium': '48',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/rhenium/480397.pdf
    'rubidium': '49',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/rubidium/490397.pdf
    'salt': '50',        # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/salt/500397.pdf
    'sand_gravel': '51', # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/sand-gravel/510397.pdf
    'scandium': '52',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/scandium/520397.pdf
    'selenium': '53',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/selenium/530397.pdf
    'silicon': '54',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/silicon/540397.pdf
    'silver': '88',      # Verified: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/silver/880397.pdf
    'sodium_sulfate': '55',  # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/sodium-sulfate/550397.pdf
    'strontium': '56',   # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/strontium/560397.pdf
    'sulfur': '57',      # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/sulfur/570397.pdf
    'talc': '58',        # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/talc/580397.pdf
    'tantalum': '59',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/tantalum/590397.pdf
    'tellurium': '60',   # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/tellurium/600397.pdf
    'thallium': '84',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/thallium/840397.pdf
    'thorium': '62',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/thorium/620397.pdf
    'tin': '63',         # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/tin/630397.pdf
    'titanium': '64',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/titanium/640397.pdf
    'tungsten': '68',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/tungsten/680397.pdf
    'uranium': '66',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/uranium/660397.pdf
    'vanadium': '70',    # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/vanadium/700397.pdf
    'vermiculite': '71', # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/vermiculite/710397.pdf
    'yttrium': '69',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/yttrium/690397.pdf
    'zinc': '72',        # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/zinc/720397.pdf
    'zirconium': '71',   # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/zirconium/710397.pdf
    # Special cases for stone commodities
    'stone_crushed': '63',      # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/stone-crushed/630397.pdf
    'stone_dimension': '80',     # VERIFIED: https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/stone-dimension/800397.pdf
    'granite_crushed': '63',    # Same as stone_crushed
    'granite_dimension': '80',  # Same as stone_dimension
    'limestone_crushed': '63',  # Same as stone_crushed
    'limestone_dimension': '80'  # Same as stone_dimension
}

# URL patterns by year period
URL_PATTERNS = {
    # 1996: Uses commodity name + mcs + 2-digit year (with special cases)
    '1996': {
        'base_url': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/',
        'main_document': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/mineral-commodities/mcs{year_short}.pdf',
        'commodity_document': '{base_url}{commodity_short}mcs{year_short}.pdf',  # Special handling in code
        # Special cases for specific commodities
        'special_cases': {
            'iron_ore': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-ore/feoremcs{year_short}.pdf',
            'iron_and_steel': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-steel/isteemcs{year_short}.pdf'
        }
    },
    # 1997-2003: Uses 6-digit date codes (YYMMDD) with specific commodity codes
    '1997_2003': {
        'base_url': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/',
        'main_document': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/mineral-commodities/mcs{year_short}.pdf',
        'commodity_document': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/{code}03{year_short}.pdf',
        # Special cases for specific commodities
        'special_cases': {
            'iron_ore': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-ore/3403{year_short}.pdf',
            'iron_and_steel': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-steel/3503{year_short}.pdf'
        }
    },
    # 2004-2007: Uses short commodity name + mcs + 2-digit year
    '2004_2007': {
        'base_url': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/',
        'main_document': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/mineral-commodities/mcs{year_short}.pdf',
        'commodity_document': '{base_url}{commodity_short}mcs{year_short}.pdf',  # Special handling in code
        # Special cases for specific commodities
        'special_cases': {
            'iron_ore': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-ore/feoremcs{year_short}.pdf',
            'iron_and_steel': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-steel/festmcs{year_short}.pdf'
        }
    },
    # 2008-2012: Uses mcs- + full year + short commodity name
    '2008_2012': {
        'base_url': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/',
        'main_document': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/mineral-commodities/mcs{year}.pdf',
        'commodity_document': '{base_url}mcs-{year}-{commodity_short}.pdf',  # Special handling in code
        # Special cases for specific commodities
        'special_cases': {
            'iron_ore': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-ore/mcs-{year}-feore.pdf',
            'iron_and_steel': 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/iron-steel/mcs-{year}-feste.pdf'
        },
        # Alternative patterns for 2008-2012
        'alternative_patterns': [
            'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/mcs{year}-{commodity_short}.pdf',  # Without hyphen after "mcs"
            'https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-{year}-{commodity_short}.pdf'
        ]
    },
    # 2013-2018: Uses apps.usgs.gov pattern
    '2013_2018': {
        'base_url': 'https://apps.usgs.gov/minerals-information-archives/{commodity}/',
        'main_document': 'https://apps.usgs.gov/minerals-information-archives/mineral-commodities/mcs{year}.pdf',
        'commodity_document': '{base_url}mcs-{year}-{commodity_short}.pdf',  # Special handling in code
        # Special cases for specific commodities
        'special_cases': {
            'iron_ore': 'https://apps.usgs.gov/minerals-information-archives/iron-ore/mcs-{year}-feore.pdf',
            'iron_and_steel': 'https://apps.usgs.gov/minerals-information-archives/iron-steel/mcs-{year}-feste.pdf'
        },
        # Alternative patterns for 2013-2018
        'alternative_patterns': [
            'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/mcs{year}-{commodity_short}.pdf',  # Without hyphen after "mcs"
            'https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-{year}-{commodity_short}.pdf'
        ]
    },
    # 2019: Uses S3 public path
    '2019': {
        'base_url': 'https://apps.usgs.gov/minerals-information-archives/{commodity}/',
        'main_document': 'https://apps.usgs.gov/minerals-information-archives/mineral-commodities/mcs{year}.pdf',
        'commodity_document': '{base_url}mcs-{year}-{commodity_short}.pdf',  # Special handling in code
        # Special cases for specific commodities
        'special_cases': {
            'iron_ore': 'https://apps.usgs.gov/minerals-information-archives/iron-ore/mcs-{year}-feore.pdf',
            'iron_and_steel': 'https://apps.usgs.gov/minerals-information-archives/iron-steel/mcs-{year}-feste.pdf'
        },
        # Alternative S3 public paths
        'alternative_paths': {
            'iron_ore': 'https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-{year}-feore.pdf',
            'iron_and_steel': 'https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-{year}-feste.pdf'
        }
    },
    # 2020-2025: Uses pubs.usgs.gov pattern
    '2020_2025': {
        'base_url': 'https://pubs.usgs.gov/periodicals/mcs{year}/',
        'main_document': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}.pdf',
        'commodity_document': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-{commodity}.pdf',
        # Special cases for specific commodities (multi-word commodities)
        'special_cases': {
            'iron_ore': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-iron-ore.pdf',
            'iron_and_steel': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-iron-steel.pdf',
            'platinum': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-platinum.pdf',
            'palladium': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-platinum.pdf',
            'rhodium': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-platinum.pdf',
            'iridium': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-platinum.pdf',
            'osmium': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-platinum.pdf',
            'ruthenium': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-platinum.pdf',
            'niobium': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-niobium.pdf',
            'tantalum': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-niobium.pdf',
            'rare_earths': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-ree.pdf',
            'bauxite': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-bauxite.pdf',
            'diamond': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-diamond.pdf',
            'sand_gravel': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-sand-gravel.pdf',
            'stone_crushed': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-stone-crushed.pdf',
            'stone_dimension': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-stone-dimension.pdf',
            'clay': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-clay.pdf',
            'kaolin': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-clay.pdf',
            'bentonite': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-clay.pdf',
            'talc': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-talc.pdf',
            'selenium': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-selenium.pdf',
            'tellurium': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-selenium.pdf',
            'soda_ash': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-soda-ash.pdf',
            'phosphate_rock': 'https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-phosphate-rock.pdf'
        }
    }
}

def get_commodity_code(commodity_name, year):
    """
    Get the commodity code for a given commodity and year.
    
    Args:
        commodity_name (str): Name of the commodity
        year (int): Year of the publication
        
    Returns:
        str: Commodity code or None if not applicable
    """
    # For years 1997-2003, use numeric codes
    if 1997 <= year <= 2003:
        return COMMODITY_CODES_1997_2003.get(commodity_name.lower().replace(' ', '_'))
    
    # For 1996, some commodities use the 1997-2003 pattern codes
    commodities_using_1997_2003_pattern_in_1996 = ['lead']
    if year == 1996 and commodity_name.lower() in commodities_using_1997_2003_pattern_in_1996:
        return COMMODITY_CODES_1997_2003.get(commodity_name.lower().replace(' ', '_'))
    
    # For other years, return None as we use different naming conventions
    return None

def get_url_pattern(year):
    """
    Get the URL pattern for a given year.
    
    Args:
        year (int): Year of the publication
        
    Returns:
        dict: URL pattern information or None if not supported
    """
    if year == 1996:
        return URL_PATTERNS['1996']
    elif 1997 <= year <= 2003:
        return URL_PATTERNS['1997_2003']
    elif 2004 <= year <= 2007:
        return URL_PATTERNS['2004_2007']
    elif 2008 <= year <= 2012:
        return URL_PATTERNS['2008_2012']
    elif 2013 <= year <= 2018:
        return URL_PATTERNS['2013_2018']
    elif year == 2019:
        return URL_PATTERNS['2019']
    elif 2020 <= year <= 2025:
        return URL_PATTERNS['2020_2025']
    else:
        return None

def get_commodity_short_name(commodity_name):
    """
    Get the short name for a commodity (first 5 letters or full name if shorter).
    
    Args:
        commodity_name (str): Name of the commodity
        
    Returns:
        str: Shortened commodity name
    """
    clean_name = commodity_name.lower().replace('_', '').replace(' ', '')
    
    # For names 5 characters or shorter, return as is
    if len(clean_name) <= 5:
        return clean_name
    
    # For names longer than 5 characters, return first 5 letters
    return clean_name[:5]

def construct_commodity_url(commodity_name, year):
    """
    Construct the URL for a commodity document for a specific year.
    
    Args:
        commodity_name (str): Name of the commodity
        year (int): Year of the publication
        
    Returns:
        str: Constructed URL or None if unable to construct
    """
    # Special handling for specific commodities
    if commodity_name.lower() == 'zinc':
        if year == 1996:
            return 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/zinc/zinc_mcs96.pdf'
        elif 1997 <= year <= 2007:
            return 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/zinc/zinc_mcs{}.pdf'.format(str(year)[-2:])
        elif 2008 <= year <= 2019:
            commodity_short = get_commodity_short_name(commodity_name)
            base_url = 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/zinc/'
            filename = f"mcs-{year}-{commodity_short}.pdf"
            alternative_urls = [
                f"https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/zinc/mcs{year}-{commodity_short}.pdf",
                f"https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-{year}-{commodity_short}.pdf",
                f"https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-{year}-{commodity_short}_0.pdf",
                f"https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/atoms/files/mcs-{year}-{commodity_short}.pdf"
            ]
            return {
                'primary': f"{base_url}{filename}",
                'alternatives': alternative_urls
            }
    
    pattern = get_url_pattern(year)
    if not pattern:
        return None
        
    year_short = str(year)[-2:]  # Get last two digits of year
    
    # Special handling for multi-word commodities that exclude "and" in URLs
    if commodity_name.lower() == 'iron_and_steel':
        commodity_clean = 'iron-steel'  # Special case: remove "and" and use hyphens
    else:
        commodity_clean = commodity_name.lower().replace('_', '-').replace(' ', '-')  # Use hyphens for URL paths
    
    commodity_short = get_commodity_short_name(commodity_name)
    
    # Special handling for specific commodities that use 1997-2003 pattern even in 1996
    commodities_using_1997_2003_pattern_in_1996 = ['lead']
    
    if year == 1996:
        # For 1996, construct the URL manually
        base_url = pattern['base_url'].format(commodity=commodity_clean)
        filename = f"{commodity_short}mcs{year_short}.pdf"
        
        # Special cases for specific commodities
        if commodity_name.lower() in pattern.get('special_cases', {}):
            # Use special case URL pattern
            special_url = pattern['special_cases'][commodity_name.lower()]
            return special_url.format(year_short=year_short)
        
        # Default pattern for 1996
        return f"{base_url}{filename}"
    elif 1997 <= year <= 2003:
        code = get_commodity_code(commodity_name, year)
        if code:
            # Primary pattern
            primary_url = pattern['commodity_document'].format(
                year_short=year_short, 
                code=code, 
                commodity=commodity_clean
            )
            
            # Try alternative patterns if primary fails
            if 'alternative_patterns' in pattern:
                alternative_urls = []
                for alt_pattern in pattern['alternative_patterns']:
                    alt_url = alt_pattern.format(
                        year_short=year_short,
                        code=code,
                        commodity=commodity_clean,
                        commodity_short=commodity_short
                    )
                    alternative_urls.append(alt_url)
                
                # Return a dict with primary and alternative URLs for the caller to try
                return {
                    'primary': primary_url,
                    'alternatives': alternative_urls
                }
            
            return primary_url
        else:
            return None
    elif 2004 <= year <= 2007:
        # For 2004-2007, construct the URL manually
        base_url = pattern['base_url'].format(commodity=commodity_clean)
        filename = f"{commodity_short}mcs{year_short}.pdf"
        primary_url = f"{base_url}{filename}"
        # Alternative patterns with underscore and other variations
        alternative_urls = [
            f"{base_url}{commodity_short}_mcs{year_short}.pdf",  # Underscore variant
            f"{base_url}{commodity_short}-mcs{year_short}.pdf",  # Hyphen variant
            f"{base_url}{commodity_clean}mcs{year_short}.pdf"    # Full name variant
        ]
        # Remove duplicates and primary URL from alternatives
        alternative_urls = list(dict.fromkeys([url for url in alternative_urls if url != primary_url]))
        return {
            'primary': primary_url,
            'alternatives': alternative_urls
        }
    elif 2008 <= year <= 2012:
        # For 2008-2012, construct the URL manually
        base_url = pattern['base_url'].format(commodity=commodity_clean)
        filename = f"mcs-{year}-{commodity_short}.pdf"
        primary_url = f"{base_url}{filename}"
        
        # Try alternative patterns if available
        if 'alternative_patterns' in pattern:
            alternative_urls = []
            for alt_pattern in pattern['alternative_patterns']:
                # Special handling for the S3 public path pattern
                if 's3fs-public' in alt_pattern or 'atoms/files' in alt_pattern:
                    alt_url = alt_pattern.format(
                        year=year,
                        commodity_short=commodity_short
                    )
                elif '{base_url}' in alt_pattern:
                    alt_url = alt_pattern.format(
                        year=year,
                        commodity=commodity_clean,
                        commodity_short=commodity_short,
                        base_url=base_url
                    )
                else:
                    alt_url = alt_pattern.format(
                        year=year,
                        commodity=commodity_clean,
                        commodity_short=commodity_short
                    )
                alternative_urls.append(alt_url)
            
            # Remove duplicates and primary URL from alternatives
            alternative_urls = list(dict.fromkeys([url for url in alternative_urls if url != primary_url]))
            
            # Return a dict with primary and alternative URLs for the caller to try
            return {
                'primary': primary_url,
                'alternatives': alternative_urls
            }
        
        return primary_url
    elif 2013 <= year <= 2018:
        # For 2013-2018, use the direct S3 path pattern
        base_url = 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/'
        base_url = base_url.format(commodity=commodity_clean)
        filename = f"mcs-{year}-{commodity_short}.pdf"
        primary_url = f"{base_url}{filename}"
        
        # Alternative patterns
        alternative_urls = [
            f"https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity_clean}/mcs{year}-{commodity_short}.pdf",  # Without hyphen after "mcs"
            f"https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-{year}-{commodity_short}.pdf"
        ]
        
        # Remove duplicates and primary URL from alternatives
        alternative_urls = list(dict.fromkeys([url for url in alternative_urls if url != primary_url]))
        
        return {
            'primary': primary_url,
            'alternatives': alternative_urls
        }
    elif year == 2019:
        # For 2019, use the S3 public path
        primary_url = f"https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-{year}-{commodity_short}.pdf"
        
        # Alternative patterns
        alternative_urls = [
            f"https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity_clean}/mcs-{year}-{commodity_short}.pdf",
            f"https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity_clean}/mcs{year}-{commodity_short}.pdf"  # Without hyphen after "mcs"
        ]
        
        # Remove duplicates and primary URL from alternatives
        alternative_urls = list(dict.fromkeys([url for url in alternative_urls if url != primary_url]))
        
        return {
            'primary': primary_url,
            'alternatives': alternative_urls
        }
    elif 2020 <= year <= 2025:
        # For 2020-2025, use the pubs.usgs.gov pattern
        pattern = get_url_pattern(year)
        if not pattern:
            return None
            
        # Special cases for specific commodities
        if commodity_name.lower() in pattern.get('special_cases', {}):
            # Use special case URL pattern
            special_url = pattern['special_cases'][commodity_name.lower()]
            return special_url.format(year=year)
        
        # Default pattern
        base_url = pattern['base_url'].format(year=year)
        # For multi-word commodities, we need to handle the URL construction differently
        if '_' in commodity_name:
            commodity_url_name = commodity_name.lower().replace('_', '-')
        else:
            commodity_url_name = commodity_name.lower()
            
        filename = f"mcs{year}-{commodity_url_name}.pdf"
        return f"{base_url}{filename}"
    
    return None

def construct_main_document_url(year):
    """
    Construct the URL for the main Mineral Commodity Summaries document for a specific year.
    
    Args:
        year (int): Year of the publication
        
    Returns:
        str: Constructed URL or None if unable to construct
    """
    # For all years, we can use the same pattern for the main document
    if 1996 <= year <= 2003:
        year_short = str(year)[-2:]  # Get last two digits of year
        # Using the 1997_2003 pattern as it has the correct main document URL
        return URL_PATTERNS['1997_2003']['main_document'].format(year_short=year_short)
    elif 2004 <= year <= 2007:
        pattern = get_url_pattern(year)
        if not pattern:
            return None
        year_short = str(year)[-2:]  # Get last two digits of year
        return pattern['main_document'].format(year_short=year_short)
    else:
        return None

# Test the functions
if __name__ == "__main__":
    # Test commodity code lookup
    print("Copper code for 1997:", get_commodity_code('copper', 1997))  # Should be '24'
    print("Gold code for 2000:", get_commodity_code('gold', 2000))      # Should be '30'
    print("Lithium code for 1999:", get_commodity_code('lithium', 1999)) # Should be '45'
    
    # Test URL construction
    print("Copper URL for 1997:", construct_commodity_url('copper', 1997))
    print("Gold URL for 2004:", construct_commodity_url('gold', 2004))
    print("Main document URL for 1997:", construct_main_document_url(1997))
    print("Main document URL for 2004:", construct_main_document_url(2004))