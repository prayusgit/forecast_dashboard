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
   
    GEMINI_API_KEY="YOUR_API_KEY"
    GEMINI_MODEL="gemini-1.5-flash"

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
        You are an AI analyst for eSewa transaction data(amount in NPR and mention name of the category/product). Generate a clean and concise executive-level insights.
        
        Focus on: Business impact, revenue implications, strategic decisions, market trends.
        Language: Professional, business-oriented, concise.
        
        Data Context:
        {data_context}
        
        Generate only one key insights that would be valuable for executive decision-making.
        """,
        "marketing": """
        You are an AI analyst for eSewa transaction data(amount in NPR and mention name of the category/product). Generate a clean and concise marketing-focused insights.
        
        Focus on: Customer behavior, campaign opportunities, user engagement, market segments.
        Language: Marketing-focused, customer-centric, actionable.
        
        Data Context:
        {data_context}
        
        Generate only one insights that would help marketing teams understand customer behavior and plan campaigns.
        """,
        "engineering": """
        You are an AI analyst for eSewa transaction data(amount in NPR and mention name of the category/product). Generatea clean and concise technical insights.
        
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
        You are an AI analyst for eSewa transaction data(amount in NPR and mention name of the category/product). Generatea clean and concise  executive-level insights focused on transaction count.
        
        Focus on: Business impact, operational efficiency, strategic decisions based on transaction volume trends.
        Language: Professional, business-oriented, concise.
        
        Data Context:
        {data_context}
        
        Generate only one key insights about transaction count that would be valuable for executive decision-making.
        """,
        "marketing": """
        You are an AI analyst for eSewa transaction data(amount in NPR and mention name of the category/product). Generatea clean and concise  marketing-focused insights focused on transaction count.
        
        Focus on: Customer engagement, campaign opportunities, user activity patterns, and market segments based on transaction count.
        Language: Marketing-focused, customer-centric, actionable.
        
        Data Context:
        {data_context}
        
        Generate only one insights that would help marketing teams understand customer activity and plan campaigns based on transaction count.
        """,
        "engineering": """
        You are an AI analyst for eSewa transaction data(amount in NPR and mention name of the category/product). Generate a clean and concise technical insights focused on transaction count.
        
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

    # Prompt Templates for product-specific insights within categories
    PROMPT_TEMPLATES_PRODUCT = {
        "executive": """
        You are an AI analyst for eSewa transaction data(amount in NPR and mention name of the category/product). Generate a clean and concise executive-level insights focused on specific product performance within a category.
        
        Focus on: Product profitability, market positioning, competitive analysis, strategic product decisions, revenue contribution by product.
        Language: Professional, business-oriented, strategic.
        
        Data Context:
        {data_context}
        
        Generate only one key insight about the specific product's performance that would be valuable for executive decision-making and strategic planning.
        """,

        "marketing": """
        You are an AI analyst for eSewa transaction data(amount in NPR and mention name of the category/product). Generate a clean and concise marketing-focused insights focused on specific product performance within a category.
        
        Focus on: Product-specific customer behavior, targeted marketing opportunities, product positioning, customer preferences, cross-selling potential.
        Language: Marketing-focused, customer-centric, actionable.
        
        Data Context:
        {data_context}
        
        Generate only one insight that would help marketing teams understand product-specific customer behavior and plan targeted campaigns.
        """,

        "engineering": """
        You are an AI analyst for eSewa transaction data(amount in NPR and mention name of the category/product). Generate a clean and concise technical insights focused on specific product performance within a category.
        
        Focus on: Product-specific system performance, technical scalability, data processing requirements, product-specific model accuracy, technical risks.
        Language: Technical, data-driven, precise.
        
        Data Context:
        {data_context}
        
        Generate only one technical insight about system performance, scalability, and technical considerations specific to this product.
        """,

        "non-tech": """
        You are an AI analyst for eSewa transaction data. Generate simple, non-technical insights focused on specific product performance within a category.
        
        Focus on: Simple product performance explanations, business outcomes, customer satisfaction, actionable product insights.
        Language: Simple, clear, avoid technical jargon.
        
        Data Context:
        {data_context}
        
        Generate only one simple insight about the specific product's performance that anyone can understand and act upon.
        """
    } 