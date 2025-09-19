import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

from .base_analyzer import BaseAnalyzer

class MLPredictor(BaseAnalyzer):
    """Machine Learning predictor for commodity data"""
    
    def __init__(self):
        super().__init__("MLPredictor")
        self.models = {
            'linear': LinearRegression(),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        self.scaler = StandardScaler()
        self.trained_models = {}
        self.feature_importance = {}
    
    def analyze(self, data: pd.DataFrame, target_column: str = 'price', **kwargs) -> Dict[str, Any]:
        """
        Perform ML analysis and prediction
        
        Args:
            data: DataFrame with time series data
            target_column: Column to predict
        """
        if target_column not in data.columns:
            return {'error': f'Target column {target_column} not found in data'}
        
        if len(data) < 20:
            return {'error': 'Insufficient data for ML analysis (minimum 20 records required)'}
        
        # Prepare features
        features_data = self.prepare_features(data, target_column)
        
        if features_data is None:
            return {'error': 'Failed to prepare features'}
        
        X, y = features_data
        
        # Train and evaluate models
        model_results = self.train_and_evaluate_models(X, y)
        
        # Select best model
        best_model_name = max(model_results.keys(), key=lambda k: model_results[k]['r2_score'])
        best_model = self.trained_models[best_model_name]
        
        # Generate predictions
        predictions = self.generate_predictions(data, best_model, target_column)
        
        # Feature importance
        importance = self.get_feature_importance(best_model_name, X.columns)
        
        results = {
            'target_column': target_column,
            'analysis_date': datetime.utcnow().isoformat(),
            'data_points': len(data),
            'best_model': best_model_name,
            'model_performance': model_results,
            'predictions': predictions,
            'feature_importance': importance,
            'model_summary': self.generate_model_summary(model_results, best_model_name)
        }
        
        return results
    
    def prepare_features(self, data: pd.DataFrame, target_column: str) -> Optional[Tuple[pd.DataFrame, pd.Series]]:
        """Prepare features for ML models"""
        try:
            data = data.copy().sort_values('date' if 'date' in data.columns else data.index)
            
            # Create time-based features
            if 'date' in data.columns:
                data['year'] = data['date'].dt.year
                data['month'] = data['date'].dt.month
                data['quarter'] = data['date'].dt.quarter
                data['day_of_year'] = data['date'].dt.dayofyear
            
            # Create lag features
            for lag in [1, 2, 3, 7, 30]:
                if len(data) > lag:
                    data[f'{target_column}_lag_{lag}'] = data[target_column].shift(lag)
            
            # Create rolling statistics
            for window in [7, 30, 90]:
                if len(data) > window:
                    data[f'{target_column}_ma_{window}'] = data[target_column].rolling(window=window).mean()
                    data[f'{target_column}_std_{window}'] = data[target_column].rolling(window=window).std()
            
            # Create technical indicators
            if len(data) > 14:
                # RSI-like indicator
                delta = data[target_column].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                data['rsi'] = 100 - (100 / (1 + rs))
            
            # Create volatility features
            if len(data) > 20:
                data['volatility_20'] = data[target_column].rolling(window=20).std()
            
            # Select feature columns (exclude target and non-numeric columns)
            feature_columns = [col for col in data.columns 
                             if col != target_column 
                             and col not in ['date', 'commodity', 'country']
                             and data[col].dtype in ['int64', 'float64']]
            
            # Remove rows with NaN values
            data_clean = data[feature_columns + [target_column]].dropna()
            
            if len(data_clean) < 10:
                return None
            
            X = data_clean[feature_columns]
            y = data_clean[target_column]
            
            return X, y
            
        except Exception as e:
            self.logger.error(f"Error preparing features: {e}")
            return None
    
    def train_and_evaluate_models(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """Train and evaluate multiple ML models"""
        results = {}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features for linear models
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        for model_name, model in self.models.items():
            try:
                # Use scaled data for linear regression, original for tree-based models
                if model_name == 'linear':
                    X_train_model = X_train_scaled
                    X_test_model = X_test_scaled
                else:
                    X_train_model = X_train
                    X_test_model = X_test
                
                # Train model
                model.fit(X_train_model, y_train)
                self.trained_models[model_name] = model
                
                # Make predictions
                y_pred_train = model.predict(X_train_model)
                y_pred_test = model.predict(X_test_model)
                
                # Calculate metrics
                train_mae = mean_absolute_error(y_train, y_pred_train)
                test_mae = mean_absolute_error(y_test, y_pred_test)
                train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
                test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
                train_r2 = r2_score(y_train, y_pred_train)
                test_r2 = r2_score(y_test, y_pred_test)
                
                # Cross-validation
                cv_scores = cross_val_score(model, X_train_model, y_train, cv=5, scoring='r2')
                
                results[model_name] = {
                    'train_mae': train_mae,
                    'test_mae': test_mae,
                    'train_rmse': train_rmse,
                    'test_rmse': test_rmse,
                    'train_r2': train_r2,
                    'test_r2': test_r2,
                    'r2_score': test_r2,  # Primary metric for model selection
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'overfitting': train_r2 - test_r2  # Measure of overfitting
                }
                
            except Exception as e:
                self.logger.error(f"Error training {model_name}: {e}")
                results[model_name] = {'error': str(e)}
        
        return results
    
    def generate_predictions(self, data: pd.DataFrame, model, target_column: str, 
                           periods_ahead: int = 30) -> Dict[str, Any]:
        """Generate future predictions"""
        try:
            # Prepare the most recent data for prediction
            recent_data = data.tail(100).copy()  # Use last 100 points for context
            
            # Prepare features for the most recent point
            features_data = self.prepare_features(recent_data, target_column)
            if features_data is None:
                return {'error': 'Could not prepare features for prediction'}
            
            X, y = features_data
            
            if len(X) == 0:
                return {'error': 'No valid features for prediction'}
            
            # Get the last valid feature vector
            last_features = X.iloc[-1:].copy()
            
            # Generate predictions for future periods
            predictions = []
            current_features = last_features.copy()
            
            for i in range(periods_ahead):
                # Make prediction
                if hasattr(model, 'predict'):
                    if isinstance(model, LinearRegression):
                        # Use scaled features for linear regression
                        features_scaled = self.scaler.transform(current_features)
                        pred = model.predict(features_scaled)[0]
                    else:
                        pred = model.predict(current_features)[0]
                else:
                    pred = y.iloc[-1]  # Fallback to last known value
                
                predictions.append(pred)
                
                # Update features for next prediction (simple approach)
                # In a more sophisticated model, you would update lag features properly
                if f'{target_column}_lag_1' in current_features.columns:
                    current_features[f'{target_column}_lag_1'] = pred
            
            # Calculate prediction intervals (simple approach using historical volatility)
            historical_volatility = y.std()
            confidence_intervals = []
            
            for i, pred in enumerate(predictions):
                # Increase uncertainty over time
                uncertainty = historical_volatility * np.sqrt(i + 1) * 0.5
                confidence_intervals.append({
                    'lower': pred - 1.96 * uncertainty,
                    'upper': pred + 1.96 * uncertainty
                })
            
            return {
                'predictions': predictions,
                'confidence_intervals': confidence_intervals,
                'prediction_dates': [(datetime.now() + timedelta(days=i+1)).isoformat() 
                                   for i in range(periods_ahead)],
                'historical_volatility': historical_volatility,
                'last_actual_value': float(y.iloc[-1])
            }
            
        except Exception as e:
            self.logger.error(f"Error generating predictions: {e}")
            return {'error': str(e)}
    
    def get_feature_importance(self, model_name: str, feature_names: List[str]) -> Dict[str, float]:
        """Get feature importance from trained model"""
        if model_name not in self.trained_models:
            return {}
        
        model = self.trained_models[model_name]
        
        try:
            if hasattr(model, 'feature_importances_'):
                # Tree-based models
                importance = dict(zip(feature_names, model.feature_importances_))
            elif hasattr(model, 'coef_'):
                # Linear models
                importance = dict(zip(feature_names, np.abs(model.coef_)))
            else:
                return {}
            
            # Sort by importance
            importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
            
            return importance
            
        except Exception as e:
            self.logger.error(f"Error getting feature importance: {e}")
            return {}
    
    def generate_model_summary(self, model_results: Dict[str, Any], best_model: str) -> Dict[str, Any]:
        """Generate a summary of model performance"""
        if best_model not in model_results:
            return {'error': 'Best model not found in results'}
        
        best_performance = model_results[best_model]
        
        # Interpret R² score
        r2 = best_performance.get('test_r2', 0)
        if r2 > 0.8:
            performance_level = 'Excellent'
        elif r2 > 0.6:
            performance_level = 'Good'
        elif r2 > 0.4:
            performance_level = 'Fair'
        else:
            performance_level = 'Poor'
        
        # Check for overfitting
        overfitting = best_performance.get('overfitting', 0)
        if overfitting > 0.2:
            overfitting_level = 'High'
        elif overfitting > 0.1:
            overfitting_level = 'Moderate'
        else:
            overfitting_level = 'Low'
        
        return {
            'best_model': best_model,
            'performance_level': performance_level,
            'r2_score': r2,
            'test_mae': best_performance.get('test_mae', 0),
            'test_rmse': best_performance.get('test_rmse', 0),
            'overfitting_level': overfitting_level,
            'cross_validation_score': best_performance.get('cv_mean', 0),
            'model_reliability': 'High' if r2 > 0.7 and overfitting < 0.1 else 'Medium' if r2 > 0.5 else 'Low'
        }
    
    def predict_price_movements(self, data: pd.DataFrame, target_column: str = 'price') -> Dict[str, Any]:
        """Predict price movement direction (up/down/stable)"""
        try:
            # Prepare data for classification
            data = data.copy().sort_values('date' if 'date' in data.columns else data.index)
            
            # Create target variable (price movement direction)
            data['price_change'] = data[target_column].pct_change()
            data['movement'] = np.where(data['price_change'] > 0.02, 1,  # Up (>2% increase)
                                      np.where(data['price_change'] < -0.02, -1, 0))  # Down (<-2% decrease), else Stable
            
            # Prepare features
            features_data = self.prepare_features(data, target_column)
            if features_data is None:
                return {'error': 'Could not prepare features'}
            
            X, _ = features_data
            y_movement = data['movement'].iloc[X.index]
            
            # Remove NaN values
            valid_idx = ~y_movement.isna()
            X_clean = X[valid_idx]
            y_clean = y_movement[valid_idx]
            
            if len(X_clean) < 10:
                return {'error': 'Insufficient data for movement prediction'}
            
            # Train a simple classifier
            from sklearn.ensemble import RandomForestClassifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.2, random_state=42)
            
            # Train classifier
            classifier.fit(X_train, y_train)
            
            # Evaluate
            train_accuracy = classifier.score(X_train, y_train)
            test_accuracy = classifier.score(X_test, y_test)
            
            # Predict next movement
            last_features = X_clean.iloc[-1:].copy()
            next_movement_prob = classifier.predict_proba(last_features)[0]
            next_movement = classifier.predict(last_features)[0]
            
            movement_labels = {-1: 'Down', 0: 'Stable', 1: 'Up'}
            
            return {
                'next_movement_prediction': movement_labels.get(next_movement, 'Unknown'),
                'movement_probabilities': {
                    'down': next_movement_prob[0] if len(next_movement_prob) > 0 else 0,
                    'stable': next_movement_prob[1] if len(next_movement_prob) > 1 else 0,
                    'up': next_movement_prob[2] if len(next_movement_prob) > 2 else 0
                },
                'model_accuracy': {
                    'train': train_accuracy,
                    'test': test_accuracy
                },
                'confidence': max(next_movement_prob) if len(next_movement_prob) > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting price movements: {e}")
            return {'error': str(e)}

