_# Simple flask - sqlite - signin/up :

## Technical "facts" :

### Tech stack :
- DB : sqlite
- programming language : python
- web server management : flask


### Architecture :
(not definitive)
```
Simple-flask-sqlite-sign-in-or-up
├── App
│   ├── home.py
│   ├── index.py
│   └── utils
│       └── db
│           └── user_db.py
├── README.md
├── main.py
├── templates
│   ├── home.html
│   └── index.html
└── user_db.db
```

### Features :
- check if the user's signed in before loading anything, if not, redirect him to signing page
- determine automatically based on email if the user needs to sign in or sign up, load form accordingly
- load form part by part as the user's filling the form
- create an account
- login to an account


### Session cookies :
- "login_state" : bool, determines if the user's connected or not
- "email"/"name" : str, if the user's not connected -> None | else -> email/name loaded in session after signing in/up
- "signing_state" : str, used by signing_manager.py and signing.html, can be "sign_in" or "sign_up", determines the type of signing
- "signing_phase" : int, used by signing_manager.py and signing.html, can be from 1 (username) to 2/3 (depends on password or password confirm for sign_up, on sign_in only gos to 1 : password), determines the inputs to load


## userDB
// Todo : document

## Python files :

### main.py
> - at each refresh via @flask_app.teardown_appcontext : close user_db and check if user's logged via session['login_state']
> - managing db -> opening it when needed and closing it at each tear down (errors, closing website, ...)
> - defining routes for sign page, 404 and home -> func to check if user's connected, if yes, proceed to everything else,
otherwise redirect to sign.in.up,
> if error (ex: 404): if user's connected : redirect him to the error, else : redirect him to sign.in.up,
> so basically, whatever the user's doing, if he's not connected he will be redirected to the sign.in.up page, 
> excepted if he goes to the index
##### Routes:
- [index](#appindexpy)
- [home](#apphomepy)
- [sign.in.up](#appsigning_managerpy)
- [404](#404)

### App/index.py
> Basically contains a function to call to render home page
##### Functions list
  - load() :
    - [Load index.html](#indexhtml)


### App/home.py
> Basically contains a function to call to render home page
##### Functions list
  - load() :
    - [Load home.html](#homehtml)

### App/signing_manager.py
##### Sign up :
> For the password, I don't want to send it back and forth between client and server especially in cookies, so I just store

## HTML files (located in /templates) :

##### index.html
  - if user's logged in : display a **go to home** button, else : display a **go to sign in/up** button

##### home.html
  - showing infos about the user that are stored in the cookies (email, username)
  
### HTTP errors :
##### 404
> returns the error_
