"""
Data processor for preparing transaction data for LLM insights
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime, timedelta

class DataProcessor:
    """Process transaction data for LLM insight generation"""
    
    def __init__(self):
        pass
    
    def prepare_data_for_insights(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare transaction data for LLM insight generation
        
        Args:
            transaction_data: Raw transaction data and metrics
            
        Returns:
            Processed data ready for LLM prompts
        """
        processed_data = {
            "metrics": {},
            "comparisons": {},
            "trends": [],
            "events": [],
            "anomalies": [],
            "recommendations": []
        }
        
        # Extract and process metrics
        if "metrics" in transaction_data:
            processed_data["metrics"] = self._process_metrics(transaction_data["metrics"])
        
        # Process predictions vs actuals
        if "predictions" in transaction_data and "actuals" in transaction_data:
            processed_data["comparisons"] = self._process_comparisons(
                transaction_data["predictions"], 
                transaction_data["actuals"]
            )
        
        # Analyze trends
        if "historical_data" in transaction_data:
            processed_data["trends"] = self._analyze_trends(transaction_data["historical_data"])
        
        # Process calendar events
        if "calendar_events" in transaction_data:
            processed_data["events"] = self._process_events(transaction_data["calendar_events"])
        
        # Detect anomalies
        if "metrics" in transaction_data:
            processed_data["anomalies"] = self._detect_anomalies(transaction_data["metrics"])
        
        # Generate recommendations
        processed_data["recommendations"] = self._generate_recommendations(processed_data)
        
        return processed_data
    
    def _process_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Process and format metrics for insights"""
        processed_metrics = {}
        
        # Format numerical values
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                if value > 1000000:
                    processed_metrics[key] = f"{value/1000000:.1f}M"
                elif value > 1000:
                    processed_metrics[key] = f"{value/1000:.1f}K"
                else:
                    processed_metrics[key] = f"{value:,.0f}"
            else:
                processed_metrics[key] = str(value)
        
        return processed_metrics
    
    def _process_comparisons(self, predictions: Dict[str, Any], actuals: Dict[str, Any]) -> Dict[str, Any]:
        """Process prediction vs actual comparisons"""
        comparisons = {}
        
        for key in predictions.keys():
            if key in actuals:
                pred_val = predictions[key]
                actual_val = actuals[key]
                
                if isinstance(pred_val, (int, float)) and isinstance(actual_val, (int, float)):
                    if actual_val != 0:
                        error_pct = ((actual_val - pred_val) / actual_val) * 100
                        comparisons[f"{key}_error"] = f"{error_pct:+.1f}%"
                        comparisons[f"{key}_predicted"] = f"{pred_val:,.0f}"
                        comparisons[f"{key}_actual"] = f"{actual_val:,.0f}"
        
        return comparisons
    
    def _analyze_trends(self, historical_data: List[Dict[str, Any]]) -> List[str]:
        """Analyze trends in historical data"""
        trends = []
        
        if len(historical_data) < 2:
            return trends
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(historical_data)
        
        # Analyze transaction volume trends
        if "transaction_amount" in df.columns:
            recent_avg = df["transaction_amount"].tail(7).mean()
            previous_avg = df["transaction_amount"].tail(14).head(7).mean()
            
            if recent_avg > previous_avg * 1.1:
                trends.append("Transaction volume is increasing over the past week")
            elif recent_avg < previous_avg * 0.9:
                trends.append("Transaction volume is decreasing over the past week")
            else:
                trends.append("Transaction volume is stable")
        
        # Analyze category performance
        if "category" in df.columns and "transaction_amount" in df.columns:
            category_performance = df.groupby("category")["transaction_amount"].sum().sort_values(ascending=False)
            top_category = category_performance.index[0]
            trends.append(f"Top performing category is {top_category}")
        
        return trends
    
    def _process_events(self, events: List[Dict[str, Any]]) -> List[str]:
        """Process calendar events for insights"""
        processed_events = []
        
        for event in events:
            if event.get("is_festival"):
                processed_events.append(f"Festival: {event.get('event_name', 'Unknown')}")
            elif event.get("is_holiday"):
                processed_events.append(f"Holiday: {event.get('event_name', 'Public Holiday')}")
            elif event.get("specialday"):
                processed_events.append(f"Special Day: {event.get('event_name', 'Special Event')}")
        
        return processed_events
    
    def _detect_anomalies(self, metrics: Dict[str, Any]) -> List[str]:
        """Detect anomalies in metrics"""
        anomalies = []
        
        # Example anomaly detection logic
        if "prediction_error" in metrics:
            error_val = float(metrics["prediction_error"].replace("%", ""))
            if abs(error_val) > 15:
                anomalies.append(f"High prediction error: {error_val}%")
        
        if "transaction_count" in metrics:
            count_val = int(metrics["transaction_count"].replace(",", ""))
            if count_val < 1000:
                anomalies.append("Low transaction volume detected")
            elif count_val > 50000:
                anomalies.append("Unusually high transaction volume")
        
        return anomalies
    
    def _generate_recommendations(self, processed_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on processed data"""
        recommendations = []
        
        # Recommendations based on anomalies
        if processed_data["anomalies"]:
            recommendations.append("Investigate anomalies in transaction patterns")
        
        # Recommendations based on trends
        if any("decreasing" in trend for trend in processed_data["trends"]):
            recommendations.append("Consider promotional campaigns to boost declining categories")
        
        # Recommendations based on events
        if processed_data["events"]:
            recommendations.append("Prepare for upcoming events that may affect transaction patterns")
        
        # Recommendations based on prediction errors
        if any("error" in key for key in processed_data["comparisons"].keys()):
            recommendations.append("Review and potentially retrain prediction models")
        
        return recommendations
    
    def calculate_insight_metrics(self, transaction_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate metrics specifically for insight generation
        
        Args:
            transaction_df: Transaction DataFrame
            
        Returns:
            Dictionary of calculated metrics
        """
        metrics = {}
        
        if transaction_df.empty:
            return metrics
        
        # Basic metrics
        metrics["total_transactions"] = len(transaction_df)
        metrics["total_amount"] = transaction_df["amount"].sum()
        metrics["avg_transaction_amount"] = transaction_df["amount"].mean()
        
        # Category metrics
        if "category" in transaction_df.columns:
            category_stats = transaction_df.groupby("category").agg({
                "amount": ["sum", "count", "mean"]
            }).round(2)
            
            metrics["top_category"] = category_stats["amount"]["sum"].idxmax()
            metrics["top_category_amount"] = category_stats["amount"]["sum"].max()
            metrics["category_count"] = len(category_stats)
        
        # Time-based metrics
        if "transaction_date" in transaction_df.columns:
            transaction_df["transaction_date"] = pd.to_datetime(transaction_df["transaction_date"])
            
            # Recent vs previous period comparison
            recent_date = transaction_df["transaction_date"].max()
            week_ago = recent_date - timedelta(days=7)
            
            recent_data = transaction_df[transaction_df["transaction_date"] >= week_ago]
            previous_data = transaction_df[
                (transaction_df["transaction_date"] >= week_ago - timedelta(days=7)) &
                (transaction_df["transaction_date"] < week_ago)
            ]
            
            if not previous_data.empty and not recent_data.empty:
                recent_avg = recent_data["amount"].mean()
                previous_avg = previous_data["amount"].mean()
                
                if previous_avg != 0:
                    growth_rate = ((recent_avg - previous_avg) / previous_avg) * 100
                    metrics["week_over_week_growth"] = f"{growth_rate:+.1f}%"
        
        # Event metrics
        if "is_festival" in transaction_df.columns:
            festival_transactions = transaction_df[transaction_df["is_festival"] == True]
            metrics["festival_transactions"] = len(festival_transactions)
            metrics["festival_amount"] = festival_transactions["amount"].sum()
        
        return metrics 