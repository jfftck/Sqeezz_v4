Sqeezz v4
=========

About
-----

Sqeezz is a dependency management library, it contains modules to handle injection, importing, and simple lifecycle management.
The tools provided are simple, small, and fast to load; this should make little impact on performance but will increase memory useage.

This is a complete rewrite of the Sqeezz dependency management library for the current versions of Python, as the older versions were for Python 2.7 and then ported over to Python 3, which left a lot of older libraries being used and had reduced maintainability.
Only supported versions of Python are supported by this library,
this will be a rolling release model where version number will match the lowest Python version point release that is supported.

> Example: Python **3.6** would be the lowest version supported by Sqeezz 4.**3.6**.x where x is the point releases for Sqeezz

Features
--------
- It is now a package instead of a single file
- Everything is explicit in definition, there is no auto wiring
- Simple functions build up the entire library
- Built with Pythonic design
- All of the functions are exposed to allow extention of the library
- No external dependencies outside of the standard Python libraries

Wishlist
--------
- [ ] Works with multiple flavors of Python (PyPy, Cython, etc...)
- [ ] Support compiling to an executable
- [ ] Translate to other languages (JavaScript/TypeScript, Ruby, Java, etc...)

Examples
--------

  1. Basic Setup
    #### `/main.py`
    ```python
    import sqeezz

    
    def main():
        sqeezz.config('.config.app')
        
        app = sqeezz.resource('app')
    
        app().main()
    ```
    ---
    #### `/config/app.py`
    ```python
    def config_init(register):
        register('app').load('.app.main')
        fetch = register('fetch').load_now('.app.utils.fetch')
        model = register('user.model').load('.app.models.user')
        with register('user').load('.app.routes.users') as user:
            user.model = model()
            user.fetch = fetch()
    ```
    ---
    #### `/app/main.py`
    ```python
    from sqeezz import inject, resource
    
    
    UserAPI = resource('user')
    
    
    @inject
    def main(Users: UserAPI):
        users_api = Users()

        # Use the users_api
    ```
    ---
    #### `/app/utils/fetch.py`
    ```python
    import requests
    
    
    delete = requests.delete
    get = requests.get
    post = requests.post
    put = requests.put
    ```
    ---
    #### `/app/routes/users.py`
    ```python
    from sqeezz import future
    
    
    fetch = None
    model = None
    
    
    @future
    class Users:
        def create(self, user: model.UserCreate):
            return fetch.post(model.post_url(), data=user)

        def delete(self, id: str):
            return fetch.delete(model.delete_url(id))

        def get(self, id: str = None):
            if id is not None:
                return fetch.get(model.get_url(id))

            return fetch.get(model.get_all_url())

        def update(self, user: model.UserUpdate):
            return fetch.put(model.put_url(), data=user)
    ```
    ---
    #### `/app/models/user.py`
    ```python
    
    ```