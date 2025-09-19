import requests
import pandas as pd
import pdfplumber
import io
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from datetime import datetime
import time
import logging
from .base_collector import BaseDataCollector
from .usgs_commodity_codes import get_commodity_code, get_url_pattern, construct_commodity_url, construct_main_document_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('usgs_collector.log'),
        logging.StreamHandler()
    ]
)

class USGSCollector(BaseDataCollector):
    """Enhanced data collector for USGS Mineral Commodity Summaries with historical data support"""
    
    def __init__(self):
        super().__init__(
            name="USGS",
            base_url="https://www.usgs.gov"
        )
        
        # Multiplier mapping
        self.multiplier_map = {
            'thousands': 1000,
            'millions': 1000000,
            'billions': 1000000000,
            'trillions': 1000000000000
        }
        
        # USGS commodity URLs and patterns
        self.commodity_urls = {
            'copper': '/centers/nmic/copper-statistics-and-information',
            'gold': '/centers/nmic/gold-statistics-and-information',
            'silver': '/centers/nmic/silver-statistics-and-information',
            'aluminum': '/centers/nmic/aluminum-statistics-and-information',
            'nickel': '/centers/nmic/nickel-statistics-and-information',
            'zinc': '/centers/nmic/zinc-statistics-and-information',
            'lead': '/centers/nmic/lead-statistics-and-information',
            'lithium': '/centers/nmic/lithium-statistics-and-information',
            'cobalt': '/centers/nmic/cobalt-statistics-and-information',
            'rare_earths': '/centers/nmic/rare-earths-statistics-and-information'
        }
        
        # Comprehensive list of USGS tracked commodities
        self.commodities_list = [
            'aluminum', 'antimony', 'arsenic', 'asbestos', 'barite', 'beryllium',
            'bismuth', 'boron', 'bromine', 'cadmium', 'cesium', 'chromium',
            'cobalt', 'copper', 'diamond', 'diatomite', 'feldspar', 'fluorspar',
            'gallium', 'garnet', 'germanium', 'gold', 'graphite', 'gypsum',
            'hafnium', 'helium', 'indium', 'iodine', 'iron_ore', 'iron_and_steel', 'kyanite',
            'lead', 'lithium', 'magnesium', 'manganese', 'mercury', 'mica',
            'molybdenum', 'nickel', 'niobium', 'nitrogen', 'palladium', 'peat',
            'phosphate_rock', 'platinum', 'potash', 'rare_earths', 'rhenium',
            'rubidium', 'salt', 'sand_gravel', 'scandium', 'selenium', 'silicon',
            'silver', 'sodium_sulfate', 'strontium', 'sulfur', 'talc', 'tantalum',
            'tellurium', 'thallium', 'thorium', 'tin', 'titanium', 'tungsten',
            'vanadium', 'vermiculite', 'yttrium', 'zinc', 'zirconium'
        ]
        
        # Commodities that have dedicated Mineral Commodity Summaries (exclude uranium)
        self.mcs_commodities = [
            'aluminum', 'antimony', 'arsenic', 'asbestos', 'barite', 'beryllium',
            'bismuth', 'boron', 'bromine', 'cadmium', 'cesium', 'chromium',
            'cobalt', 'copper', 'diamond', 'diatomite', 'feldspar', 'fluorspar',
            'gallium', 'garnet', 'germanium', 'gold', 'graphite', 'gypsum',
            'hafnium', 'helium', 'indium', 'iodine', 'iron_ore', 'iron_and_steel', 'kyanite',
            'lead', 'lithium', 'magnesium', 'manganese', 'mercury', 'mica',
            'molybdenum', 'nickel', 'niobium', 'nitrogen', 'palladium', 'peat',
            'phosphate_rock', 'platinum', 'potash', 'rare_earths', 'rhenium',
            'rubidium', 'salt', 'sand_gravel', 'scandium', 'selenium', 'silicon',
            'silver', 'sodium_sulfate', 'strontium', 'sulfur', 'talc', 'tantalum',
            'tellurium', 'thallium', 'thorium', 'tin', 'titanium', 'tungsten',
            'vanadium', 'vermiculite', 'yttrium', 'zinc', 'zirconium'
        ]
        
        self.min_request_interval = 2.0  # Be respectful to USGS servers
        self.historical_data_start_year = 1900  # Collect data going back to 1900
    
    def test_connection(self):
        """Test USGS website connection"""
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'USGS website connection successful',
                    'status_code': response.status_code
                }
            else:
                return {
                    'success': False,
                    'error': f'USGS website returned status {response.status_code}'
                }
        except Exception as e:
            return {'success': False, 'error': f'Connection failed: {str(e)}'}
    
    def collect_data(self, commodity: str = None, data_type: str = 'production', years: List[int] = None) -> List[Dict[str, Any]]:
        """
        Collect USGS commodity data with historical support
        
        Args:
            commodity: Commodity name (if None, collect all)
            data_type: Type of data ('production', 'reserves', 'consumption')
            years: List of years to collect (if None, collect current year)
        """
        all_data = []
        
        # If no specific years provided, collect current year
        if not years:
            years = [datetime.now().year]
        
        # If no specific commodity, collect all
        commodities_to_collect = [commodity] if commodity else list(self.commodity_urls.keys())
        
        for year in years:
            for comm in commodities_to_collect:
                if comm not in self.commodity_urls and comm not in self.commodities_list:
                    self.logger.warning(f"Unknown commodity: {comm}")
                    continue
                
                data = self._collect_commodity_data_for_year(comm, year, data_type)
                all_data.extend(data)
        
        return all_data
    
    def _collect_commodity_data_for_year(self, commodity: str, year: int, data_type: str) -> List[Dict[str, Any]]:
        """Collect data for a specific commodity and year"""
        self.logger.info(f"Collecting data for {commodity} in {year}")
        
        # For years 2020-2025, only collect data for commodities that have dedicated Mineral Commodity Summaries
        if 2020 <= year <= 2025 and commodity not in self.mcs_commodities:
            self.logger.info(f"Skipping {commodity} for {year} as it doesn't have a dedicated Mineral Commodity Summary")
            return []
            
        # For years 1996-2019, use the special URL construction logic
        if 1996 <= year <= 2019:
            commodity_pdf_url = construct_commodity_url(commodity, year)
            if not commodity_pdf_url:
                # If we can't construct a specific commodity URL, do not fall back to the main document
                # The main document is too large and we should only use specific commodity URLs
                self.logger.info(f"Skipping {commodity} for {year} as no specific commodity URL could be constructed")
                return []
            else:
                self.logger.info(f"Constructed specific commodity URL: {commodity_pdf_url}")
        else:
            # For years 2020-2025, use the existing logic
            # Try to get PDF links for the year
            pdf_links = self._get_mcs_pdf_links(year)
            self.logger.info(f"Found {len(pdf_links)} PDF links for {year}")
            
            # Find the specific commodity PDF
            commodity_pdf_url = None
            for link in pdf_links:
                # Check if the link title or URL contains the commodity name
                if (commodity.lower().replace('_', ' ') in link['title'].lower() or 
                    f"{commodity.lower().replace('_', ' ')}.pdf" in link['url'].lower() or
                    f"mcs{year}-{commodity.lower().replace('_', ' ')}.pdf" in link['url'].lower()):
                    commodity_pdf_url = link['url']
                    self.logger.info(f"Found specific commodity PDF: {commodity_pdf_url}")
                    break
            
            # If we still haven't found it, do not fall back to the main MCS PDF
            # The main MCS PDF is too large and we should only use specific commodity PDFs
            if not commodity_pdf_url:
                self.logger.info(f"Skipping {commodity} for {year} as no specific commodity PDF was found")
                return []
            else:
                self.logger.info(f"Using specific commodity PDF: {commodity_pdf_url}")
        
        # Handle the new URL format with fallback options
        primary_url = None
        alternative_urls = []
        
        if isinstance(commodity_pdf_url, dict):
            # New format with primary and alternative URLs
            primary_url = commodity_pdf_url.get('primary')
            alternative_urls = commodity_pdf_url.get('alternatives', [])
            # Try primary URL first
            commodity_pdf_url = primary_url
            self.logger.info(f"Trying primary URL: {primary_url}")
            if alternative_urls:
                self.logger.info(f"Have {len(alternative_urls)} alternative URLs to try if primary fails")
        elif isinstance(commodity_pdf_url, str):
            # Old format, just a single URL
            primary_url = commodity_pdf_url
            self.logger.info(f"Using single URL: {primary_url}")
        else:
            # None or invalid format
            primary_url = None
            self.logger.info("No valid URL found")
        
        # Parse the PDF to extract data
        if commodity_pdf_url:
            self.logger.info(f"Parsing PDF: {commodity_pdf_url}")
            parsed_data = self._parse_mineral_commodity_summary_pdf(commodity_pdf_url, commodity, year)
            self.logger.info(f"PDF parsing result: {parsed_data}")
            
            # If parsing failed and we have alternative URLs, try those
            if not parsed_data.get('success') and alternative_urls:
                self.logger.info(f"Primary URL failed, trying {len(alternative_urls)} alternative URLs")
                for alt_url in alternative_urls:
                    self.logger.info(f"Trying alternative URL: {alt_url}")
                    parsed_data = self._parse_mineral_commodity_summary_pdf(alt_url, commodity, year)
                    if parsed_data.get('success'):
                        self.logger.info(f"Successfully parsed data from alternative URL: {alt_url}")
                        break
                # If all alternatives failed, log the error
                if not parsed_data.get('success'):
                    self.logger.error(f"All URLs failed for {commodity} in {year}: {parsed_data.get('error')}")
                    return []
        else:
            self.logger.warning(f"No PDF found for {commodity} in {year}")
            return []
        
        if not parsed_data['success']:
            self.logger.error(f"Failed to parse PDF for {commodity} in {year}: {parsed_data.get('error')}")
            return []
        
        return parsed_data['data']
    
    def _get_mcs_pdf_links(self, year: int) -> List[Dict[str, str]]:
        """Get links to Mineral Commodity Summaries PDFs for a specific year"""
        try:
            # Determine the correct base URL based on year
            if 1996 <= year <= 2003:
                # For 1996-2003, there's no directory structure, just direct links to PDFs
                # We'll generate the main document URL and return it
                main_pdf_url = construct_main_document_url(year)
                if main_pdf_url:
                    return [{
                        'url': main_pdf_url,
                        'title': f"Mineral Commodity Summaries {year}",
                        'year': year
                    }]
                else:
                    return []
            else:
                # USGS Mineral Commodity Summaries page for specific year (2004+)
                url = f"https://pubs.usgs.gov/periodicals/mcs{year}/"
                response = self._make_html_request(url)
                
                if not response:
                    return []
                
                soup = BeautifulSoup(response, 'html.parser')
                
                # Find PDF links
                pdf_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if '.pdf' in href.lower():
                        # Make absolute URL
                        if href.startswith('/'):
                            href = f"https://pubs.usgs.gov{href}"
                        elif not href.startswith('http'):
                            # Correct URL structure for USGS MCS
                            if href.startswith('mcs'):
                                href = f"https://pubs.usgs.gov/periodicals/mcs{year}/{href}"
                            else:
                                href = f"https://pubs.usgs.gov/{href}"
                        
                        pdf_links.append({
                            'url': href,
                            'title': link.get_text(strip=True),
                            'year': year
                        })
                
                return pdf_links
            
        except Exception as e:
            self.logger.error(f"Error getting MCS PDF links for {year}: {e}")
            return []
    
    def _parse_mineral_commodity_summary_pdf(self, pdf_url: str, commodity: str, year: int) -> Dict[str, Any]:
        """Parse a specific Mineral Commodity Summary PDF and extract data"""
        self.logger.info(f"Parsing PDF for {commodity} in {year}: {pdf_url}")
        
        # Retry logic for network errors
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Download PDF
                response = requests.get(pdf_url, timeout=30)
                if response.status_code != 200:
                    return {"success": False, "error": f"Failed to download PDF: {response.status_code}"}

                pdf_file = io.BytesIO(response.content)
                production_reserves_data = []
                
                with pdfplumber.open(pdf_file) as pdf:
                    self.logger.info(f"PDF has {len(pdf.pages)} pages")
                    # Extract multiplier from first page
                    multiplier = 1
                    if pdf.pages:
                        first_page_text = pdf.pages[0].extract_text()
                        multiplier = self._extract_multiplier(first_page_text)
                    
                    # Look for production data tables
                    for page_idx, page in enumerate(pdf.pages):
                        page_text = page.extract_text()
                        
                        # Log first few lines of each page for debugging
                        lines = page_text.split("\n") if page_text else []
                        self.logger.debug(f"Page {page_idx+1} text: {page_text}")
                        self.logger.debug(f"Page {page_idx+1} first 10 lines: {lines[:10]}")
                        
                        # Look for different table headers that might contain production data
                        table_headers = [
                            "World Smelter Production and Capacity",
                            "World Mine Production and Reserves",
                            "World Production and Reserves",
                            "Production Yearend capacity",
                            "Refinery production",  # For indium and others
                            "Mine production",      # For copper and others
                            # Iron and steel specific headers
                            "World Production:",
                            "Pig iron",
                            "Steel production:"
                        ]
                        
                        found_table = False
                        table_header_line = None
                        for header in table_headers:
                            if header in page_text:
                                self.logger.info(f"Found table header '{header}' on page {page_idx+1}")
                                found_table = True
                                # Find the line with the header
                                lines = page_text.split("\n")
                                for line in lines:
                                    if header in line:
                                        table_header_line = line
                                        break
                                break
                        
                        if found_table:
                            lines = page_text.split("\n")
                            collecting_data = False
                            header_found = False
                            header_line_index = -1
                            
                            # Find the header line index
                            for line_idx, line in enumerate(lines):
                                if table_header_line and table_header_line in line:
                                    header_line_index = line_idx
                                    collecting_data = True
                                    header_found = True
                                    self.logger.info(f"Found header at line {line_idx}: {line}")
                                    continue
                                
                                # Stop collecting when we see another section or end of table
                                if collecting_data and line.strip() and (
                                    "World Resources:" in line or 
                                    "Substitutes:" in line or
                                    "World total" in line.lower() or
                                    "Other countries" in line or
                                    "Notes:" in line or
                                    "Sources:" in line or
                                    len(line.strip()) < 5):
                                    # Check if this is actually the end of the table or just a section title
                                    if "World total" in line:
                                        # This is part of the table, continue
                                        self.logger.info(f"World total line: {line}")
                                    elif "Other countries" in line:
                                        # This might be the last row, continue to process it
                                        self.logger.info(f"Other countries line: {line}")
                                    else:
                                        self.logger.info(f"Stopping collection at line {line_idx}: {line}")
                                        collecting_data = False
                                        continue
                                
                                # Process data lines
                                if collecting_data and line.strip() and len(line.strip()) > 5:
                                    self.logger.info(f"Processing data line {line_idx}: {line}")
                                    # Handle different table formats
                                    
                                    # Special case for tables with multiple columns like "Mine production Refinery production Reserves"
                                    if "Mine production" in table_header_line and "Refinery production" in table_header_line:
                                        # Format: Country Year1 Year2 Year3 Year4 Year5 Reserves
                                        # Extract all numbers from the line
                                        numbers = re.findall(r'[\d,]+', line.strip())
                                        self.logger.info(f"Numbers found: {numbers}")
                                        
                                        # Extract country name by removing numbers and extra whitespace
                                        country = re.sub(r'[\d,]+', '', line.strip()).strip()
                                        self.logger.info(f"Country extracted: '{country}'")
                                        
                                        # Clean up country name (be careful with trailing characters)
                                        if country.endswith('e') and country not in ['Chile']:
                                            country = country[:-1].strip()
                                        self.logger.info(f"Country cleaned: '{country}'")
                                        
                                        # Convert numbers to actual values
                                        production_values = []
                                        for num_str in numbers:
                                            cleaned_value = self._clean_number(num_str)
                                            if cleaned_value is not None:
                                                production_values.append(cleaned_value)
                                        
                                        self.logger.info(f"Production values for {country}: {production_values}")
                                        
                                        # For this format, we have Mine production (2 years), Refinery production (2 years), Reserves (1 value)
                                        if len(production_values) >= 2 and country and country not in ['Country', 'World', 'Production', 'Yearend', 'Mine production Reserves', 'Refinery production Reserves', 'World total (rounded)']:
                                            # Take the most recent mine production value (second one)
                                            production = production_values[1] if len(production_values) > 1 else production_values[0]
                                            # Take the reserves value (last one) if we have 5 or more values
                                            reserves = production_values[-1] if len(production_values) >= 5 else None
                                            
                                            self.logger.info(f"Valid data found: {country}, production: {production}, reserves: {reserves}")
                                            production_reserves_data.append({
                                                'commodity': commodity,
                                                'country': country,
                                                'year': year,
                                                'production_volume': production,
                                                'reserves_volume': reserves,
                                                'unit': 'metric tons',
                                                'multiplier': multiplier,
                                                'source': 'USGS',
                                                'source_url': pdf_url,
                                                'data_type': 'production_reserves'
                                            })
                                        else:
                                            self.logger.info(f"Invalid data: country='{country}', production_values={production_values}")
                                    else:
                                        # Standard format handling
                                        # Extract all numbers from the line
                                        numbers = re.findall(r'[\d,]+', line.strip())
                                        self.logger.info(f"Numbers found: {numbers}")
                                        
                                        # Extract country name by removing numbers and extra whitespace
                                        country = re.sub(r'[\d,]+', '', line.strip()).strip()
                                        self.logger.info(f"Country extracted: '{country}'")
                                        
                                        # Clean up country name (be careful with trailing characters)
                                        if country.endswith('e') and country not in ['Chile']:
                                            country = country[:-1].strip()
                                        self.logger.info(f"Country cleaned: '{country}'")
                                        
                                        # Convert numbers to actual values
                                        production_values = []
                                        for num_str in numbers:
                                            cleaned_value = self._clean_number(num_str)
                                            if cleaned_value is not None:
                                                production_values.append(cleaned_value)
                                        
                                        self.logger.info(f"Production values for {country}: {production_values}")
                                        
                                        # We expect at least 2 values (production for two years)
                                        if len(production_values) >= 2 and country and country not in ['Country', 'World', 'Production', 'Yearend', 'Mine production Reserves', 'Refinery production Reserves', 'World total (rounded)']:
                                            # Take the most recent production value (second one)
                                            production = production_values[1] if len(production_values) > 1 else production_values[0]
                                            # Take the reserves value (last one) if we have 3 or more values
                                            reserves = production_values[-1] if len(production_values) >= 3 else None
                                            
                                            self.logger.info(f"Valid data found: {country}, production: {production}, reserves: {reserves}")
                                            production_reserves_data.append({
                                                'commodity': commodity,
                                                'country': country,
                                                'year': year,
                                                'production_volume': production,
                                                'reserves_volume': reserves,
                                                'unit': 'metric tons',
                                                'multiplier': multiplier,
                                                'source': 'USGS',
                                                'source_url': pdf_url,
                                                'data_type': 'production_reserves'
                                            })
                                        else:
                                            self.logger.info(f"Invalid data: country='{country}', production_values={production_values}")
                
                self.logger.info(f"Finished parsing PDF, found {len(production_reserves_data)} records")
                
                # If no data was found, log more detailed information for debugging
                if len(production_reserves_data) == 0:
                    self.logger.warning(f"No production/reserves data found in PDF for {commodity} in {year}")
                    self.logger.debug(f"PDF URL: {pdf_url}")
                    self.logger.debug(f"First page text preview: {page_text[:500] if 'page_text' in locals() else 'No text extracted'}")
                
                return {
                    "success": True,
                    "pdf_url": pdf_url,
                    "commodity": commodity,
                    "year": year,
                    "data": production_reserves_data,
                    "count": len(production_reserves_data)
                }

            except Exception as e:
                error_msg = str(e)
                self.logger.error(f"Error parsing PDF {pdf_url} (attempt {attempt + 1}/{max_retries}): {e}")
                
                # If it's a connection reset error and we haven't exhausted retries, try again
                if "Connection reset by peer" in error_msg and attempt < max_retries - 1:
                    self.logger.info(f"Retrying due to connection reset... (attempt {attempt + 2})")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    # If it's not a retryable error or we've exhausted retries, return the error
                    return {"success": False, "error": str(e)}
        
        # This should never be reached, but just in case
        return {"success": False, "error": "Maximum retries exceeded"}
    
    def _extract_multiplier(self, page_text: str) -> int:
        """
        Extract multiplier from the PDF subheader text.
        Looks for patterns like "(Data in million metric tons of usable ore"
        and converts to numeric multiplier (1000000 for million).
        """
        # Look for the subheader pattern
        import re
        
        # Pattern to match "(Data in [multiplier] metric tons"
        pattern = r'\(Data in\s+([a-zA-Z]+)\s+metric tons'
        match = re.search(pattern, page_text)
        
        if match:
            multiplier_text = match.group(1).lower()
            # Handle special case for "million" -> "millions"
            if multiplier_text == 'million':
                multiplier_text = 'millions'
            # Handle special case for "thousand" -> "thousands"  
            elif multiplier_text == 'thousand':
                multiplier_text = 'thousands'
            # Handle special case for "billion" -> "billions"
            elif multiplier_text == 'billion':
                multiplier_text = 'billions'
                
            if multiplier_text in self.multiplier_map:
                self.logger.info(f"Found multiplier: {multiplier_text} = {self.multiplier_map[multiplier_text]}")
                return self.multiplier_map[multiplier_text]
        
        # Pattern to match "(Data in metric tons" - no multiplier means 1
        if '(Data in metric tons' in page_text:
            self.logger.info("Found multiplier: metric tons = 1")
            return 1
            
        # Pattern to match "(Data in tons" - no multiplier means 1
        if '(Data in tons' in page_text:
            self.logger.info("Found multiplier: tons = 1")
            return 1
            
        # Default to 1 if no multiplier found
        self.logger.warning("No multiplier found in page text, defaulting to 1")
        return 1
    
    def _clean_number(self, value: str) -> Optional[float]:
        """Clean and convert a number string to float"""
        if not value or value in ['-', 'NA', '']:
            return None
        
        # Remove commas and other formatting
        cleaned = re.sub(r'[^\d\.eE-]', '', value)
        
        try:
            return float(cleaned) if cleaned else None
        except ValueError:
            return None
    
    def collect_historical_data(self, commodity: str = None, start_year: int = 1900, end_year: int = None) -> List[Dict[str, Any]]:
        """
        Collect historical data for commodities from start_year to end_year
        
        Args:
            commodity: Commodity name (if None, collect all major commodities)
            start_year: Starting year (default 1900)
            end_year: Ending year (default current year)
        """
        if not end_year:
            end_year = datetime.now().year
        
        # Create list of years to collect
        years = list(range(start_year, end_year + 1))
        
        # Collect data for all years
        return self.collect_data(commodity=commodity, data_type='production', years=years)
    
    def _collect_commodity_data(self, commodity: str, data_type: str) -> List[Dict[str, Any]]:
        """Collect data for a specific commodity (maintained for backward compatibility)"""
        # For backward compatibility, collect current year data
        return self._collect_commodity_data_for_year(commodity, datetime.now().year, data_type)
    
    def _find_data_links(self, soup: BeautifulSoup, commodity: str) -> List[Dict[str, str]]:
        """Find links to data files on the commodity page (maintained for backward compatibility)"""
        links = []
        
        # Look for links to Excel files, CSV files, and data tables
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().strip()
            
            # Check if it's a data file
            if any(ext in href.lower() for ext in ['.xlsx', '.xls', '.csv', '.pdf']):
                # Make sure it's a full URL
                if not href.startswith('http'):
                    href = self.base_url + href
                
                links.append({
                    'url': href,
                    'text': text,
                    'type': self._determine_link_type(href, text)
                })
        
        return links
    
    def _determine_link_type(self, url: str, text: str) -> str:
        """Determine the type of data in a link (maintained for backward compatibility)"""
        text_lower = text.lower()
        url_lower = url.lower()
        
        if any(word in text_lower for word in ['production', 'mine', 'output']):
            return 'production'
        elif any(word in text_lower for word in ['reserve', 'resource']):
            return 'reserves'
        elif any(word in text_lower for word in ['consumption', 'demand', 'use']):
            return 'consumption'
        elif any(word in text_lower for word in ['price', 'cost']):
            return 'price'
        elif any(word in text_lower for word in ['trade', 'import', 'export']):
            return 'trade'
        else:
            return 'general'
    
    def _is_relevant_link(self, link: Dict[str, str], data_type: str) -> bool:
        """Check if a link is relevant to the requested data type (maintained for backward compatibility)"""
        return link['type'] == data_type or link['type'] == 'general'
    
    def _process_data_link(self, link: Dict[str, str], commodity: str, data_type: str) -> List[Dict[str, Any]]:
        """Process a data link and extract information (maintained for backward compatibility)"""
        processed_data = []
        
        try:
            # For now, we'll create placeholder data
            # In a full implementation, this would download and parse the actual files
            processed_data.append({
                'commodity': commodity,
                'data_type': data_type,
                'source_url': link['url'],
                'source_text': link['text'],
                'data_available': True,
                'last_checked': datetime.utcnow().isoformat(),
                'source': 'USGS'
            })
            
        except Exception as e:
            self.logger.error(f"Error processing link {link['url']}: {e}")
        
        return processed_data
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate a single data point"""
        required_fields = ['commodity', 'source', 'year']
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate year is within acceptable range
        try:
            year = int(data['year'])
            if year < self.historical_data_start_year or year > datetime.now().year + 1:
                return False
        except (ValueError, TypeError):
            return False
        
        return True
    
    def get_available_commodities(self) -> List[str]:
        """Get list of available commodities"""
        return self.commodities_list
    
    def get_mineral_commodity_summaries_url(self, year: int = None) -> str:
        """Get URL for Mineral Commodity Summaries for a specific year"""
        if not year:
            year = datetime.now().year
        
        return f"https://pubs.usgs.gov/periodicals/mcs{year}/"
    
    def collect_production_data(self, commodity: str, countries: List[str] = None, years: List[int] = None) -> List[Dict[str, Any]]:
        """Collect production data for a specific commodity across years"""
        if not years:
            years = [datetime.now().year]
        
        all_data = []
        for year in years:
            # This would implement specific production data collection
            # For now, return placeholder structure
            all_data.extend([{
                'commodity': commodity,
                'country': country,
                'year': year,
                'production_volume': None,
                'unit': 'metric tons',
                'source': 'USGS',
                'data_type': 'production'
            } for country in (countries or ['USA', 'CHN', 'AUS', 'CHL', 'PER'])])
        
        return all_data
    
    def collect_reserves_data(self, commodity: str, countries: List[str] = None, years: List[int] = None) -> List[Dict[str, Any]]:
        """Collect reserves data for a specific commodity across years"""
        if not years:
            years = [datetime.now().year]
        
        all_data = []
        for year in years:
            # This would implement specific reserves data collection
            # For now, return placeholder structure
            all_data.extend([{
                'commodity': commodity,
                'country': country,
                'year': year,
                'reserves_volume': None,
                'unit': 'metric tons',
                'source': 'USGS',
                'data_type': 'reserves'
            } for country in (countries or ['USA', 'CHN', 'AUS', 'CHL', 'PER'])])
        
        return all_data