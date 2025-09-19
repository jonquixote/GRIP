import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .base_analyzer import BaseAnalyzer

class PriceAnalyzer(BaseAnalyzer):
    """Analyzer for commodity price data"""
    
    def __init__(self):
        super().__init__("PriceAnalyzer")
    
    def analyze(self, data: pd.DataFrame, commodity: str = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze commodity price data
        
        Args:
            data: DataFrame with columns ['date', 'price', 'commodity']
            commodity: Specific commodity to analyze (optional)
        """
        if not self.validate_data(data, ['date', 'price']):
            return {'error': 'Invalid data format'}
        
        # Clean the data
        data = self.clean_data(data)
        
        # Filter by commodity if specified
        if commodity and 'commodity' in data.columns:
            data = data[data['commodity'] == commodity]
        
        if len(data) == 0:
            return {'error': 'No data available for analysis'}
        
        # Sort by date
        data = data.sort_values('date')
        
        # Perform various analyses
        results = {
            'commodity': commodity,
            'analysis_date': datetime.utcnow().isoformat(),
            'data_points': len(data),
            'date_range': {
                'start': data['date'].min().isoformat() if not data['date'].empty else None,
                'end': data['date'].max().isoformat() if not data['date'].empty else None
            }
        }
        
        # Basic statistics
        results['statistics'] = self.calculate_statistics(data['price'])
        
        # Trend analysis
        results['trend'] = self.calculate_trend(data['price'])
        
        # Volatility analysis
        results['volatility'] = {
            'daily': self.calculate_volatility(data['price'], window=30),
            'weekly': self.calculate_volatility(data['price'], window=7),
            'monthly': self.calculate_volatility(data['price'], window=90)
        }
        
        # Price movements
        results['price_movements'] = self.analyze_price_movements(data)
        
        # Support and resistance levels
        results['support_resistance'] = self.find_support_resistance_levels(data['price'])
        
        # Seasonal patterns
        if len(data) > 365:  # Need at least a year of data
            results['seasonality'] = self.analyze_seasonality(data)
        
        # Risk metrics
        results['risk_metrics'] = self.calculate_risk_metrics(data['price'])
        
        # Price forecasting (simple)
        results['forecast'] = self.simple_forecast(data['price'])
        
        return results
    
    def analyze_price_movements(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze price movements and returns"""
        data = data.copy()
        data['returns'] = data['price'].pct_change()
        data['log_returns'] = np.log(data['price'] / data['price'].shift(1))
        
        # Daily returns statistics
        returns_stats = self.calculate_statistics(data['returns'].dropna())
        
        # Identify significant movements
        threshold = data['returns'].std() * 2  # 2 standard deviations
        significant_moves = data[abs(data['returns']) > threshold]
        
        return {
            'returns_statistics': returns_stats,
            'significant_movements': {
                'count': len(significant_moves),
                'threshold': threshold,
                'largest_gain': data['returns'].max(),
                'largest_loss': data['returns'].min()
            },
            'consecutive_gains': self.find_consecutive_movements(data['returns'], positive=True),
            'consecutive_losses': self.find_consecutive_movements(data['returns'], positive=False)
        }
    
    def find_consecutive_movements(self, returns: pd.Series, positive: bool = True) -> Dict[str, Any]:
        """Find consecutive positive or negative movements"""
        if positive:
            condition = returns > 0
        else:
            condition = returns < 0
        
        # Find consecutive sequences
        groups = (condition != condition.shift()).cumsum()
        consecutive = returns[condition].groupby(groups[condition])
        
        if len(consecutive) == 0:
            return {'max_streak': 0, 'avg_streak': 0, 'total_streaks': 0}
        
        streak_lengths = consecutive.size()
        
        return {
            'max_streak': streak_lengths.max(),
            'avg_streak': streak_lengths.mean(),
            'total_streaks': len(streak_lengths)
        }
    
    def find_support_resistance_levels(self, prices: pd.Series, window: int = 20) -> Dict[str, Any]:
        """Identify support and resistance levels"""
        # Rolling min/max for support/resistance
        rolling_min = prices.rolling(window=window).min()
        rolling_max = prices.rolling(window=window).max()
        
        # Find local minima and maxima
        local_mins = prices[(prices == rolling_min) & (prices.shift(1) > prices) & (prices.shift(-1) > prices)]
        local_maxs = prices[(prices == rolling_max) & (prices.shift(1) < prices) & (prices.shift(-1) < prices)]
        
        return {
            'support_levels': local_mins.tolist()[-5:] if len(local_mins) > 0 else [],  # Last 5 support levels
            'resistance_levels': local_maxs.tolist()[-5:] if len(local_maxs) > 0 else [],  # Last 5 resistance levels
            'current_support': local_mins.iloc[-1] if len(local_mins) > 0 else None,
            'current_resistance': local_maxs.iloc[-1] if len(local_maxs) > 0 else None
        }
    
    def analyze_seasonality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze seasonal patterns in price data"""
        data = data.copy()
        data['month'] = data['date'].dt.month
        data['quarter'] = data['date'].dt.quarter
        data['day_of_week'] = data['date'].dt.dayofweek
        
        # Monthly patterns
        monthly_avg = data.groupby('month')['price'].mean()
        monthly_std = data.groupby('month')['price'].std()
        
        # Quarterly patterns
        quarterly_avg = data.groupby('quarter')['price'].mean()
        
        # Day of week patterns
        dow_avg = data.groupby('day_of_week')['price'].mean()
        
        return {
            'monthly_patterns': {
                'averages': monthly_avg.to_dict(),
                'volatility': monthly_std.to_dict(),
                'best_month': monthly_avg.idxmax(),
                'worst_month': monthly_avg.idxmin()
            },
            'quarterly_patterns': {
                'averages': quarterly_avg.to_dict(),
                'best_quarter': quarterly_avg.idxmax(),
                'worst_quarter': quarterly_avg.idxmin()
            },
            'day_of_week_patterns': {
                'averages': dow_avg.to_dict(),
                'best_day': dow_avg.idxmax(),
                'worst_day': dow_avg.idxmin()
            }
        }
    
    def calculate_risk_metrics(self, prices: pd.Series) -> Dict[str, Any]:
        """Calculate various risk metrics"""
        returns = prices.pct_change().dropna()
        
        # Value at Risk (VaR) - 95% confidence
        var_95 = returns.quantile(0.05)
        
        # Conditional Value at Risk (CVaR)
        cvar_95 = returns[returns <= var_95].mean()
        
        # Maximum Drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Sharpe Ratio (assuming risk-free rate of 2%)
        risk_free_rate = 0.02 / 252  # Daily risk-free rate
        excess_returns = returns - risk_free_rate
        sharpe_ratio = excess_returns.mean() / returns.std() * np.sqrt(252) if returns.std() != 0 else 0
        
        return {
            'var_95': var_95,
            'cvar_95': cvar_95,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'annualized_volatility': returns.std() * np.sqrt(252)
        }
    
    def simple_forecast(self, prices: pd.Series, periods: int = 30) -> Dict[str, Any]:
        """Simple price forecasting using moving averages and trend"""
        if len(prices) < 10:
            return {'error': 'Insufficient data for forecasting'}
        
        # Simple moving averages
        sma_short = prices.rolling(window=10).mean().iloc[-1]
        sma_long = prices.rolling(window=30).mean().iloc[-1] if len(prices) >= 30 else sma_short
        
        # Trend-based forecast
        trend_info = self.calculate_trend(prices.tail(30))  # Use last 30 periods for trend
        
        current_price = prices.iloc[-1]
        
        # Simple forecast based on trend
        if trend_info['trend'] == 'increasing':
            forecast_direction = 'bullish'
            price_change = abs(trend_info['slope']) * periods
        elif trend_info['trend'] == 'decreasing':
            forecast_direction = 'bearish'
            price_change = -abs(trend_info['slope']) * periods
        else:
            forecast_direction = 'neutral'
            price_change = 0
        
        forecasted_price = current_price + price_change
        
        return {
            'current_price': current_price,
            'forecasted_price': forecasted_price,
            'forecast_direction': forecast_direction,
            'confidence': min(trend_info['r_squared'], 0.8),  # Cap confidence at 80%
            'sma_short': sma_short,
            'sma_long': sma_long,
            'signal': 'buy' if sma_short > sma_long else 'sell' if sma_short < sma_long else 'hold'
        }
    
    def compare_commodities(self, data: pd.DataFrame, commodities: List[str]) -> Dict[str, Any]:
        """Compare multiple commodities"""
        if 'commodity' not in data.columns:
            return {'error': 'Commodity column required for comparison'}
        
        comparison_results = {}
        
        for commodity in commodities:
            commodity_data = data[data['commodity'] == commodity]
            if len(commodity_data) > 0:
                analysis = self.analyze(commodity_data, commodity)
                comparison_results[commodity] = {
                    'current_price': commodity_data['price'].iloc[-1] if len(commodity_data) > 0 else None,
                    'volatility': analysis.get('volatility', {}).get('daily', 0),
                    'trend': analysis.get('trend', {}).get('trend', 'unknown'),
                    'performance_1m': self.calculate_performance(commodity_data, 30),
                    'performance_3m': self.calculate_performance(commodity_data, 90),
                    'performance_1y': self.calculate_performance(commodity_data, 365)
                }
        
        return comparison_results
    
    def calculate_performance(self, data: pd.DataFrame, days: int) -> Optional[float]:
        """Calculate performance over specified number of days"""
        if len(data) < days:
            return None
        
        data_sorted = data.sort_values('date')
        current_price = data_sorted['price'].iloc[-1]
        past_price = data_sorted['price'].iloc[-days]
        
        return (current_price - past_price) / past_price * 100

