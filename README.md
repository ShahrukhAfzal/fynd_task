# IMDB API task using FastAPI


## Prerequisites:

- Python 3.6 or higher

## Clone the project

```
git clone https://github.com/ShahrukhAfzal/fynd_task.git
```

## Run local

### create and activate virtual environment 

 works for linux only
```
 virtualenv env
 source env/bin/activate
```
for other os please refer to the python virual environment [docs](https://docs.python.org/3.6/tutorial/venv.html)

### Install dependencies

```
pip install -r requirements.txt
```

### Run server

```
uvicorn app.main:app --reload
```

### Run tests

```
pytest
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8000/docs
```

### Deployment on Heroku

For deployment on heroku refer [this](https://www.tutlinks.com/create-and-deploy-fastapi-app-to-heroku/) article
