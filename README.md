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
##### Functions :
- load(user_db)
  - initialize a dictionary called feedback_messages, essentially storing the errors or success messages for each input field on the html
  - gets the email with get_input
  - calls check_email
    - if email's alright :
      - determine signing state and sets the email's feedback message to valid
      - determines signing phase
    - if email's not alright : email's feedback message is changed to an error
    - if there are no email : do 
    
    - if state is sign up
        - if phase is less than 0:
          - get_input(username)
        - if it is more than 1:
          - get_input(password) # Not definitive cause we don't want the password to be in the cookies
        
    - if state is sign in
      - // todo : password
    
  - renders the template and gives it the feedback messages

- get_input(field)
  - get input of field from the form, if it's None, tries to get it from cookies, if it's something puts it in cookies. This is due to the @before_request verification which otherwise creates a strange bug i haven't really understood but basically, it doesn't work anymore or only if the cookies are already initiated, i really don't know why but it is base on the fact that the page is doing the request two times and so the form is reset and yeah...
  
- determine_signing_state(user_db, email), needs an already checked email, basically go through all emails in userdb 
and checks if the given one is matching one of them, if yes returns "sign_in", else returns "sign_up"
determine_signing_phase()

- if state is sign_in : returns 1 bc phase 1 is password for sigin in
check_email(email)

- if there are no email : return None, if there is : if it matches the regex pattern : return True, else : return False
 
 
## HTML files (located in /templates) :

##### index.html
  - if user's logged in : display a **go to home** button, else : display a **go to sign in/up** button

##### home.html
  - showing infos about the user that are stored in the cookies (email, username)
  
### HTTP errors :
##### 404
> returns the error

# Add a verif so cookies are cleared and email's re put in cookies if signing state changes
