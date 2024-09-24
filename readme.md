# Streamlit Data with Mongo

This demo project shows how easy it is to stand up a data visualization using Streamlit and MongoDB.

## Installation

This project uses:

- `streamlit` to build the interactive interface
- `pymongo` to interact with the database
- `altair` to generate graphs

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Load data into your mongodb instance

> **Note**: This is assuming that you have an environment variable named `MONGODB_URI` containing the url to your MongoDB or Atlas cluster.

```powershell
mongoimport --uri $env:MONGODB_URI --db demo --collection computers data.json
```

Run

Please note the extra bare `--` which signals streamlit that the following cli option `--uri` is for **app.py** and not for _Streamlit_.

```powershell
streamlit app.py -- --uri $env:MONGODB_URI
```

Open broser to one of the URLs listed by the app in the console.
