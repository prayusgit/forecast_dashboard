"""
Configuration settings for LLM integration
"""
import os
from typing import Dict, Any

class LLMConfig:
    """Configuration for LLM services"""
    
    # Google Gemini Configuration
    # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    # GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    # GEMINI_API_KEY="AIzaSyAf5c_pZOLdR_rxtuJLdX_-yiarMXT9234"
    GEMINI_API_KEY="YOUR API KEY"
    GEMINI_MODEL="gemini-1.5-flash"
    
    # Hugging Face Configuration (Fallback)
    # HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
    # HF_MODEL = os.getenv("HF_MODEL", "microsoft/DialoGPT-medium")
    
    # HF_API_TOKEN="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"
    # HF_MODEL="microsoft/DialoGPT-medium"


    # Insight Generation Settings
    MAX_TOKENS = 500
    TEMPERATURE = 0.4   # 0.4-0.6 banalced and good for reports, explaination and business insights
    # User Persona Templates
    USER_PERSONAS = {
        "executive": {
            "focus": "business impact, revenue, strategic decisions",
            "language": "professional, business-oriented",
            "metrics": ["revenue", "growth", "market_share"]
        },
        "marketing": {
            "focus": "customer behavior, campaigns, engagement",
            "language": "marketing-focused, customer-centric",
            "metrics": ["user_engagement", "campaign_performance", "customer_behavior"]
        },
        "engineering": {
            "focus": "technical metrics, system performance, model accuracy",
            "language": "technical, data-driven",
            "metrics": ["model_accuracy", "system_performance", "technical_metrics"]
        },
        "non-tech": {
            "focus": "simple explanations, business outcomes, actionable insights",
            "language": "simple, non-technical",
            "metrics": ["business_outcomes", "simple_metrics", "actionable_insights"]
        }
    }
    
    # Prompt Templates for transaction amount/volume
    PROMPT_TEMPLATES_VOLUME = {
        "executive": """
        You are an AI analyst for eSewa transaction data. Generate executive-level insights.
        
        Focus on: Business impact, revenue implications, strategic decisions, market trends.
        Language: Professional, business-oriented, concise.
        
        Data Context:
        {data_context}
        
        Generate only one key insights that would be valuable for executive decision-making.
        """,
        "marketing": """
        You are an AI analyst for eSewa transaction data. Generate marketing-focused insights.
        
        Focus on: Customer behavior, campaign opportunities, user engagement, market segments.
        Language: Marketing-focused, customer-centric, actionable.
        
        Data Context:
        {data_context}
        
        Generate only one insights that would help marketing teams understand customer behavior and plan campaigns.
        """,
        "engineering": """
        You are an AI analyst for eSewa transaction data. Generate technical insights.
        
        Focus on: Model performance, system metrics, technical accuracy, data quality.
        Language: Technical, data-driven, precise.
        
        Data Context:
        {data_context}
        
        Generate only one technical insights about model performance and system metrics.
        """,
        "non-tech": """
        You are an AI analyst for eSewa transaction data. Generate simple, non-technical insights.
        
        Focus on: Simple explanations, business outcomes, actionable insights.
        Language: Simple, clear, avoid technical jargon.
        
        Data Context:
        {data_context}
        
        Generate only one simple insight that anyone can understand and act upon.
        """
    }

    # Prompt Templates for transaction count/volume (traffic/flow)
    PROMPT_TEMPLATES_COUNT = {
        "executive": """
        You are an AI analyst for eSewa transaction data. Generate executive-level insights focused on transaction count.
        
        Focus on: Business impact, operational efficiency, strategic decisions based on transaction volume trends.
        Language: Professional, business-oriented, concise.
        
        Data Context:
        {data_context}
        
        Generate only one key insights about transaction count that would be valuable for executive decision-making.
        """,
        "marketing": """
        You are an AI analyst for eSewa transaction data. Generate marketing-focused insights focused on transaction count.
        
        Focus on: Customer engagement, campaign opportunities, user activity patterns, and market segments based on transaction count.
        Language: Marketing-focused, customer-centric, actionable.
        
        Data Context:
        {data_context}
        
        Generate only one insights that would help marketing teams understand customer activity and plan campaigns based on transaction count.
        """,
        "engineering": """
        You are an AI analyst for eSewa transaction data. Generate technical insights focused on transaction count.
        
        Focus on: Server load, system performance, peak transaction periods, and technical risks due to high transaction count.
        Language: Technical, data-driven, precise.
        
        Data Context:
        {data_context}
        
        Generate only one technical insights about server load, system performance, and risks related to transaction count.
        """,
        "non-tech": """
        You are an AI analyst for eSewa transaction data. Generate simple, non-technical insights focused on transaction count.
        
        Focus on: Simple explanations, business outcomes, and actionable insights related to transaction count.
        Language: Simple, clear, avoid technical jargon.
        
        Data Context:
        {data_context}
        
        Generate only one simple insight about transaction count that anyone can understand and act upon.
        """
    } 