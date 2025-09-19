# USGS Mineral Commodity Summaries URL Patterns and Special Cases

## Overview

This document outlines the URL patterns used for USGS Mineral Commodity Summaries across different time periods, with a focus on special cases and fallback strategies for data collection.

## URL Patterns by Time Period

### 1996
- **Main Document**: `https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/mineral-commodities/mcs{year_short}.pdf`
- **Commodity Document**: `{base_url}{commodity_short}mcs{year_short}.pdf`

### 1997-2003
- **Main Document**: `https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/mineral-commodities/mcs{year_short}.pdf`
- **Commodity Document**: `https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/{code}03{year_short}.pdf`
- **Alternative Patterns**:
  - `https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/{code}{year_short}.pdf`
  - `https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/{commodity}/{commodity_short}mcs{year_short}.pdf`

### 2004-2007
- **Main Document**: `https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/mineral-commodities/mcs{year_short}.pdf`
- **Commodity Document**: `{base_url}{commodity_short}mcs{year_short}.pdf`

### 2008-2019
- **Main Document**: `https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/mineral-commodities/mcs{year}.pdf`
- **Commodity Document**: `{base_url}mcs-{year}-{commodity_short}.pdf`
- **Alternative Patterns** (especially for 2019):
  - `{base_url}mcs{year}-{commodity_short}.pdf`
  - `https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-{year}-{commodity_short}.pdf`

### 2020-2025
- **Main Document**: `https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}.pdf`
- **Commodity Document**: `https://pubs.usgs.gov/periodicals/mcs{year}/mcs{year}-{commodity}.pdf`

## Special Cases and Exceptions

### Zinc Special Cases
Zinc has been identified as having special URL patterns in some years. The system should try alternative patterns when the primary URL construction fails.

### 2019 Pattern Variations
The year 2019 has been noted to sometimes use different URL structures:
- Standard: `mcs-2019-{commodity_short}.pdf`
- Alternative: `mcs2019-{commodity_short}.pdf` (without the hyphen after "mcs")
- S3 Public Path: `https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mcs-2019-{commodity_short}.pdf`

## Corrected Commodity Codes for 1997-2003 Period

The following commodity codes have been corrected based on research:

| Commodity | Old Code | New Code | Notes |
|-----------|----------|----------|-------|
| Cobalt | 13 | 21 | Confirmed correction |
| Silver | 54 | 88 | Confirmed correction |
| Diamond | 14 | 27 | Confirmed code |
| Lead | 31 | 38 | Confirmed code |
| Graphite | 21 | 14 | Corrected (was conflicting with cobalt) |
| Iodine | 27 | 37 | Corrected (was conflicting with diamond) |
| Nickel | 37 | 13 | Corrected (was conflicting with iodine, reclaiming old cobalt code) |
| Niobium | 38 | 47 | Corrected (was conflicting with lead) |
| Rhenium | 47 | 48 | Corrected (was conflicting with niobium) |
| Rubidium | 48 | 49 | Corrected (was conflicting with rhenium) |
| Salt | 49 | 50 | Corrected (was conflicting with sand_gravel) |
| Sand/Gravel | 50 | 51 | Corrected (was conflicting with salt) |
| Scandium | 51 | 52 | Corrected (was conflicting with selenium) |
| Selenium | 52 | 53 | Corrected (was conflicting with scandium) |
| Silicon | 53 | 54 | Corrected (was conflicting with silver) |

## Fallback System Implementation

The system implements a multi-level fallback approach:

1. **Primary URL**: Try the main pattern for the time period
2. **Alternative URLs**: If primary fails, try alternative patterns
3. **Main Document**: If all commodity-specific URLs fail, fall back to the main MCS document for that year
4. **Error Handling**: Log failures and continue with other commodities/years

## Implementation Notes

1. **URL Construction**: The `construct_commodity_url` function now returns either a string (single URL) or a dictionary with 'primary' and 'alternatives' keys for more complex cases.

2. **Collector Logic**: The `USGSCollector._collect_commodity_data_for_year` method has been updated to handle the new return format and implement the fallback logic.

3. **Pattern Testing**: When implementing new collectors or debugging URL issues, test all alternative patterns for a given time period.

4. **Special Case Handling**: For commodities like zinc that are known to have special cases, always implement comprehensive fallback strategies.

## Testing Strategy

To verify the URL patterns and fallback system:

1. Test with known commodities and years
2. Verify that corrected codes produce valid URLs
3. Test fallback behavior when primary URLs fail
4. Check that alternative patterns are correctly constructed
5. Validate that the system gracefully handles completely unavailable documents

This system should provide robust access to USGS Mineral Commodity Summaries across all time periods while gracefully handling the variations and special cases that exist in the archive.