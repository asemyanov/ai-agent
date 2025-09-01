"""
Configuration management.

This module provides a centralized way to access configuration settings and
environment variables across the application. It supports different environment
modes (development, staging, production) and provides validation for required
values.

Usage:
    from utils.config import config
    
    # Access configuration values
    api_key = config.OPENAI_API_KEY
    env_mode = config.ENV_MODE
"""

import os
from enum import Enum
from typing import Dict, Any, Optional, get_type_hints, Union
from dotenv import load_dotenv
import logging
import secrets

logger = logging.getLogger(__name__)

class EnvMode(Enum):
    """Environment mode enumeration."""
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"

class Configuration:
    """
    Centralized configuration for AgentPress backend.
    
    This class loads environment variables and provides type checking and validation.
    Default values can be specified for optional configuration items.
    """
    
    # Environment mode
    ENV_MODE: EnvMode = EnvMode.LOCAL
    
    # Subscription tier IDs - Production
    STRIPE_FREE_TIER_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUpjHARY5K'
    STRIPE_TIER_2_20_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUE4yuvihy'
    STRIPE_TIER_6_50_ID_PROD: str = 'price_1Rskv5PA6ngq7HqU75HMYmgX'
    STRIPE_TIER_12_100_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUpY1Vuho6'
    STRIPE_TIER_25_200_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUoSqcENlm'
    STRIPE_TIER_50_400_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUUajSvBqN'
    STRIPE_TIER_125_800_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUkdrI3lUh'
    STRIPE_TIER_200_1000_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUS0E9z6Qr'
    
    # Yearly subscription tier IDs - Production (15% discount)
    STRIPE_TIER_2_20_YEARLY_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUuyMrINo0'
    STRIPE_TIER_6_50_YEARLY_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUEDN8Up7u'
    STRIPE_TIER_12_100_YEARLY_ID_PROD: str = 'price_1Rskv5PA6ngq7HqUeYeXSLWb'
    STRIPE_TIER_25_200_YEARLY_ID_PROD: str = 'price_1Rskv4PA6ngq7HqUmx9mCQZP'
    STRIPE_TIER_50_400_YEARLY_ID_PROD: str = 'price_1Rskv4PA6ngq7HqU4dcc8VfY'
    STRIPE_TIER_125_800_YEARLY_ID_PROD: str = 'price_1Rskv4PA6ngq7HqUNuKAzAEy'
    STRIPE_TIER_200_1000_YEARLY_ID_PROD: str = 'price_1Rskv4PA6ngq7HqUyYTk3duo'

    # Yearly commitment prices - Production (15% discount, monthly payments with 12-month commitment via schedules)
    STRIPE_TIER_2_17_YEARLY_COMMITMENT_ID_PROD: str = 'price_1Rskv4PA6ngq7HqUw2QZ7b1h'  # $17/month
    STRIPE_TIER_6_42_YEARLY_COMMITMENT_ID_PROD: str = 'price_1Rskv4PA6ngq7HqU0HxMUEMP'  # $42.50/month
    STRIPE_TIER_25_170_YEARLY_COMMITMENT_ID_PROD: str = 'price_1Rskv4PA6ngq7HqUyHmxD6Lm'  # $170/month

    # Subscription tier IDs - Staging
    STRIPE_FREE_TIER_ID_STAGING: str = 'price_1Rskf1PA6ngq7HqUBVQwuKKn'
    STRIPE_TIER_2_20_ID_STAGING: str = 'price_1RskfBPA6ngq7HqUnfyIt89g'
    STRIPE_TIER_6_50_ID_STAGING: str = 'price_1RskfJPA6ngq7HqUqYwus8IH'
    STRIPE_TIER_12_100_ID_STAGING: str = 'price_1RskfUPA6ngq7HqUrz2zLWe2'
    STRIPE_TIER_25_200_ID_STAGING: str = 'price_1RskgTPA6ngq7HqUzyIfez1T'
    STRIPE_TIER_50_400_ID_STAGING: str = 'price_1RskgaPA6ngq7HqUtNJfkrhm'
    STRIPE_TIER_125_800_ID_STAGING: str = 'price_1RskgiPA6ngq7HqUhMaeH5Rp'
    STRIPE_TIER_200_1000_ID_STAGING: str = 'price_1RskhTPA6ngq7HqUpo5zFVTv'
    
    # Yearly subscription tier IDs - Staging (15% discount)
    STRIPE_TIER_2_20_YEARLY_ID_STAGING: str = 'price_1RskhfPA6ngq7HqUKEOxV7Bg'
    STRIPE_TIER_6_50_YEARLY_ID_STAGING: str = 'price_1RskhmPA6ngq7HqUwRFh4AZk'
    STRIPE_TIER_12_100_YEARLY_ID_STAGING: str = 'price_1Rski5PA6ngq7HqUkVZlHtyC'
    STRIPE_TIER_25_200_YEARLY_ID_STAGING: str = 'price_1RskiEPA6ngq7HqUYSHBEZBL'
    STRIPE_TIER_50_400_YEARLY_ID_STAGING: str = 'price_1RskipPA6ngq7HqUFsGEhbos'
    STRIPE_TIER_125_800_YEARLY_ID_STAGING: str = 'price_1RskiwPA6ngq7HqUzYNQEyHn'
    STRIPE_TIER_200_1000_YEARLY_ID_STAGING: str = 'price_1RskjiPA6ngq7HqUscgPhUtN'

    # Yearly commitment prices - Staging (15% discount, monthly payments with 12-month commitment via schedules)
    STRIPE_TIER_2_17_YEARLY_COMMITMENT_ID_STAGING: str = 'price_1RskjwPA6ngq7HqUpsn0aBp1'  # $17/month
    STRIPE_TIER_6_42_YEARLY_COMMITMENT_ID_STAGING: str = 'price_1RskkSPA6ngq7HqUcWqm5p9W'  # $42.50/month
    STRIPE_TIER_25_170_YEARLY_COMMITMENT_ID_STAGING: str = 'price_1RskkUPA6ngq7HqU6ZB4FJoW'  # $170/month
    


    
    # Computed subscription tier IDs based on environment
    @property
    def STRIPE_FREE_TIER_ID(self) -> str:   
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_FREE_TIER_ID_STAGING
        return self.STRIPE_FREE_TIER_ID_PROD
    
    @property
    def STRIPE_TIER_2_20_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_2_20_ID_STAGING
        return self.STRIPE_TIER_2_20_ID_PROD
    
    @property
    def STRIPE_TIER_6_50_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_6_50_ID_STAGING
        return self.STRIPE_TIER_6_50_ID_PROD
    
    @property
    def STRIPE_TIER_12_100_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_12_100_ID_STAGING
        return self.STRIPE_TIER_12_100_ID_PROD
    
    @property
    def STRIPE_TIER_25_200_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_25_200_ID_STAGING
        return self.STRIPE_TIER_25_200_ID_PROD
    
    @property
    def STRIPE_TIER_50_400_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_50_400_ID_STAGING
        return self.STRIPE_TIER_50_400_ID_PROD
    
    @property
    def STRIPE_TIER_125_800_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_125_800_ID_STAGING
        return self.STRIPE_TIER_125_800_ID_PROD
    
    @property
    def STRIPE_TIER_200_1000_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_200_1000_ID_STAGING
        return self.STRIPE_TIER_200_1000_ID_PROD
    
    # Yearly tier computed properties
    @property
    def STRIPE_TIER_2_20_YEARLY_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_2_20_YEARLY_ID_STAGING
        return self.STRIPE_TIER_2_20_YEARLY_ID_PROD
    
    @property
    def STRIPE_TIER_6_50_YEARLY_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_6_50_YEARLY_ID_STAGING
        return self.STRIPE_TIER_6_50_YEARLY_ID_PROD
    
    @property
    def STRIPE_TIER_12_100_YEARLY_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_12_100_YEARLY_ID_STAGING
        return self.STRIPE_TIER_12_100_YEARLY_ID_PROD
    
    @property
    def STRIPE_TIER_25_200_YEARLY_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_25_200_YEARLY_ID_STAGING
        return self.STRIPE_TIER_25_200_YEARLY_ID_PROD
    
    @property
    def STRIPE_TIER_50_400_YEARLY_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_50_400_YEARLY_ID_STAGING
        return self.STRIPE_TIER_50_400_YEARLY_ID_PROD
    
    @property
    def STRIPE_TIER_125_800_YEARLY_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_125_800_YEARLY_ID_STAGING
        return self.STRIPE_TIER_125_800_YEARLY_ID_PROD
    
    @property
    def STRIPE_TIER_200_1000_YEARLY_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_200_1000_YEARLY_ID_STAGING
        return self.STRIPE_TIER_200_1000_YEARLY_ID_PROD
    
    # Yearly commitment prices computed properties
    @property
    def STRIPE_TIER_2_17_YEARLY_COMMITMENT_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_2_17_YEARLY_COMMITMENT_ID_STAGING
        return self.STRIPE_TIER_2_17_YEARLY_COMMITMENT_ID_PROD

    @property
    def STRIPE_TIER_6_42_YEARLY_COMMITMENT_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_6_42_YEARLY_COMMITMENT_ID_STAGING
        return self.STRIPE_TIER_6_42_YEARLY_COMMITMENT_ID_PROD

    @property
    def STRIPE_TIER_25_170_YEARLY_COMMITMENT_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_TIER_25_170_YEARLY_COMMITMENT_ID_STAGING
        return self.STRIPE_TIER_25_170_YEARLY_COMMITMENT_ID_PROD
    
    # Credit package price ID properties
    # TEMPORARILY DISABLED - Missing PROD/STAGING attributes causing startup failures
    # @property
    # def STRIPE_CREDITS_10_PRICE_ID(self) -> str:
    #     if self.ENV_MODE == EnvMode.STAGING:
    #         return self.STRIPE_CREDITS_10_PRICE_ID_STAGING
    #     return self.STRIPE_CREDITS_10_PRICE_ID_PROD
    # 
    # @property
    # def STRIPE_CREDITS_25_PRICE_ID(self) -> str:
    #     if self.ENV_MODE == EnvMode.STAGING:
    #         return self.STRIPE_CREDITS_25_PRICE_ID_STAGING
    #     return self.STRIPE_CREDITS_25_PRICE_ID_PROD
    # 
    # @property
    # def STRIPE_CREDITS_50_PRICE_ID(self) -> str:
    #     if self.ENV_MODE == EnvMode.STAGING:
    #         return self.STRIPE_CREDITS_50_PRICE_ID_STAGING
    #     return self.STRIPE_CREDITS_50_PRICE_ID_PROD
    # 
    # @property
    # def STRIPE_CREDITS_100_PRICE_ID(self) -> str:
    #     if self.ENV_MODE == EnvMode.STAGING:
    #         return self.STRIPE_CREDITS_100_PRICE_ID_STAGING
    #     return self.STRIPE_CREDITS_100_PRICE_ID_PROD
    # 
    # @property
    # def STRIPE_CREDITS_250_PRICE_ID(self) -> str:
    #     if self.ENV_MODE == EnvMode.STAGING:
    #         return self.STRIPE_CREDITS_250_PRICE_ID_STAGING
    #     return self.STRIPE_CREDITS_250_PRICE_ID_PROD
    # 
    # @property
    # def STRIPE_CREDITS_500_PRICE_ID(self) -> str:
    #     if self.ENV_MODE == EnvMode.STAGING:
    #         return self.STRIPE_CREDITS_500_PRICE_ID_STAGING
    #     return self.STRIPE_CREDITS_500_PRICE_ID_PROD
    
    # LLM API keys
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: str
    XAI_API_KEY: Optional[str] = None
    MORPH_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    OPENROUTER_API_BASE: Optional[str] = "https://openrouter.ai/api/v1"
    OPENAI_COMPATIBLE_API_KEY: Optional[str] = None
    OPENAI_COMPATIBLE_API_BASE: Optional[str] = None
    OR_SITE_URL: Optional[str] = "http://mevoagent.com"
    OR_APP_NAME: Optional[str] = "MEVO"    
    
    # AWS Bedrock credentials
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION_NAME: Optional[str] = None
    

    
    # Supabase configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # Redis configuration
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SSL: bool = True
    
    # Daytona sandbox configuration
    DAYTONA_API_KEY: str
    DAYTONA_SERVER_URL: str
    DAYTONA_TARGET: str
    
    # Search and other API keys
    TAVILY_API_KEY: str
    RAPID_API_KEY: str
    CLOUDFLARE_API_TOKEN: Optional[str] = None
    FIRECRAWL_API_KEY: str
    FIRECRAWL_URL: Optional[str] = "https://api.firecrawl.dev"
    
    # Stripe configuration
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_DEFAULT_PLAN_ID: Optional[str] = None
    STRIPE_DEFAULT_TRIAL_DAYS: int = 14
    
    # Stripe Product IDs
    STRIPE_PRODUCT_ID_PROD: str = 'prod_SoNgsuj2fmyC3E'
    STRIPE_PRODUCT_ID_STAGING: str = 'prod_SoNPEPmnxdYD3J'
    
    # Sandbox configuration
    SANDBOX_IMAGE_NAME = "kortix/suna:0.1.3.12"
    SANDBOX_SNAPSHOT_NAME = "kortix/suna:0.1.3.12"
    SANDBOX_ENTRYPOINT = "/usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisord.conf"

    # LangFuse configuration
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    # Admin API key for server-side operations
    KORTIX_ADMIN_API_KEY: Optional[str] = None

    CLOUDFLARE_BASE_DOMAIN: Optional[str] = None
    CLOUDFLARE_API_TOKEN: Optional[str] = None
    CLOUDFLARE_ACCOUNT_ID: Optional[str] = None




    # API Keys system configuration
    API_KEY_SECRET: str = "default-secret-key-change-in-production"
    API_KEY_LAST_USED_THROTTLE_SECONDS: int = 900
    
    # Agent execution limits (can be overridden via environment variable)
    _MAX_PARALLEL_AGENT_RUNS_ENV: Optional[str] = None
    
    # Agent limits per billing tier
    # Note: These limits are bypassed in local mode (ENV_MODE=local) where unlimited agents are allowed
    AGENT_LIMITS = {
        'free': 20,
        'tier_2_20': 20,
        'tier_6_50': 20,
        'tier_12_100': 20,
        'tier_25_200': 100,
        'tier_50_400': 100,
        'tier_125_800': 100,
        'tier_200_1000': 100,
        # Yearly plans have same limits as monthly
        'tier_2_20_yearly': 20,
        'tier_6_50_yearly': 20,
        'tier_12_100_yearly': 20,
        'tier_25_200_yearly': 100,
        'tier_50_400_yearly': 100,
        'tier_125_800_yearly': 100,
        'tier_200_1000_yearly': 100,
        # Yearly commitment plans
        'tier_2_17_yearly_commitment': 20,
        'tier_6_42_yearly_commitment': 20,
        'tier_25_170_yearly_commitment': 100,
    }

    # Project limits per billing tier
    # Note: These limits are bypassed in local mode (ENV_MODE=local) where unlimited projects are allowed
    PROJECT_LIMITS = {
        'free': 1000,
        'tier_2_20': 5000,
        'tier_6_50': 5000,
        'tier_12_100': 5000,
        'tier_25_200': 2500,
        'tier_50_400': 5000,
        'tier_125_800': 10000,
        'tier_200_1000': 25000,
        # Yearly plans have same limits as monthly
        'tier_2_20_yearly': 1000,
        'tier_6_50_yearly': 5000,
        'tier_12_100_yearly': 5000,
        'tier_25_200_yearly': 2500,
        'tier_50_400_yearly': 5000,
        'tier_125_800_yearly': 10000,
        'tier_200_1000_yearly': 25000,
        # Yearly commitment plans
        'tier_2_17_yearly_commitment': 5000,
        'tier_6_42_yearly_commitment': 5000,
        'tier_25_170_yearly_commitment': 2500,
    }

    @property
    def MAX_PARALLEL_AGENT_RUNS(self) -> int:
        """
        Get the maximum parallel agent runs limit.
        
        Can be overridden via MAX_PARALLEL_AGENT_RUNS environment variable.
        Defaults:
        - Production: 3
        - Local/Staging: 999999 (effectively infinite)
        """
        # Check for environment variable override first
        if self._MAX_PARALLEL_AGENT_RUNS_ENV is not None:
            try:
                return int(self._MAX_PARALLEL_AGENT_RUNS_ENV)
            except ValueError:
                logger.warning(f"Invalid MAX_PARALLEL_AGENT_RUNS value: {self._MAX_PARALLEL_AGENT_RUNS_ENV}, using default")
        
        # Environment-based defaults
        if self.ENV_MODE == EnvMode.PRODUCTION:
            return 3
        else:
            # Local and staging: effectively infinite
            return 999999
    
    @property
    def STRIPE_PRODUCT_ID(self) -> str:
        if self.ENV_MODE == EnvMode.STAGING:
            return self.STRIPE_PRODUCT_ID_STAGING
        return self.STRIPE_PRODUCT_ID_PROD
    
    def _generate_admin_api_key(self) -> str:
        """Generate a secure admin API key for Kortix administrative functions."""
        # Generate 32 random bytes and encode as hex for a readable API key
        key_bytes = secrets.token_bytes(32)
        return key_bytes.hex()

    def __init__(self):
        """Initialize configuration by loading from environment variables."""
        # Load environment variables from .env file if it exists
        load_dotenv()
        
        # Set environment mode first
        env_mode_str = os.getenv("ENV_MODE", EnvMode.LOCAL.value)
        try:
            self.ENV_MODE = EnvMode(env_mode_str.lower())
        except ValueError:
            logger.warning(f"Invalid ENV_MODE: {env_mode_str}, defaulting to LOCAL")
            self.ENV_MODE = EnvMode.LOCAL
            
        logger.debug(f"Environment mode: {self.ENV_MODE.value}")
        
        # Load configuration from environment variables
        self._load_from_env()
        
        # Auto-generate admin API key if not present
        if not self.KORTIX_ADMIN_API_KEY:
            self.KORTIX_ADMIN_API_KEY = self._generate_admin_api_key()
            logger.info("Auto-generated KORTIX_ADMIN_API_KEY for administrative functions")
        
        # Perform validation
        self._validate()
        
    def _load_from_env(self):
        """Load configuration values from environment variables."""
        for key, expected_type in get_type_hints(self.__class__).items():
            env_val = os.getenv(key)
            
            if env_val is not None:
                # Convert environment variable to the expected type
                if expected_type == bool:
                    # Handle boolean conversion
                    setattr(self, key, env_val.lower() in ('true', 't', 'yes', 'y', '1'))
                elif expected_type == int:
                    # Handle integer conversion
                    try:
                        setattr(self, key, int(env_val))
                    except ValueError:
                        logger.warning(f"Invalid value for {key}: {env_val}, using default")
                elif expected_type == EnvMode:
                    # Already handled for ENV_MODE
                    pass
                else:
                    # String or other type
                    setattr(self, key, env_val)
        
        # Custom handling for environment-dependent properties
        max_parallel_runs_env = os.getenv("MAX_PARALLEL_AGENT_RUNS")
        if max_parallel_runs_env is not None:
            self._MAX_PARALLEL_AGENT_RUNS_ENV = max_parallel_runs_env
    
    def _validate(self):
        """Validate configuration based on type hints."""
        # Get all configuration fields and their type hints
        type_hints = get_type_hints(self.__class__)
        
        # Find missing required fields
        missing_fields = []
        for field, field_type in type_hints.items():
            # Check if the field is Optional
            is_optional = hasattr(field_type, "__origin__") and field_type.__origin__ is Union and type(None) in field_type.__args__
            
            # If not optional and value is None, add to missing fields
            if not is_optional and getattr(self, field) is None:
                missing_fields.append(field)
        
        if missing_fields:
            error_msg = f"Missing required configuration fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with an optional default."""
        return getattr(self, key, default)
    
    def as_dict(self) -> Dict[str, Any]:
        """Return configuration as a dictionary."""
        return {
            key: getattr(self, key) 
            for key in get_type_hints(self.__class__).keys()
            if not key.startswith('_')
        }

# Create a singleton instance
config = Configuration() 