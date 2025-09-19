import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

from .price_analyzer import PriceAnalyzer
from .production_analyzer import ProductionAnalyzer
from .ml_predictor import MLPredictor
from ..models.user import db
from ..models.commodity import Commodity
from ..models.country import Country
from ..models.production_data import ProductionData
from ..models.reserves_data import ReservesData
from ..models.price_data import PriceData

class AnalyticsService:
    """Service to orchestrate all analytics modules"""
    
    def __init__(self, app=None):
        self.app = app
        self.logger = logging.getLogger(__name__)
        
        # Initialize analyzers
        self.analyzers = {
            'price': PriceAnalyzer(),
            'production': ProductionAnalyzer(),
            'ml': MLPredictor()
        }
        
        # Analysis cache
        self.analysis_cache = {}
        self.cache_ttl = 3600  # 1 hour cache TTL
    
    def analyze_commodity(self, commodity_id: int, analysis_types: List[str] = None) -> Dict[str, Any]:
        """
        Perform comprehensive analysis for a commodity
        
        Args:
            commodity_id: ID of the commodity to analyze
            analysis_types: List of analysis types to perform ['price', 'production', 'ml']
        """
        if analysis_types is None:
            analysis_types = ['price', 'production', 'ml']
        
        with self.app.app_context():
            # Get commodity info
            commodity = Commodity.query.get(commodity_id)
            if not commodity:
                return {'error': f'Commodity with ID {commodity_id} not found'}
            
            results = {
                'commodity': commodity.to_dict(),
                'analysis_date': datetime.utcnow().isoformat(),
                'analyses': {}
            }
            
            # Perform each requested analysis
            for analysis_type in analysis_types:
                if analysis_type in self.analyzers:
                    try:
                        analysis_result = self._perform_analysis(commodity_id, analysis_type)
                        results['analyses'][analysis_type] = analysis_result
                    except Exception as e:
                        self.logger.error(f"Error in {analysis_type} analysis: {e}")
                        results['analyses'][analysis_type] = {'error': str(e)}
                else:
                    results['analyses'][analysis_type] = {'error': f'Unknown analysis type: {analysis_type}'}
            
            # Generate comprehensive summary
            results['summary'] = self._generate_comprehensive_summary(results['analyses'], commodity.name)
            
            return results
    
    def _perform_analysis(self, commodity_id: int, analysis_type: str) -> Dict[str, Any]:
        """Perform a specific type of analysis"""
        # Check cache first
        cache_key = f"{commodity_id}_{analysis_type}"
        if cache_key in self.analysis_cache:
            cached_result, timestamp = self.analysis_cache[cache_key]
            if (datetime.utcnow() - timestamp).seconds < self.cache_ttl:
                return cached_result
        
        # Get data based on analysis type
        if analysis_type == 'price':
            data = self._get_price_data(commodity_id)
            analyzer = self.analyzers['price']
        elif analysis_type == 'production':
            data = self._get_production_data(commodity_id)
            analyzer = self.analyzers['production']
        elif analysis_type == 'ml':
            data = self._get_price_data(commodity_id)  # Use price data for ML
            analyzer = self.analyzers['ml']
        else:
            return {'error': f'Unknown analysis type: {analysis_type}'}
        
        if data.empty:
            return {'error': f'No data available for {analysis_type} analysis'}
        
        # Perform analysis
        result = analyzer.analyze(data)
        
        # Cache result
        self.analysis_cache[cache_key] = (result, datetime.utcnow())
        
        return result
    
    def _get_price_data(self, commodity_id: int) -> pd.DataFrame:
        """Get price data for a commodity"""
        price_records = PriceData.query.filter_by(commodity_id=commodity_id).order_by(PriceData.timestamp).all()
        
        if not price_records:
            return pd.DataFrame()
        
        data = []
        for record in price_records:
            data.append({
                'date': record.timestamp,
                'price': float(record.price) if record.price else None,
                'currency': record.currency,
                'volume': float(record.volume) if record.volume else None,
                'commodity_id': record.commodity_id
            })
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df.dropna(subset=['price'])
    
    def _get_production_data(self, commodity_id: int) -> pd.DataFrame:
        """Get production data for a commodity"""
        production_records = (ProductionData.query
                            .filter_by(commodity_id=commodity_id)
                            .join(Country)
                            .order_by(ProductionData.year)
                            .all())
        
        if not production_records:
            return pd.DataFrame()
        
        data = []
        for record in production_records:
            data.append({
                'year': record.year,
                'production_volume': float(record.production_volume) if record.production_volume else None,
                'unit': record.unit,
                'country': record.country.name if record.country else 'Unknown',
                'commodity_id': record.commodity_id
            })
        
        df = pd.DataFrame(data)
        return df.dropna(subset=['production_volume'])
    
    def _generate_comprehensive_summary(self, analyses: Dict[str, Any], commodity_name: str) -> Dict[str, Any]:
        """Generate a comprehensive summary of all analyses"""
        summary = {
            'commodity': commodity_name,
            'overall_assessment': 'Unknown',
            'key_insights': [],
            'risk_level': 'Unknown',
            'investment_outlook': 'Unknown',
            'confidence_score': 0
        }
        
        insights = []
        risk_factors = []
        confidence_scores = []
        
        # Extract insights from price analysis
        if 'price' in analyses and 'error' not in analyses['price']:
            price_analysis = analyses['price']
            
            # Price trend insight
            trend = price_analysis.get('trend', {})
            if trend.get('trend') == 'increasing':
                insights.append(f"{commodity_name} prices show an upward trend")
            elif trend.get('trend') == 'decreasing':
                insights.append(f"{commodity_name} prices show a downward trend")
                risk_factors.append('Declining price trend')
            
            # Volatility insight
            volatility = price_analysis.get('volatility', {})
            daily_vol = volatility.get('daily', 0)
            if daily_vol > 0.05:  # 5% daily volatility threshold
                insights.append(f"{commodity_name} shows high price volatility")
                risk_factors.append('High price volatility')
            
            # Risk metrics
            risk_metrics = price_analysis.get('risk_metrics', {})
            max_drawdown = risk_metrics.get('max_drawdown', 0)
            if max_drawdown < -0.2:  # 20% drawdown threshold
                risk_factors.append('Significant historical drawdowns')
            
            confidence_scores.append(0.8)  # Price analysis confidence
        
        # Extract insights from production analysis
        if 'production' in analyses and 'error' not in analyses['production']:
            production_analysis = analyses['production']
            
            # Production trend
            trend = production_analysis.get('trend', {})
            if trend.get('trend') == 'increasing':
                insights.append(f"{commodity_name} production is growing")
            elif trend.get('trend') == 'decreasing':
                insights.append(f"{commodity_name} production is declining")
                risk_factors.append('Declining production')
            
            # Supply risk
            supply_risk = production_analysis.get('supply_risk', {})
            overall_risk = supply_risk.get('overall_risk', 'Unknown')
            if overall_risk == 'High':
                risk_factors.append('High supply risk')
                insights.append(f"{commodity_name} has high supply risk")
            
            # Concentration risk
            concentration = production_analysis.get('concentration', {})
            if concentration.get('concentration_level') == 'High':
                risk_factors.append('High production concentration')
            
            confidence_scores.append(0.7)  # Production analysis confidence
        
        # Extract insights from ML analysis
        if 'ml' in analyses and 'error' not in analyses['ml']:
            ml_analysis = analyses['ml']
            
            # Model performance
            model_summary = ml_analysis.get('model_summary', {})
            performance_level = model_summary.get('performance_level', 'Unknown')
            
            if performance_level in ['Excellent', 'Good']:
                insights.append(f"ML models show {performance_level.lower()} predictive performance")
                confidence_scores.append(0.9)
            else:
                insights.append("ML predictions have limited reliability")
                confidence_scores.append(0.4)
            
            # Predictions
            predictions = ml_analysis.get('predictions', {})
            if predictions and 'predictions' in predictions:
                pred_list = predictions['predictions']
                if len(pred_list) > 0:
                    current_vs_future = pred_list[0] / pred_list[-1] if pred_list[-1] != 0 else 1
                    if current_vs_future > 1.1:
                        insights.append("ML models predict price increases")
                    elif current_vs_future < 0.9:
                        insights.append("ML models predict price decreases")
        
        # Determine overall assessment
        if len(risk_factors) == 0:
            overall_assessment = 'Positive'
            investment_outlook = 'Favorable'
        elif len(risk_factors) <= 2:
            overall_assessment = 'Neutral'
            investment_outlook = 'Cautious'
        else:
            overall_assessment = 'Negative'
            investment_outlook = 'Unfavorable'
        
        # Determine risk level
        if len(risk_factors) == 0:
            risk_level = 'Low'
        elif len(risk_factors) <= 2:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        # Calculate overall confidence
        overall_confidence = np.mean(confidence_scores) if confidence_scores else 0
        
        summary.update({
            'overall_assessment': overall_assessment,
            'key_insights': insights,
            'risk_factors': risk_factors,
            'risk_level': risk_level,
            'investment_outlook': investment_outlook,
            'confidence_score': round(overall_confidence, 2)
        })
        
        return summary
    
    def compare_commodities(self, commodity_ids: List[int], analysis_type: str = 'price') -> Dict[str, Any]:
        """Compare multiple commodities"""
        with self.app.app_context():
            comparison_results = {}
            
            for commodity_id in commodity_ids:
                commodity = Commodity.query.get(commodity_id)
                if commodity:
                    analysis = self._perform_analysis(commodity_id, analysis_type)
                    comparison_results[commodity.name] = {
                        'commodity_id': commodity_id,
                        'analysis': analysis
                    }
            
            # Generate comparison summary
            comparison_summary = self._generate_comparison_summary(comparison_results, analysis_type)
            
            return {
                'comparison_type': analysis_type,
                'commodities': comparison_results,
                'summary': comparison_summary,
                'analysis_date': datetime.utcnow().isoformat()
            }
    
    def _generate_comparison_summary(self, comparison_results: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """Generate a summary comparing multiple commodities"""
        summary = {
            'best_performer': None,
            'worst_performer': None,
            'most_volatile': None,
            'least_volatile': None,
            'rankings': []
        }
        
        if analysis_type == 'price':
            # Compare based on price performance and volatility
            performance_scores = {}
            volatility_scores = {}
            
            for commodity_name, data in comparison_results.items():
                analysis = data.get('analysis', {})
                
                # Get trend score
                trend = analysis.get('trend', {})
                if trend.get('trend') == 'increasing':
                    trend_score = 1
                elif trend.get('trend') == 'decreasing':
                    trend_score = -1
                else:
                    trend_score = 0
                
                # Get volatility
                volatility = analysis.get('volatility', {}).get('daily', 0)
                
                performance_scores[commodity_name] = trend_score
                volatility_scores[commodity_name] = volatility
            
            # Find best/worst performers
            if performance_scores:
                summary['best_performer'] = max(performance_scores.keys(), key=lambda k: performance_scores[k])
                summary['worst_performer'] = min(performance_scores.keys(), key=lambda k: performance_scores[k])
            
            if volatility_scores:
                summary['most_volatile'] = max(volatility_scores.keys(), key=lambda k: volatility_scores[k])
                summary['least_volatile'] = min(volatility_scores.keys(), key=lambda k: volatility_scores[k])
            
            # Create rankings
            rankings = []
            for commodity_name in performance_scores.keys():
                rankings.append({
                    'commodity': commodity_name,
                    'performance_score': performance_scores[commodity_name],
                    'volatility': volatility_scores.get(commodity_name, 0)
                })
            
            # Sort by performance score
            rankings.sort(key=lambda x: x['performance_score'], reverse=True)
            summary['rankings'] = rankings
        
        return summary
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Get an overview of the entire market"""
        with self.app.app_context():
            # Get all commodities
            commodities = Commodity.query.all()
            
            overview = {
                'total_commodities': len(commodities),
                'analysis_date': datetime.utcnow().isoformat(),
                'market_summary': {},
                'top_performers': [],
                'risk_alerts': []
            }
            
            # Analyze each commodity briefly
            commodity_summaries = []
            
            for commodity in commodities[:10]:  # Limit to first 10 for performance
                try:
                    analysis = self.analyze_commodity(commodity.id, ['price'])
                    summary = analysis.get('summary', {})
                    
                    commodity_summaries.append({
                        'name': commodity.name,
                        'assessment': summary.get('overall_assessment', 'Unknown'),
                        'risk_level': summary.get('risk_level', 'Unknown'),
                        'confidence': summary.get('confidence_score', 0)
                    })
                    
                    # Collect risk alerts
                    if summary.get('risk_level') == 'High':
                        overview['risk_alerts'].append(f"{commodity.name}: High risk detected")
                
                except Exception as e:
                    self.logger.error(f"Error analyzing commodity {commodity.name}: {e}")
            
            # Generate market summary
            if commodity_summaries:
                positive_count = sum(1 for c in commodity_summaries if c['assessment'] == 'Positive')
                negative_count = sum(1 for c in commodity_summaries if c['assessment'] == 'Negative')
                high_risk_count = sum(1 for c in commodity_summaries if c['risk_level'] == 'High')
                
                overview['market_summary'] = {
                    'positive_outlook': positive_count,
                    'negative_outlook': negative_count,
                    'neutral_outlook': len(commodity_summaries) - positive_count - negative_count,
                    'high_risk_commodities': high_risk_count,
                    'market_sentiment': 'Positive' if positive_count > negative_count else 'Negative' if negative_count > positive_count else 'Mixed'
                }
                
                # Top performers
                overview['top_performers'] = sorted(commodity_summaries, 
                                                  key=lambda x: x['confidence'], 
                                                  reverse=True)[:5]
            
            return overview
    
    def clear_cache(self):
        """Clear the analysis cache"""
        self.analysis_cache.clear()
        self.logger.info("Analysis cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'cache_size': len(self.analysis_cache),
            'cache_ttl': self.cache_ttl,
            'cached_analyses': list(self.analysis_cache.keys())
        }

