# ZB Test - Alejandro Olaria
<br/>

## __Description__
---
This project was built as part of a test, it is a simple API made for storing products and its attributes, it expects to have two different types of users, **admins** & **anonymous**.

<br/>

## __Build__
---

1. Clone this Project
2. cd to `zb_test`
3. run __docker-compose up --build__

<br/>

## __Test__
---

* Run unit tests: 
    1. cd to `zb_test`
    2. run: __docker-compose exec zb_web python manage.py test .__
* Using postman:
    1. cd to `zb_test/utils/postman` 
    2. import those files to your postman

<br/>

### __End-points:__
<br/>

#### Login: (POST) requests JWT
---
Url: __/login/__

payload: 

    {
        "username": string,
        "password": string
    }

response (200):

    {
        "id": integer,
        "username": string,
        "access": string,
        "refresh": string
    }

<br/>

#### Product: (POST) creates product instance
---
Url: __/products/__

payload:

    {
        "name": string,
        "price": float,
        "brand": string
    }

__parameters:__

__name:__ product's name

__price:__ product's price

__brand:__ product's brand name

<br/>

response (201):

    {
        "sku": string,
        "price": float,
        "name": string,
        "brand": {
            "name": string
        }
    }

<br/>


#### Product: (GET) retrieve product instance
---
Url: __/products/{SKU}/details__

__parameters:__

__SKU:__ alphanumeric product's SKU

<br/>

response (200)

    {
        "sku": string,
        "price": float,
        "name": string,
        "brand": {
            "name": string
        },
        "watch_record": integer
    }

__watch_record:__ how many times an anonymous user retrieve that product

<br/>

#### Product: (PUT) updates product instance
---
Url: __/products/{SKU}__

payload:

    {
        "name": string,
        "price": float,
        "brand": string
    }
__parameters:__

__SKU:__ alphanumeric product's SKU

__name:__ product's name (OPTIONAL)

__price:__ product's price (OPTIONAL)

__brand:__ product's brand name (OPTIONAL)

<br/>

#### Product: (DELETE) deletes product instance
---
Url: __/products/{SKU}__

__parameters:__

__SKU:__ alphanumeric product's SKU

<br/>

#### Admins: (POST) creates "admin" instance
---
Url: __/admins/__

payload:

    {
        "username": string,
        "password": float,
        "email": string
    }

response (200): 

    {
        "id": integer,
        "username": string
    }

<br/>

#### Admins: (PUT) updates "admin" instance
---
Url: __/admins/{ID}/__

payload:

    {
        "username": string (optional),
        "password": float (optional),
        "email": string (optional)
    }

__parameters:__

__ID:__ Admin's ID

<br>


response (204)

<br/>


#### Admins: (DELETE) deletes "admin" instance
---
Url: __/admins/{ID}/__

__parameters:__

__ID:__ Admin's ID

<br/>


response (204)

---
made with ❤️ by [Alejandro Olaria](https://github.com/aolaria).