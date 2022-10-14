## create folder
```
mkdir .ebextensions
```
## create file .ebextensions/django.config
```
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: ebdjango.wsgi:application
```
```
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: ebdjango.asgi:application
```
## add to allow host
```
ALLOWED_HOSTS = ['eb-django-app-dev.elasticbeanstalk.com']
```

```
eb init
eb status
eb deploy
eb open
eb logs --zip
eb logs
```