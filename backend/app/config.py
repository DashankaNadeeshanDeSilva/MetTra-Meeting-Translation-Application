# Configuration Management by centralizing APP settings


# Configuration management with model names and API endpoints

from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings)
	WHISPER_MODEL: str - 'base'
	TRANSLATION_MODEL: str
	OLLAMA_URL: str
	LIVEKIT_API_KEY: str
	LIVEKIT_SECRET_KEY: str

	class Config: # define metadata or behavior settings for the parent class and comes from Pydantic lib
        # Dynamically locate the .env file inside the global .gitignore folder
        env_file = str(Path(__file__).parent.parent.parent / ".gitignore" / ".env")


settings = Settings()

'''
Hide APi keys and Secret keys:
1. Include them in the .env file to store them for local testing, then load
   in the script and Pydantic automatically loads (.env should be in root dir) 
   include this in .gitignore to prevent commiting.
2. For deplymnet with ci/cd, use Github secret managment feature. Add keys and 
   secret keys to 'secrets and variabels' then call up in the workflow file (yml):
    env:
        LIVEKIT_API_KEY: ${{ secrets.LIVEKIT_API_KEY }}
        LIVEKIT_SECRET_KEY: ${{ secrets.LIVEKIT_SECRET_KEY }}
'''

"""
Why pydantic config script:
 - Allows to load configuration values from multiple sources
 - NO need a seperate code to parse .env or yaml files (this handles them dynamically)
 - Pydantic ensures that the configuration values have the expected types (e.g., strings, integers, URLs).
 - Pydantic allows for custom validation logic; e.g. ensure LIVEKIT_HOST is a valid WebSocket URL.
 - Configuration values can be overridden without modifying the source code or files (more dynamic than yaml or .env)
   simply by setting environment variables e.g. In Docker container just override LIVEKIT_API_KEY with new.
 - With Pydantic, all confg values can be accessed though a single object

Why not YAML or .env
	- No type checking, manual parsing, environment sp
"""