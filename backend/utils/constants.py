# Master model configuration - single source of truth
MODELS = {

    # "bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0": {
    #     "aliases": ["claude-sonnet-4"],
    #     "pricing": {
    #         "input_cost_per_million_tokens": 3.00,
    #         "output_cost_per_million_tokens": 15.00
    #     },
    #     "tier_availability": ["free", "paid"]
    # },   
    
    # Free tier models
    "bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0": {
        "aliases": ["Expert 🤑💰💸"],
        "pricing": {
            "input_cost_per_million_tokens": 3.00,
            "output_cost_per_million_tokens": 15.00
        },
        "tier_availability": ["free", "paid"]
    },

    "openrouter/google/gemini-2.5-pro": {
        "aliases": ["Gemini Pro"],
        "pricing": {
            "input_cost_per_million_tokens": 1.25,
            "output_cost_per_million_tokens": 10.00
        },
        "tier_availability": ["paid"]
    },


    "openrouter/openai/o4-mini-high": {
        "aliases": ["GPT-o4-mh 🧠⚖️💰"],
        "pricing": {
            "input_cost_per_million_tokens": 1.10,
            "output_cost_per_million_tokens": 4.40
        },
        "tier_availability": ["paid"]
    },

    "openrouter/openai/gpt-5-mini": {
        "aliases": ["GPT-5-M 🤖💰"],
        "pricing": {
            "input_cost_per_million_tokens": 0.25,
            "output_cost_per_million_tokens": 2.00
        },
        "tier_availability": ["free", "paid"]
    },

    "openrouter/google/gemini-2.5-flash": {
        "aliases": ["Main 💨⚡️🚀"],
        "pricing": {
            "input_cost_per_million_tokens": 0.3,
            "output_cost_per_million_tokens": 2.50
        },
        "tier_availability": ["free", "paid"]
    },



    "openrouter/x-ai/grok-4": {
        "aliases": ["Grok 💰🤓"],
        "pricing": {
            "input_cost_per_million_tokens": 3.00,
            "output_cost_per_million_tokens": 15.00
        },
        "tier_availability": ["paid"]
    },

    "openrouter/openai/gpt-5": {
        "aliases": ["GPT-5 🤖💰"],
        "pricing": {
            "input_cost_per_million_tokens": 1.25,
            "output_cost_per_million_tokens": 11.00
        },
        "tier_availability": ["paid"]
    },


    # "openrouter/openai/gpt-oss-120b": {
    #     "aliases": ["GPT-OSS"],
    #     "pricing": {
    #         "input_cost_per_million_tokens": 0.2,
    #         "output_cost_per_million_tokens": 1.00
    #     },
    #     "tier_availability": ["paid"]
    # },

}

# Derived structures (auto-generated from MODELS)
def _generate_model_structures():
    """Generate all model structures from the master MODELS dictionary."""
    
    # Generate tier lists
    free_models = []
    paid_models = []
    
    # Generate aliases
    aliases = {}
    
    # Generate pricing
    pricing = {}
    
    for model_name, config in MODELS.items():
        # Add to tier lists
        if "free" in config["tier_availability"]:
            free_models.append(model_name)
        if "paid" in config["tier_availability"]:
            paid_models.append(model_name)
        
        # Add aliases
        for alias in config["aliases"]:
            aliases[alias] = model_name
        
        # Add pricing
        pricing[model_name] = config["pricing"]
        
        # Also add pricing for legacy model name variations
        if model_name.startswith("gemini/"):
            legacy_name = model_name.replace("gemini/", "")
            pricing[legacy_name] = config["pricing"]
        elif model_name.startswith("openrouter/google/"):
            # Add google/gemini-2.5-pro alias for openrouter/google/gemini-2.5-pro
            google_name = model_name.replace("openrouter/", "")
            pricing[google_name] = config["pricing"]
        elif model_name.startswith("anthropic/"):
            # Add anthropic/claude-sonnet-4 alias for claude-sonnet-4-20250514
            if "claude-sonnet-4-20250514" in model_name:
                pricing["anthropic/claude-sonnet-4"] = config["pricing"]
        elif model_name.startswith("bedrock/us.anthropic.claude-sonnet-4"):
            # Add anthropic/claude-sonnet-4 and claude-sonnet-4 aliases for bedrock models
            pricing["anthropic/claude-sonnet-4"] = config["pricing"]
            pricing["claude-sonnet-4"] = config["pricing"]
        elif model_name.startswith("xai/"):
            # Add pricing for OpenRouter x-ai models
            openrouter_name = model_name.replace("xai/", "openrouter/x-ai/")
            pricing[openrouter_name] = config["pricing"]
    
    return free_models, paid_models, aliases, pricing

# Generate all structures
FREE_TIER_MODELS, PAID_TIER_MODELS, MODEL_NAME_ALIASES, HARDCODED_MODEL_PRICES = _generate_model_structures()

MODEL_ACCESS_TIERS = {
    "free": FREE_TIER_MODELS,
    "tier_2_20": PAID_TIER_MODELS,
    "tier_6_50": PAID_TIER_MODELS,
    "tier_12_100": PAID_TIER_MODELS,
    "tier_25_200": PAID_TIER_MODELS,
    "tier_50_400": PAID_TIER_MODELS,
    "tier_125_800": PAID_TIER_MODELS,
    "tier_200_1000": PAID_TIER_MODELS,
}
