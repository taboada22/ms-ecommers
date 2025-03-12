from dotenv import load_dotenv
from pathlib import Path
import os

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))
cache_config={
    'CACHE_TYPE': 'RedisCache', 
    'CACHE_DEFAULT_TIMEOUT': 300, #Por cuanto tiempo se va a mantener en cache el dato
    'CACHE_REDIS_HOST': os.environ.get('REDIS_HOST'), 
    'CACHE_REDIS_PORT': os.environ.get('REDIS_PORT')
}