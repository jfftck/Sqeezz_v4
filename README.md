Sqeezz
======

About
-----

Sqeezz is a dependency management library, it contains modules to handle injection, importing, and simple lifecycle management.
The tools provided are simple, small, and fast to load; this should make little impact on performance but will increase memory usage.

Sqeezz had been created long ago as a personal project and this is the 4th iteration of this library, but this will be the first public release.
The earlier ones were more like revisions and will be renumbered to 0.0.1, 0.0.2, and 0.0.3, due to none of them being a release quality version and more like demos.

This is a complete rewrite of the Sqeezz dependency management library for the current versions of Python, as the older versions were for Python 2.7 and then ported over to Python 3, which left a lot of older libraries being used and had reduced maintainability.
Only supported versions of Python are supported by this library, this will be a rolling release model where version number will match the lowest Python version point release that is supported.

> Example: Python **3.6** would be the lowest version supported by Sqeezz 1.**3.6**.x where x is the point releases for Sqeezz

Features
--------
- It is now a package instead of a single file
- Everything is explicit in definition, there is no auto wiring
- Simple functions build up the entire library
- Built with Pythonic design
- All the functions are exposed to allow extension of the library
- No external dependencies outside the standard Python libraries

Wishlist
--------
- [ ] Works with multiple flavors of Python (PyPy, Cython, etc...)
- [ ] Support compiling to an executable
- [ ] Translate to other languages (JavaScript/TypeScript, Ruby, Java, etc...)

Examples
--------
### Basic Setup
#### `/main.py`
```python
import sqeezz


app = sqeezz.config('config.app')


def main():
    app()


if __name__ == '__main__':
    main()
```
---
#### `/config/app.py`
```python
def bootstrap(using):
    return using('app').func('main')


def resource(register):
    register('fetch').load('requests')


def singleton(using, register):
    fetch = using('fetch')
    routes = using('user.routes')

    with register('app').load('app.main') as app:
        app.func('main').assign(routes)
    
    with register('user.routes').load('app.routes.users') as user:
        user.prop('fetch').assign(fetch)


def transient(using, register):
    register('user.api.one').assign(lambda id: f'/api/users/{id}')
    register('user.api').assign(lambda: '/api/users')
```
---
#### `/app/main.py`
```python
from sqeezz import resource


UserAPI = resource('user.routes')


def main(Users: UserAPI):
    users_api = Users()

    # Use the users_api
```
---
#### `/app/routes/users.py`
```python
from sqeezz import future, inject, resource


API = resource('user.api')
API_ONE = resource('user.api.one')

UserCreate = resource('user.model.create').check_instance()
UserUpdate = resource('user.model.update').check_instance()

fetch = None


class Users:
    def __init__(self, url: API, url_one: API_ONE):
        self.__url = url
        self.__url_one = url_one
    
    def create(self, user: UserCreate):
        return fetch.post(self.__url(), data=user)

    def delete(self, id: str):
        return fetch.delete(self.__url_one(id))

    def get(self, id: str = None):
        if id is not None:
            return fetch.get(self.__url_one(id))

        return fetch.get(self.__url())

    def update(self, user: UserUpdate):
        return fetch.put(self.__url(), data=user)
```
---
#### `/app/models/user.py`
```python

```