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
