from env import config
from app.app import app

serve_config = config.get('serve')

app.run(host=serve_config.get('ip'),
        port=serve_config.get('port'),
        debug=serve_config.get('debug'))
