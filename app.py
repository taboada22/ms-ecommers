from app import create_app
from app import create_app
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005,debug=True)