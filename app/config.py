import os

class Settings:
    PROJECT_NAME: str = "Agon API Solver"
    VERSION: str = "2.0.0"
    
    # Feature Flags
    ENABLE_LLM_FALLBACK: bool = True
    
    # API Keys
    GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
    
    # Performance Thresholds
    MAX_OUTPUT_LENGTH: int = 1500 # Agon limit threshold

settings = Settings()
