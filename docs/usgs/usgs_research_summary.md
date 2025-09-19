# USGS Commodity Codes Research Summary

## Task Completed

I have successfully researched and documented the USGS commodity codes for the 1997-2003 period, specifically focusing on the two-digit codes used in PDF filenames. I've also researched the URL patterns for years 1996 and 2004-2007 to understand how to construct URLs for those years.

## Files Created

1. **Documentation File**: `/Users/johnny/Code/GRIP/grip-backend/usgs_commodity_codes_1996_2007.md`
   - Comprehensive mapping of USGS commodity codes for the 1996-2007 period
   - Detailed information about URL patterns for different years
   - Examples of commodity codes including copper (24), gold (30), lithium (45), and 68 others

2. **Python Module**: `/Users/johnny/Code/GRIP/grip-backend/src/data_collectors/usgs_commodity_codes.py`
   - Programmatic access to commodity codes and URL patterns
   - Functions to construct URLs for different years and commodities
   - Support for both numeric codes (1996-2003) and named URLs (2004-2007)

3. **Updated USGS Collector**: `/Users/johnny/Code/GRIP/grip-backend/src/data_collectors/usgs_collector.py`
   - Integrated the new commodity codes module
   - Ready to use the comprehensive mapping for data collection

## Commodity Codes Found

For the 1997-2003 period, I've documented 70 commodity codes including:
- Aluminum (01)
- Antimony (02)
- Copper (24)
- Gold (30)
- Lithium (45)
- And 65 others

## URL Patterns Identified

- **1996-2003**: `https://pubs.usgs.gov/mcs/mcs[YY]-[CODE].pdf`
- **2004-2007**: `https://pubs.usgs.gov/periodicals/mcs[YY]/mcs[YY]-[commodity-name].pdf`

This research will enable the GRIP system to collect historical USGS data across a broader range of commodities and years.