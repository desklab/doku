import os
from doku import create_app

app = create_app(config=os.environ.get('DOKU_CONFIG', 'config.dev'))
