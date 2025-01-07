# config/settings.py

import os
from dataclasses import dataclass, fields
from typing import Any, Dict, List, Literal, Optional, Tuple
from enum import Enum
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig
from langchain_fireworks import ChatFireworks
from langchain_anthropic import ChatAnthropic 
from langchain_cohere import ChatCohere
from langchain_ollama import ChatOllama

class ModelProvider(str, Enum):
    FIREWORKS = "fireworks"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    OLLAMA = "ollama"

@dataclass
class ModelSettings:
    """Settings for each model provider"""
    enabled: bool = False
    api_key: Optional[str] = None
    model_name: Optional[str] = None
    base_url: Optional[str] = None
    extra_config: Dict[str, Any] = None

    @classmethod
    def from_env(cls, prefix: str) -> "ModelSettings":
        """Create settings from environment variables with given prefix"""
        return cls(
            enabled=os.getenv(f"{prefix}_ENABLED", "false").lower() == "true",
            api_key=os.getenv(f"{prefix}_API_KEY"),
            model_name=os.getenv(f"{prefix}_MODEL_NAME"),
            base_url=os.getenv(f"{prefix}_BASE_URL"),
            extra_config={k.replace(f"{prefix}_CONFIG_", "").lower(): v 
                         for k, v in os.environ.items() 
                         if k.startswith(f"{prefix}_CONFIG_")}
        )

class ModelConfig:
    """Enhanced model configuration with fallback support"""
    
    def __init__(self):
        self.providers: Dict[ModelProvider, ModelSettings] = {
            ModelProvider.FIREWORKS: ModelSettings.from_env("FIREWORKS"),
            ModelProvider.ANTHROPIC: ModelSettings.from_env("ANTHROPIC"),
            ModelProvider.COHERE: ModelSettings.from_env("COHERE"),
            ModelProvider.OLLAMA: ModelSettings.from_env("OLLAMA"),
        }
        
        # Get fallback order from environment or use default
        fallback_order = os.getenv("MODEL_FALLBACK_ORDER", "fireworks,anthropic,cohere,ollama")
        self.fallback_order = [ModelProvider(p.strip()) for p in fallback_order.split(",")]
        
    def _create_model(self, provider: ModelProvider) -> Optional[BaseChatModel]:
        """Create a model instance for the given provider"""
        settings = self.providers[provider]
        
        if not settings.enabled or not settings.model_name:
            return None
            
        try:
            if provider == ModelProvider.FIREWORKS:
                return ChatFireworks(
                    api_key=settings.api_key,
                    model=settings.model_name,
                    **settings.extra_config
                )
            elif provider == ModelProvider.ANTHROPIC:
                return ChatAnthropic(
                    api_key=settings.api_key,
                    model=settings.model_name,
                    **settings.extra_config
                )
            elif provider == ModelProvider.COHERE:
                return ChatCohere(
                    api_key=settings.api_key,
                    model=settings.model_name,
                    **settings.extra_config
                )
            elif provider == ModelProvider.OLLAMA:
                return ChatOllama(
                    base_url=settings.base_url or "http://localhost:11434",
                    model=settings.model_name,
                    **settings.extra_config
                )
        except Exception as e:
            print(f"Failed to initialize {provider} model: {str(e)}")
            return None
            
        return None

    def get_model(self) -> Tuple[BaseChatModel, ModelProvider]:
        """Get the first available model in the fallback chain"""
        errors = []
        
        for provider in self.fallback_order:
            try:
                model = self._create_model(provider)
                if model:
                    return model, provider
            except Exception as e:
                errors.append(f"{provider}: {str(e)}")
                
        raise RuntimeError(
            f"No models available in fallback chain. Errors: {'; '.join(errors)}"
        )

@dataclass(kw_only=True)
class Configuration:
    """Base configuration for the application"""
    user_id: str = "default-user"
    model_config: ModelConfig = ModelConfig()
    
    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "Configuration":
        configurable = config["configurable"] if config and "configurable" in config else {}
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls) if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})

class PathConfig:
    """Path configuration for the application"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    
    @classmethod
    def get_prompt_path(cls, prompt_name: str) -> str:
        """Get full path for a prompt file"""
        return os.path.join(cls.PROMPTS_DIR, prompt_name)