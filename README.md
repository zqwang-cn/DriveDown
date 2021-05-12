# Drive Downloader

Create a website using Django to download files from Google Drive, OneDrive and Dropbox. The website must be deployed on a server that can access these drives.

## Preparation

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

## Debug

Run server using

```bash
python manage.py runserver
```

and visit [localhost:8000](http://localhost:8000)

## Deployment

Use [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) or other tools to deploy.