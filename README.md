# fav-links

mini web application project (backend only)

# Initially

run docker compose

```
docker compose up -d --build
```

execute to container bash

```
docker exec -it backend-1 bash
```

initial migrate

```
python manange.py migrate
```

create superuser if dont have account

```
python manage.py createsuperuser
```

CLI

execute in bash
python manage.py executecli

then need to login befor

input format if need to parse parameters
if want to process on "add" action with parameters url="https://www.google.com/" and title is Google

you can type

```
add url="https://www.google.com/" title=Google category="Search Engine" tags=search,google,default-url
```
