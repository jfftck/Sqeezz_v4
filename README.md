Sqeezz
======

About
-----

Sqeezz is a dependency management library, it contains modules to handle injection, importing, and simple lifecycle management.
The tools provided are simple, small, and fast to load; this should make little impact on performance but will increase memory usage.

Sqeezz had been created long ago as a personal project and this is the 4th iteration of this library, but this will be the first public release.
The earlier ones were more like revisions and will be renumbered to 0.0.1, 0.0.2, and 0.0.3, due to none of them being a release quality version and more like demos.

This is a complete rewrite of the Sqeezz dependency management library for the current versions of Python, as the older versions were for Python 2.7 and then ported over to Python 3, which left a lot of older libraries being used and had reduced maintainability. Only supported versions of Python are supported by this library, this will be a rolling release model where version number will match the Python versions that is supported. Any released versions of Python that are still the same major version are expected to be supprted.

> Example: Python **3.6** would be the lowest and **3.10** would be the highest versions supported by Sqeezz 1.**36**.**310**.x where x is the point releases for Sqeezz. 

Features
--------

- It is now a package instead of a single file
- Everything is explicit in definition, there is no auto wiring
- Simple functions build up the entire library
- Built with Pythonic design
- All the functions are exposed to allow extension of the library
- No external dependencies outside the standard Python libraries
- Handlers for common validations with the ability to create custom validations

Wishlist
--------

- [ ] Works with multiple flavors of Python (PyPy, Cython, etc...)
- [ ] Support compiling to an executable
- [ ] Translate to other languages (JavaScript/TypeScript, Ruby, Java, etc...)
- [ ] Precompile static code injection and create a production ready copy, this would remove the look-up and reduce memory usage
  - [ ] Precompile multiple code branches from dynamic to static
- [ ] Compile to byte-code based on precompiled static code
- [ ] Precompile any branch of code to remove any unnecessary objects and/or variables to reduce memory usage and increase performance
- [ ] Tree shaking and additional code optimizations

Examples
--------

### Full Example

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
    with using('app') as app:  
        return app.giving('main', app)  


def handlers(create, using):
    create('length.username').assign(lambda user: 6 <= len(user.user_name) <= 32)
    create('length.password').assign(lambda user: 12 <= len(user.password) <= 64)


def resource(register):  
    register('fetch').load('requests')  
    register.load('sqeezz_handlers_validation')
    register.load('sqeezz_handlers_json')


def singleton(register, using):  
    fetch = using('fetch')  

    register('app').load('app.main')  

    with register('user.routes').load('app.routes.users') as user:  
        user.prop('fetch').assign(fetch)  
        user.giving('Users', user)  

    with register('user.model').load('app.models.users') as user:
        user.giving('CreateUser', 'create')
        user.giving('UpdateUser', 'update')
        user.giving('ReturnUser', 'return')


def transient(register, using):  
    register('user.api.one').assign(lambda id: f'/api/users/{id}')  
    register('user.api.all').assign(lambda: '/api/users')  
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
from sqeezz import handlers, resource  


API = resource('user.api')  
API_ALL = API('all')  
API_ONE = API('one')  

json = handlers('json')
required = handlers('required')
length = handlers('length')

UserCreate = json.to(length(resource('user.model.create').static()))  
UserUpdate = json.to(length(required(resource('user.model.update').static())))  
UserReturn = json.parse(resource('user.model.return').static())

fetch = resource()  


class Users:  
    def __init__(self, url_all: API_ALL, url_one: API_ONE):  
        self.__url_all = url_all  
        self.__url_one = url_one  

    def create(self, user: UserCreate):  
        return fetch.post(self.__url_all(), data=user)  

    def delete(self, id: str):  
        return fetch.delete(self.__url_one(id))  

    def get(self, id: str = None) -> UserReturn:  
        if id is not None:  
            return fetch.get(self.__url_one(id))  

        return fetch.get(self.__url_all())  

    def update(self, user: UserUpdate):  
        return fetch.put(self.__url_all(), data=user)  
```

---

#### `/app/models/user.py`

```python
from dataclasses import dataclass

from sqeezz import resource


JSON = resource('sqeezz.json').static()


@dataclass
class CreateUser(JSON.Validator):
    name: JSON.Required[str]
    user_name: JSON.Required[str]
    password: JSON.Required[str]
    email: JSON.Required[str]
    metadata: dict[str, str]


@dataclass
class UpdateUser(JSON.Validator):
    name: str = None
    user_name: str = None
    password: str = None
    email: str = None
    metadata: dict[str, str] = None

    def required(self):
        return self.user_name is not None and (self.name is not None or
                                               self.password is not None or
                                               self.email is not None)


@dataclass
class ReturnUser(JSON.Response):
    name: str
    user_name: str
    email: str
    metadata: dict[str, str] = None
```
