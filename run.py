from gingerblog import create_app, db
from flask_migrate import Migrate
import os

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
