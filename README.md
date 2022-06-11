# api-yueying

Django REST API for YueYing Website, A Website for Reviewing Books and Videos

## Contributors

### [`Cheang Fou SUY`](https://github.com/CheangFouSUY)

### [`Wengshan NG`](https://github.com/Coralnws)

## Project Setup

- for initial setup, need to install the dependencies inside `.\requirement.txt` file

```powershell
pip install .\requirements.txt
```

- after that, go to `yueying\`  directory, then follow the `.template.env` file format for environment variables that needed for `settings.py` file

## Compile And Run Project

go to path that have `manage.py` file then run the following command

```powerhsell
py manage.py runserver
```

## Database Migration

new database will need to `makemigrations` and `migrate` by using the following commands

```powershell
py manage.py makemigrations
py manage.py migrate
```

## Note

for image storage, needed to have [AWS S3](https://aws.amazon.com/) and need it opens publicly
