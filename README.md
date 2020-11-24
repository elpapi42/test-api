# test-api

This is an application for register users and companies, with no real use case or bussiness model to cover, this is just an api for a job application.

you need Docker and docker-compose for run this API:
```bash
sudo docker-compose up -d --build
```

## Users

### Register User

POST `/users/`
```json
{
	"email": "whitman01@mail.com",
	"password": "whitman",
	"company_id": null,
	"profile": {
		"name": "whitman",
		"last_name": "bohorquez",
		"age": 22,
		"gender": "M",
		"document_number": "26493929"
	}
}
```

Response  
```json
{
    "id": "5fbd60e112d0ce5b6000e057",
    "email": "whitman01@8mail.com",
    "company_id": null,
    "profile": {
        "name": "whitman",
        "last_name": "bohorquez",
        "age": 20,
        "gender": "M",
        "document_number": "26493929"
    },
    "admin": false
}
```

### Login User

POST `/login/`
```json
{
	"email": "whitman01@mail.com",
	"password": "whitman",
}
```

Response  
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDYyNjgyNjgsInN1YiI6IjVmYmQ2MGUxMTJkMGNlNWI2MDAwZTA1NyIsImFkbSI6ZmFsc2V9.0EyzLZvwclzAZ2oZw83EPu_EG3JdcmspaEkiYV561Vw",
    "token_type": "bearer"
}
```

The token must be saved for later, will be used to authenticate the requests

### List Users

This route requires the autheticated user to be an admin, normal users cant fetch other users data

GET `/users/`
Headers: `Authorization`: `Bearer <token>`

Response  
```json
[
  {
    "id": "5fbd4b4a6b70963958f97375",
    "email": "whitman@hotmail.com",
    "company_id": "5fbd4b6315c066980bd6e9db",
    "profile": {
      "name": "whitman",
      "last_name": "bohorquez",
      "age": 23,
      "gender": "M",
      "document_number": "26493929"
    },
    "admin": true
  },
  {
    "id": "5fbd4b6715c066980bd6e9dc",
    "email": "whitm@mail.com",
    "company_id": "5fbd4b6315c066980bd6e9db",
    "profile": {
      "name": "whitman",
      "last_name": "bohorquez",
      "age": 10,
      "gender": "M",
      "document_number": "26493929"
    },
    "admin": false
  },
]
```

### Retrieve User

Normal users can only access their own data, for fetch data of users other than autheticated, the token must be owned by an admin

GET `/users/:id/`
Headers: `Authorization`: `Bearer <token>`

Response
```json
{
    "id": "5fbd4b6715c066980bd6e9dc",
    "email": "whitm@mail.com",
    "company_id": "5fbd4b6315c066980bd6e9db",
    "profile": {
        "name": "whitman",
        "last_name": "bohorquez",
        "age": 10,
        "gender": "M",
        "document_number": "26493929"
    },
    "admin": false
},
```

### Update User

Normal users can only update their own data, for update data of users other than autheticated, the token must be owned by an admin

PATCH `/users/:id/`
Headers: `Authorization`: `Bearer <token>`
```json
{
	"password": "holasoygerman",
	"company_id": "5fbd4b6315c066980bd6e9db",
	"profile": {
		"name": "whitman",
		"last_name": "bohorquez",
		"age": 23,
		"gender": "M",
		"document_number": "26493929"
	},
	"admin": true
}
```

This is a patch method, hence a partial update, all the fields are optional.

Response `204 No Content`

Actually, the method allows the users to register to an company, so, if someone wants to be part of a company, he can do:

PATCH `/users/:id/`
Headers: `Authorization`: `Bearer <token>`
```json
{
	"company_id": "5fbd4b6315c066980bd6e9db"
}
```

Response `204 No Content`

company_id must be a valid and registered company id.

### Delete User

Only admins can delete users

DELETE `/users/:id/`
Headers: `Authorization`: `Bearer <token>`

Response `204 No Content`

### Users Stats

This endpoint return general stats about the distribution of registered users based on age and gender. Only admins can access this endpoint.

GET `/stats/`
Headers: `Authorization`: `Bearer <token>`

Response  
```json
{
    "M:19": 0,
    "M:20": 0,
    "M:21": 0,
    "M:22": 0,
    "M:23": 1,
    "F:19": 0,
    "F:20": 0,
    "F:21": 0,
    "F:22": 0,
    "F:23": 0
}
```

The returned data can be filtered using `age` and `gender` query filters:

GET `/stats/?age=20`
Headers: `Authorization`: `Bearer <token>`

Response  
```json
{
    "M:20": 0,
    "F:20": 0
}
```

GET `/stats/?gender=M`
Headers: `Authorization`: `Bearer <token>`

Response  
```json
{
    "M:19": 0,
    "M:20": 0,
    "M:21": 0,
    "M:22": 0,
    "M:23": 1
}
```

Both filters can be used at the same time, and can be used multiple times each, for example:

GET `/stats/?gender=M&age=20&age=21`
Headers: `Authorization`: `Bearer <token>`

This will return all the Male users with ages 20 or 21

Response  
```json
{
    "M:20": 0,
    "M:21": 0,
}
```

## Companies

### Register Company

Only admins can register new companies.

POST `/users/`
```json
{
	"email": "whitman01@mail.com",
	"password": "whitman",
	"company_id": null,
	"profile": {
		"name": "whitman",
		"last_name": "bohorquez",
		"age": 22,
		"gender": "M",
		"document_number": "26493929"
	}
}
```

Response  
```json
{
    "id": "5fbd60e112d0ce5b6000e057",
    "email": "whitman01@8mail.com",
    "company_id": null,
    "profile": {
        "name": "whitman",
        "last_name": "bohorquez",
        "age": 20,
        "gender": "M",
        "document_number": "26493929"
    },
    "admin": false
}
```