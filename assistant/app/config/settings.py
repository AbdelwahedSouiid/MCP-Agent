class Settings:
    PROJECT_NAME: str = "Assistant Adv Intelligent"
    VERSION: str = "1.0"
    PORT: int = 8080
    RELOAD: bool = True
    # session recuperer depuis l'application
    OLLAMA_MODEL = "llama3.2"
    OLLAMA_API_URL = "http://localhost:11434/api"
    Deepseek_Model = "deepseek-chat"
    DEEPSEEK_API_KEY= "sk-cdb75809151149d69cab6584a3296ce6"
    SESSION_COOKIE_NAME: str = "session_id_1"
    

settings = Settings()


