import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging

class BaseAnalyzer(ABC):
    """Base class for all analytics modules"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"analytics.{name}")
        
    @abstractmethod
    def analyze(self, data: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """Perform analysis on the provided data"""
        pass
    
    def validate_data(self, data: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate that data contains required columns"""
        missing_columns = set(required_columns) - set(data.columns)
        if missing_columns:
            self.logger.error(f"Missing required columns: {missing_columns}")
            return False
        return True
    
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare data for analysis"""
        # Remove rows with all NaN values
        data = data.dropna(how='all')
        
        # Convert date columns if they exist
        date_columns = ['date', 'timestamp', 'year']
        for col in date_columns:
            if col in data.columns:
                data[col] = pd.to_datetime(data[col], errors='coerce')
        
        return data
    
    def calculate_statistics(self, series: pd.Series) -> Dict[str, float]:
        """Calculate basic statistics for a data series"""
        return {
            'mean': series.mean(),
            'median': series.median(),
            'std': series.std(),
            'min': series.min(),
            'max': series.max(),
            'count': len(series),
            'null_count': series.isnull().sum()
        }
    
    def detect_outliers(self, series: pd.Series, method: str = 'iqr') -> pd.Series:
        """Detect outliers in a data series"""
        if method == 'iqr':
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (series < lower_bound) | (series > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((series - series.mean()) / series.std())
            return z_scores > 3
        
        else:
            raise ValueError(f"Unknown outlier detection method: {method}")
    
    def calculate_trend(self, series: pd.Series, periods: int = None) -> Dict[str, Any]:
        """Calculate trend information for a time series"""
        if periods is None:
            periods = min(len(series), 12)  # Default to 12 periods
        
        if len(series) < 2:
            return {'trend': 'insufficient_data', 'slope': 0, 'r_squared': 0}
        
        # Simple linear regression for trend
        x = np.arange(len(series))
        y = series.values
        
        # Remove NaN values
        mask = ~np.isnan(y)
        if mask.sum() < 2:
            return {'trend': 'insufficient_data', 'slope': 0, 'r_squared': 0}
        
        x_clean = x[mask]
        y_clean = y[mask]
        
        # Calculate slope and R-squared
        slope, intercept = np.polyfit(x_clean, y_clean, 1)
        y_pred = slope * x_clean + intercept
        ss_res = np.sum((y_clean - y_pred) ** 2)
        ss_tot = np.sum((y_clean - np.mean(y_clean)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Determine trend direction
        if abs(slope) < 0.01:  # Threshold for "flat" trend
            trend = 'stable'
        elif slope > 0:
            trend = 'increasing'
        else:
            trend = 'decreasing'
        
        return {
            'trend': trend,
            'slope': slope,
            'r_squared': r_squared,
            'periods_analyzed': len(x_clean)
        }
    
    def calculate_volatility(self, series: pd.Series, window: int = 30) -> float:
        """Calculate volatility (rolling standard deviation)"""
        if len(series) < window:
            return series.std()
        
        rolling_std = series.rolling(window=window).std()
        return rolling_std.mean()
    
    def generate_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a human-readable summary of analysis results"""
        summary_parts = [f"Analysis: {self.name}"]
        
        # Add key findings
        if 'statistics' in analysis_results:
            stats = analysis_results['statistics']
            summary_parts.append(f"Mean: {stats.get('mean', 'N/A'):.2f}")
            summary_parts.append(f"Trend: {analysis_results.get('trend', {}).get('trend', 'N/A')}")
        
        return " | ".join(summary_parts)

