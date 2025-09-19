import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .base_analyzer import BaseAnalyzer

class ProductionAnalyzer(BaseAnalyzer):
    """Analyzer for commodity production data"""
    
    def __init__(self):
        super().__init__("ProductionAnalyzer")
    
    def analyze(self, data: pd.DataFrame, commodity: str = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze commodity production data
        
        Args:
            data: DataFrame with columns ['year', 'production_volume', 'country', 'commodity']
            commodity: Specific commodity to analyze (optional)
        """
        required_columns = ['year', 'production_volume']
        if not self.validate_data(data, required_columns):
            return {'error': 'Invalid data format'}
        
        # Clean the data
        data = self.clean_data(data)
        
        # Filter by commodity if specified
        if commodity and 'commodity' in data.columns:
            data = data[data['commodity'] == commodity]
        
        if len(data) == 0:
            return {'error': 'No data available for analysis'}
        
        # Sort by year
        data = data.sort_values('year')
        
        # Perform various analyses
        results = {
            'commodity': commodity,
            'analysis_date': datetime.utcnow().isoformat(),
            'data_points': len(data),
            'year_range': {
                'start': int(data['year'].min()) if not data['year'].empty else None,
                'end': int(data['year'].max()) if not data['year'].empty else None
            }
        }
        
        # Basic statistics
        results['statistics'] = self.calculate_statistics(data['production_volume'])
        
        # Trend analysis
        results['trend'] = self.calculate_trend(data['production_volume'])
        
        # Country analysis (if country data available)
        if 'country' in data.columns:
            results['country_analysis'] = self.analyze_by_country(data)
        
        # Year-over-year growth
        results['growth_analysis'] = self.analyze_growth(data)
        
        # Production concentration
        results['concentration'] = self.analyze_concentration(data)
        
        # Supply risk assessment
        results['supply_risk'] = self.assess_supply_risk(data)
        
        # Production forecasting
        results['forecast'] = self.forecast_production(data)
        
        return results
    
    def analyze_by_country(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze production by country"""
        # Total production by country
        country_totals = data.groupby('country')['production_volume'].sum().sort_values(ascending=False)
        
        # Average annual production by country
        country_averages = data.groupby('country')['production_volume'].mean().sort_values(ascending=False)
        
        # Production share by country (latest year)
        latest_year = data['year'].max()
        latest_data = data[data['year'] == latest_year]
        total_latest = latest_data['production_volume'].sum()
        
        if total_latest > 0:
            country_shares = (latest_data.groupby('country')['production_volume'].sum() / total_latest * 100).sort_values(ascending=False)
        else:
            country_shares = pd.Series()
        
        # Growth rates by country
        country_growth = {}
        for country in data['country'].unique():
            country_data = data[data['country'] == country].sort_values('year')
            if len(country_data) >= 2:
                first_year_prod = country_data['production_volume'].iloc[0]
                last_year_prod = country_data['production_volume'].iloc[-1]
                years_span = country_data['year'].iloc[-1] - country_data['year'].iloc[0]
                
                if first_year_prod > 0 and years_span > 0:
                    cagr = ((last_year_prod / first_year_prod) ** (1/years_span) - 1) * 100
                    country_growth[country] = cagr
        
        return {
            'top_producers': country_totals.head(10).to_dict(),
            'market_share': country_shares.head(10).to_dict(),
            'average_production': country_averages.head(10).to_dict(),
            'growth_rates': country_growth,
            'total_countries': len(data['country'].unique())
        }
    
    def analyze_growth(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze production growth patterns"""
        # Year-over-year growth
        if 'country' in data.columns:
            # Aggregate by year first
            yearly_data = data.groupby('year')['production_volume'].sum().reset_index()
        else:
            yearly_data = data.copy()
        
        yearly_data = yearly_data.sort_values('year')
        yearly_data['yoy_growth'] = yearly_data['production_volume'].pct_change() * 100
        
        # Growth statistics
        growth_stats = self.calculate_statistics(yearly_data['yoy_growth'].dropna())
        
        # Identify growth periods
        positive_growth_years = yearly_data[yearly_data['yoy_growth'] > 0]
        negative_growth_years = yearly_data[yearly_data['yoy_growth'] < 0]
        
        # Calculate CAGR (Compound Annual Growth Rate)
        if len(yearly_data) >= 2:
            first_year_prod = yearly_data['production_volume'].iloc[0]
            last_year_prod = yearly_data['production_volume'].iloc[-1]
            years_span = yearly_data['year'].iloc[-1] - yearly_data['year'].iloc[0]
            
            if first_year_prod > 0 and years_span > 0:
                cagr = ((last_year_prod / first_year_prod) ** (1/years_span) - 1) * 100
            else:
                cagr = 0
        else:
            cagr = 0
        
        return {
            'growth_statistics': growth_stats,
            'cagr': cagr,
            'positive_growth_years': len(positive_growth_years),
            'negative_growth_years': len(negative_growth_years),
            'best_growth_year': {
                'year': int(yearly_data.loc[yearly_data['yoy_growth'].idxmax(), 'year']) if not yearly_data['yoy_growth'].empty else None,
                'growth_rate': yearly_data['yoy_growth'].max()
            },
            'worst_growth_year': {
                'year': int(yearly_data.loc[yearly_data['yoy_growth'].idxmin(), 'year']) if not yearly_data['yoy_growth'].empty else None,
                'growth_rate': yearly_data['yoy_growth'].min()
            }
        }
    
    def analyze_concentration(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze production concentration"""
        if 'country' not in data.columns:
            return {'error': 'Country data required for concentration analysis'}
        
        # Use latest year data
        latest_year = data['year'].max()
        latest_data = data[data['year'] == latest_year]
        
        # Calculate country shares
        total_production = latest_data['production_volume'].sum()
        if total_production == 0:
            return {'error': 'No production data for latest year'}
        
        country_shares = (latest_data.groupby('country')['production_volume'].sum() / total_production).sort_values(ascending=False)
        
        # Calculate Herfindahl-Hirschman Index (HHI)
        hhi = (country_shares ** 2).sum() * 10000  # Multiply by 10000 for standard HHI scale
        
        # Concentration ratios
        cr3 = country_shares.head(3).sum() * 100  # Top 3 countries
        cr5 = country_shares.head(5).sum() * 100  # Top 5 countries
        cr10 = country_shares.head(10).sum() * 100  # Top 10 countries
        
        # Interpret concentration level
        if hhi < 1500:
            concentration_level = 'Low'
        elif hhi < 2500:
            concentration_level = 'Moderate'
        else:
            concentration_level = 'High'
        
        return {
            'hhi': hhi,
            'concentration_level': concentration_level,
            'concentration_ratios': {
                'cr3': cr3,
                'cr5': cr5,
                'cr10': cr10
            },
            'top_producer_share': country_shares.iloc[0] * 100 if len(country_shares) > 0 else 0,
            'number_of_producers': len(country_shares)
        }
    
    def assess_supply_risk(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess supply risk based on production patterns"""
        risk_factors = {}
        overall_risk_score = 0
        
        # Concentration risk
        concentration = self.analyze_concentration(data)
        if 'hhi' in concentration:
            if concentration['hhi'] > 2500:
                risk_factors['concentration'] = {'level': 'High', 'score': 3}
                overall_risk_score += 3
            elif concentration['hhi'] > 1500:
                risk_factors['concentration'] = {'level': 'Medium', 'score': 2}
                overall_risk_score += 2
            else:
                risk_factors['concentration'] = {'level': 'Low', 'score': 1}
                overall_risk_score += 1
        
        # Volatility risk
        if 'country' in data.columns:
            yearly_totals = data.groupby('year')['production_volume'].sum()
        else:
            yearly_totals = data.set_index('year')['production_volume']
        
        volatility = self.calculate_volatility(yearly_totals)
        mean_production = yearly_totals.mean()
        cv = (volatility / mean_production) * 100 if mean_production > 0 else 0  # Coefficient of variation
        
        if cv > 20:
            risk_factors['volatility'] = {'level': 'High', 'score': 3, 'cv': cv}
            overall_risk_score += 3
        elif cv > 10:
            risk_factors['volatility'] = {'level': 'Medium', 'score': 2, 'cv': cv}
            overall_risk_score += 2
        else:
            risk_factors['volatility'] = {'level': 'Low', 'score': 1, 'cv': cv}
            overall_risk_score += 1
        
        # Trend risk (declining production)
        trend = self.calculate_trend(yearly_totals)
        if trend['trend'] == 'decreasing' and trend['r_squared'] > 0.5:
            risk_factors['trend'] = {'level': 'High', 'score': 3}
            overall_risk_score += 3
        elif trend['trend'] == 'decreasing':
            risk_factors['trend'] = {'level': 'Medium', 'score': 2}
            overall_risk_score += 2
        else:
            risk_factors['trend'] = {'level': 'Low', 'score': 1}
            overall_risk_score += 1
        
        # Overall risk assessment
        max_possible_score = 9  # 3 factors × 3 max score each
        risk_percentage = (overall_risk_score / max_possible_score) * 100
        
        if risk_percentage > 70:
            overall_risk = 'High'
        elif risk_percentage > 40:
            overall_risk = 'Medium'
        else:
            overall_risk = 'Low'
        
        return {
            'overall_risk': overall_risk,
            'risk_score': overall_risk_score,
            'risk_percentage': risk_percentage,
            'risk_factors': risk_factors
        }
    
    def forecast_production(self, data: pd.DataFrame, years_ahead: int = 5) -> Dict[str, Any]:
        """Simple production forecasting"""
        if 'country' in data.columns:
            yearly_data = data.groupby('year')['production_volume'].sum().reset_index()
        else:
            yearly_data = data.copy()
        
        if len(yearly_data) < 3:
            return {'error': 'Insufficient data for forecasting'}
        
        yearly_data = yearly_data.sort_values('year')
        
        # Simple linear trend forecast
        trend = self.calculate_trend(yearly_data['production_volume'])
        
        last_year = yearly_data['year'].iloc[-1]
        last_production = yearly_data['production_volume'].iloc[-1]
        
        forecasts = {}
        for i in range(1, years_ahead + 1):
            forecast_year = last_year + i
            forecast_production = last_production + (trend['slope'] * i)
            forecasts[int(forecast_year)] = max(0, forecast_production)  # Ensure non-negative
        
        # Calculate forecast confidence based on trend R-squared
        confidence = min(trend['r_squared'] * 100, 80)  # Cap at 80%
        
        return {
            'forecasts': forecasts,
            'method': 'linear_trend',
            'confidence': confidence,
            'trend_slope': trend['slope'],
            'base_year': int(last_year),
            'base_production': last_production
        }
    
    def compare_production_efficiency(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Compare production efficiency across countries"""
        if 'country' not in data.columns:
            return {'error': 'Country data required for efficiency analysis'}
        
        # Calculate production per country over time
        country_efficiency = {}
        
        for country in data['country'].unique():
            country_data = data[data['country'] == country].sort_values('year')
            
            if len(country_data) >= 2:
                # Calculate average annual production
                avg_production = country_data['production_volume'].mean()
                
                # Calculate production stability (inverse of coefficient of variation)
                std_production = country_data['production_volume'].std()
                stability = 1 / (std_production / avg_production) if avg_production > 0 and std_production > 0 else 1
                
                # Calculate growth consistency
                country_data['yoy_growth'] = country_data['production_volume'].pct_change()
                growth_volatility = country_data['yoy_growth'].std()
                growth_consistency = 1 / (1 + growth_volatility) if not np.isnan(growth_volatility) else 1
                
                country_efficiency[country] = {
                    'avg_production': avg_production,
                    'stability_score': stability,
                    'growth_consistency': growth_consistency,
                    'efficiency_score': (stability + growth_consistency) / 2
                }
        
        # Rank countries by efficiency
        efficiency_ranking = sorted(country_efficiency.items(), 
                                  key=lambda x: x[1]['efficiency_score'], 
                                  reverse=True)
        
        return {
            'country_efficiency': country_efficiency,
            'efficiency_ranking': [(country, scores['efficiency_score']) for country, scores in efficiency_ranking],
            'most_efficient': efficiency_ranking[0][0] if efficiency_ranking else None,
            'least_efficient': efficiency_ranking[-1][0] if efficiency_ranking else None
        }

