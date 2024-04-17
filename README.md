# FAV-Links web application

Project was written in Python (version 3.10) using Django and Django Rest Framework
Created by [Nachai Paramesthanakorn](nachai.pf@gmail.com)

## Initially

### Build and run docker following this instruction:

#### If you've not built image, follow this instructions:

1. Create .env file and add _SECRET_KEY_ variable

2. Using docker compose for start container

   ```
   docker-compose up -d --build
   ```

3. Execute container 'backend' (container named 'fav-links-backend-1') bash

   ```
   docker exec -it fav-links-backend-1 bash
   ```

4. Make migration
   ```
   $ python manage.py migrate
   ```
5. Create django super user for using django admin
   ```
   $ python manage.py createsuperuser
   ```

## Endpoints

### Authentication Headers

Using DRF seesion authentication that you should provid
and authentication in header when request:

```
X-CSRFToken: {{csrfToken}}
```

#### To get the csrf token

    GET /csrf/

Server will response json like this

```json
{
  "csrfToken": "Token..."
}
```

Response status code 200

---

### User Account Management

#### Registration

    POST /api/account/registration/

Required field: username, password.
Allow anonymous user but need csrf token header

Example request body:

```json
{
  "username": "sample.user",
  "password": "sample@Pwd1"
}
```

Response status code 201

### Authentication

#### Login

    POST /api/account/login/

Required field: username, password.

Example request body:

```json
{
  "username": "sample.user",
  "password": "sample@Pwd1"
}
```

Response status code 200

---

#### Logout

Need authenticated user

    POST /api/account/logout/

Response status code 200

---

### Favorite Url Endpoints

#### List Favorite URLs

List favorite url which created by authenticated user

    GET /api/fav-link/urls/

Optional query parameters:

- url: search by url i.e. url=google
- title: search by title i.e. title=Document
- tags: filter tag name seperate by comma i.e. tags=tag-1,tag-2
- category: filter category name i.e. category=Python

Example Response with pagination count:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "url": "https://www.google.com/",
      "title": "This is title",
      "owner": 1,
      "tags": [
        {
          "name": "tag-1"
        },
        {
          "name": "tag-2"
        }
      ],
      "category": {
        "id": 1,
        "name": "Search Engine"
      },
      "create_at": "2024-04-11T14:03:41.983851Z"
    }
  ]
}
```

Response status 200

---

#### Add Favorite URL

Need authenticated user

    POST /api/fav-link/urls/

Required field: url
Optional field:

- title: char field
- tags: list of object with name attribute
- category: object with name attribute

_If there're no category and/or tag name, system will create them automatically._

Example request body:

```json
{
  "url": "https://docs.djangoproject.com/en/5.0/",
  "title": "Django doc",
  "tags": [
    {
      "name": "tag-name"
    },
    {
      "name": "python"
    }
  ],
  "category": {
    "name": "Framework"
  }
}
```

Response status code 201

---

#### Get single Favorite URL

Need authenticated user

    GET /api/fav-link/urls/{id}

Required parameter: id

Example response:

```json
{
  "id": 1,
  "url": "https://docs.djangoproject.com/en/5.0/",
  "title": "Django doc",
  "tags": [
    {
      "name": "tag-name"
    },
    {
      "name": "python"
    }
  ],
  "category": {
    "id": 15,
    "name": "Framework"
  },
  "create_at": "2024-04-16T17:01:18.942878Z"
}
```

Response status code 200

---

#### Update Favorite URL

Need authenticated user

    PUT /api/fav-link/urls/{id}

Required parameter: id
Optional update field:

- url
- title
- tags: value is [] or null for remove tags
- category: value is null for remove category

_If there're no category and/or tag name, system will create them automatically._

Example request body:

```json
{
  "url": "https://docs.djangoproject.com/en/5.0/",
  "title": "Django doc",
  "tags": [
    {
      "name": "tag-name"
    },
    {
      "name": "python"
    }
  ],
  "category": {
    "name": "Framework"
  }
}
```

Response status code 200

---

#### Delete Favorite URL

Need authenticated user

    DELETE /api/fav-link/urls/{id}

Required parameter: id

Response status code 200

---

### Tag Endpoints

#### List Tags

List tags which created by authenticated user

    GET /api/fav-link/tags/

Optional query parameters:

- name: filter by tag name i.e. name=py

Example Response with pagination count:

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 4,
      "name": "rer33",
      "owner": 1,
      "create_at": "2024-04-15T08:54:15.270689Z"
    },
    {
      "id": 5,
      "name": "sample-1",
      "owner": 1,
      "create_at": "2024-04-15T09:18:19.633479Z"
    }
  ]
}
```

Response status 200

---

#### Add Tag

Need authenticated user

    POST /api/fav-link/tags/

Required field: name (should be in slug field)

Example request body:

```json
{
  "name": "python-django"
}
```

Response status code 201

---

#### Get Single Tag

Need authenticated user

    GET /api/fav-link/tags/{tag_name}/

Required parameter: tag_name

Example response:

```json
{
  "id": 34,
  "name": "python-django",
  "owner": 1,
  "create_at": "2024-04-11T17:34:44.314375Z"
}
```

Response status code 200

---

#### Update Tag

Need authenticated user

    PUT /api/fav-link/tags/{tag_name}

Required parameter: tag_name
Required field: name

Example request body:

```json
{
  "name": "python-django"
}
```

Response status code 200

---

#### Delete Tag

Need authenticated user

    DELETE /api/fav-link/tags/{tag_name}

Required parameter: tag_name

Response status code 200

---

#### List Category

List category which created by authenticated user

    GET /api/fav-link/category/

Optional query parameters:

- name: filter by category name i.e. name=Trip

Example Response with pagination count:

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Trip Budget",
      "owner": 1,
      "create_at": "2024-04-11T11:27:24.153924Z",
      "url": "http://localhost:8000/api/fav-link/category/1/"
    },
    {
      "id": 3,
      "name": "Test Cases",
      "owner": 1,
      "create_at": "2024-04-11T12:23:38.077568Z",
      "url": "http://localhost:8000/api/fav-link/category/3/"
    }
  ]
}
```

Response status 200

---

### Category Endpoints

#### Add Category

Need authenticated user

    POST /api/fav-link/category/

Required field: name (should be in slug field)

Example request body:

```json
{
  "name": "Search Engine"
}
```

Response status code 201

---

#### Get Single Category

Need authenticated user

    GET /api/fav-link/category/{id}/

Required parameter: id

Example response:

```json
{
  "id": 10,
  "name": "Trip Japan",
  "owner": 1,
  "create_at": "2024-04-11T19:03:58.966054Z",
  "url": "http://localhost:8000/api/fav-link/category/10/"
}
```

Response status code 200

---

#### Update Category

Need authenticated user

    PUT /api/fav-link/category/{id}

Required parameter: id
Required field: name

Example request body:

```json
{
  "name": "Trip USA"
}
```

Response status code 200

---

#### Delete Category

Need authenticated user

    DELETE /api/fav-link/category/{id}

Required parameter: id

Response status code 200

---

### CLI

Using django command admin

#### Executed in container bash

```
python manage.py executecli
```

#### Then you need to login before handle action

```
Enter [username]:
Enter [password]:
```

#### Command action following command format:

1. The first argument must be action name.
2. The rest of arguments will parameter.
3. Using '=' for assign parameter value.
4. Text without space can leave double quote i.e. param=hello
5. If parameter has space, you need to place value between double quote i.e. param="hello world"
6. Tags parameter can use , (comma) for seperate value to list

**Follow this format**: [action] param1=value param2=value2 param3="string with space"

For example:

```
$ list title=new category="hello world" tags=python,py
```

```
$ get id=1
```

```
add url="https://www.google.com/" title=Google category="Search Engine" tags=search,google,default-url
```
