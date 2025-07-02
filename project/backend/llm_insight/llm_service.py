"""
LLM Service for generating insights using free APIs
"""
import logging
from typing import Dict, Any, List
from datetime import datetime
from .config import LLMConfig
from .data_processor import DataProcessor

logger = logging.getLogger(__name__)

class LLMService:
    """Service for generating insights using free LLM APIs"""
    
    def __init__(self):
        self.config = LLMConfig()
        self.data_processor = DataProcessor()
        self._setup_gemini()
    
    def _setup_gemini(self):
        """Setup Gemini connection"""
        try:
            import google.generativeai as genai
            
            if self.config.GEMINI_API_KEY:
                genai.configure(api_key=self.config.GEMINI_API_KEY)
                # Test the connection
                model = genai.GenerativeModel(self.config.GEMINI_MODEL)
                response = model.generate_content("Test connection")
                if response.text:
                    logger.info("Gemini connection successful")
                    self.gemini_available = True
                else:
                    logger.warning("Gemini not responding properly")
                    self.gemini_available = False
            else:
                logger.warning("Gemini API key not found, will use fallback")
                self.gemini_available = False
                
        except Exception as e:
            logger.warning(f"Gemini setup failed: {e}")
            self.gemini_available = False
    
    def generate_insight_volume(self, user_type: str, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate insights for specific user type (volume/amount)
        """
        try:
            processed_data = self.data_processor.prepare_data_for_insights(transaction_data)
            prompt = self._create_prompt(user_type, processed_data, self.config.PROMPT_TEMPLATES_VOLUME)
            if self.gemini_available:
                insight_text = self._generate_with_gemini(prompt)
            else:
                insight_text = self._generate_with_huggingface(prompt)
            insight = {
                "user_type": user_type,
                "insight_text": insight_text,
                "generated_at": datetime.now().isoformat(),
                "data_context": processed_data,
                "source": "gemini"
            }
            return insight
        except Exception as e:
            logger.error(f"Error generating insight: {e}")
            return self._generate_fallback_insight(user_type, transaction_data)

    def generate_insight_count(self, user_type: str, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate insights for specific user type (count/traffic)
        """
        try:
            processed_data = self.data_processor.prepare_data_for_insights(transaction_data)
            prompt = self._create_prompt(user_type, processed_data, self.config.PROMPT_TEMPLATES_COUNT)
            if self.gemini_available:
                insight_text = self._generate_with_gemini(prompt)
            else:
                insight_text = self._generate_with_huggingface(prompt)
            insight = {
                "user_type": user_type,
                "insight_text": insight_text,
                "generated_at": datetime.now().isoformat(),
                "data_context": processed_data,
                "source": "gemini"
            }
            return insight
        except Exception as e:
            logger.error(f"Error generating insight: {e}")
            return self._generate_fallback_insight(user_type, transaction_data)

    def _create_prompt(self, user_type: str, data_context: Dict[str, Any], template_dict=None) -> str:
        """Create prompt based on user type and data context, using the provided template dict."""
        if template_dict is None:
            template_dict = self.config.PROMPT_TEMPLATES_VOLUME
        template = template_dict.get(user_type, template_dict.get("non-tech"))
        formatted_context = self._format_data_context(data_context)
        return template.format(data_context=formatted_context)
    
    def _format_data_context(self, data: Dict[str, Any]) -> str:
        """Format data context for prompt"""
        context_parts = []
        
        if "metrics" in data:
            metrics = data["metrics"]
            context_parts.append(f"Transaction Metrics:")
            for key, value in metrics.items():
                context_parts.append(f"- {key}: {value}")
        
        if "comparisons" in data:
            comparisons = data["comparisons"]
            context_parts.append(f"\nPredictions vs Actuals:")
            for key, value in comparisons.items():
                context_parts.append(f"- {key}: {value}")
        
        if "trends" in data:
            trends = data["trends"]
            context_parts.append(f"\nTrends:")
            for trend in trends:
                context_parts.append(f"- {trend}")
        
        if "events" in data:
            events = data["events"]
            context_parts.append(f"\nCalendar Events:")
            for event in events:
                context_parts.append(f"- {event}")
        
        return "\n".join(context_parts)
    
    def _generate_with_gemini(self, prompt: str) -> str:
        """Generate insight using Google Gemini"""
        try:
            import google.generativeai as genai
            
            model = genai.GenerativeModel(self.config.GEMINI_MODEL)
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.config.TEMPERATURE,
                    max_output_tokens=self.config.MAX_TOKENS
                )
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise
    
    def _generate_fallback_insight(self, user_type: str, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback insight using templates"""
        fallback_templates = {
            "executive": "Transaction volume shows {trend} pattern. Key categories: {top_categories}. Revenue impact: {revenue_impact}.",
            "marketing": "Customer engagement is {engagement_level}. Best performing category: {best_category}. Campaign opportunity: {opportunity}.",
            "engineering": "Model accuracy: {accuracy}%. System performance: {performance}. Data quality: {quality}.",
            "non-tech": "Transactions are {trend_description}. The {category} category is doing {performance}. This means {business_impact}."
        }
        
        # Extract basic metrics for fallback
        metrics = transaction_data.get("metrics", {})
        
        # Simple fallback logic
        if user_type == "executive":
            insight = f"Overall transaction volume is {metrics.get('total_transactions', 'stable')}. Top performing category is {metrics.get('top_category', 'general')}."
        elif user_type == "marketing":
            insight = f"Customer activity shows {metrics.get('growth_rate', 'steady')} growth. Best opportunity in {metrics.get('best_category', 'general')} category."
        elif user_type == "engineering":
            insight = f"System is performing well with {metrics.get('accuracy', 'good')} prediction accuracy. Model performance is {metrics.get('performance', 'stable')}."
        else:
            insight = f"Transaction activity is {metrics.get('status', 'normal')}. The {metrics.get('category', 'main')} category is performing well."
        
        return {
            "user_type": user_type,
            "insight_text": insight,
            "generated_at": datetime.now().isoformat(),
            "data_context": transaction_data,
            "source": "fallback_template"
        }
    
    def generate_dashboard_summary(self, transaction_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate summary insights for dashboard"""
        user_types = ["executive", "marketing", "engineering", "non-tech"]
        summaries = []
        
        for user_type in user_types:
            try:
                insight = self.generate_insight(user_type, transaction_data)
                summaries.append(insight)
            except Exception as e:
                logger.error(f"Error generating summary for {user_type}: {e}")
                # Add fallback
                summaries.append(self._generate_fallback_insight(user_type, transaction_data))
        
        return summaries 

llm_service = LLMService()

def generate_insight(user_type, transaction_data):
    return llm_service.generate_insight(user_type, transaction_data) 