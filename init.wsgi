python_home = '/home/ubuntu/.cache/pypoetry/virtualenvs/application--oV7L9bQ-py3.8' # For ubuntu server. Make this dynamically generated
activate_this = python_home + '/bin/activate_this.py'

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import os
import sys

BASE_DIR = os.path.join(os.path.dirname(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from application import init_app
from dotenv import load_dotenv

load_dotenv()
application = init_app()
application.secret_key = os.getenv('SECRET_KEY', 'for dev') 


if __name__ == "__main__":
    application.run(host="0.0.0.0")
