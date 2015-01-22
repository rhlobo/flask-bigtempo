Flask-BigTempo
--------------

Flask extension created to enable a flask server to provide bigtempo functions.

## Installing

`pip` should do the job:
```bash
$ pip install flask-bigtempo
```

There is a `requirements.txt` file is you want to checkout the source code directly.

-------------------------------------------------------------------------------

## Datastore API
It is meant to store timeseries data.

Each timeseries is identified by the conjunction of an `reference` and a `symbol`.
It is structured this way so that the source (or type) of the data can be declared as the `reference`.
Example:
- While in the stockmarket context, the `reference` can be NASDAQ while `symbol` is left for the company stock.
- Storing country 'UN Human Development Index' the `reference` can be `HDI` while the `symbol` would take a country's name or code.

Here you can find:

- A __Storage__ implementation that offers methods to save / update, retrieve and delete `pandas dataframes`
- A __flask extension__ that exposes an REST API that handles data as json
- A __REST client__ that can communicate with the REST API
- A __command line script__ that enables shell usage of the REST API

### Storage implementation
For the moment the is only one implementation based on SQLAlchemy.
You can find it at `flask_bigtempo/store/storages.py`.
Example usage can be found `flask_bigtempo/store/clients.py`


### The flask extension:
You can easily have your flask server expose `bigtempo store api`:
```python
#!/usr/bin/env python


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bigtempo import DatastoreAPI


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

db = SQLAlchemy(app)

# The datastore api needs flask's app instance and a sqlalchemy engine
datastore = DatastoreAPI(app, db.engine)


@app.route('/')
def hello_world():
    return '''
           <h1>Welcome!</h1>
           The routes for datastore can be found at "/api/store/"<br/>
           '''


if __name__ == '__main__':
    app.run(debug=True)
```

The following methods are made available:

- Data retrieval: __GET__ /api/store/<reference>/<symbol>
- Data insertion: __PUT__ /api/store/<reference>/<symbol>
- Data deletion: __DELETE__ /api/store/<reference>/<symbol>

Optionally, you can use the `jsonformat` url parameter (eg.: `?jsonformat=index`).
The formats available are the same provided by the pandas `to_json` and `read_json` methods.


### REST Client
You can find it at `flask_bigtempo/store/clients.py`.

Using it should be as simple as:
```python
import flask_bigtempo.store.clients as store_client

api = store_client.StoreRestClient()
dataframe = api.retrieve('HDI', 'Brazil')
```


### CL Script
Its code is available at the `scripts` directory.
As soon as you install this lib at your computer, `client_api` should be available on the PATH.

You can learn more about its usage by executing `client_api -h`
