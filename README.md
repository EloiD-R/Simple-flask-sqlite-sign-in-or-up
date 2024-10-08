# Simple flask - sqlite - signin/up :

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

# // Todo : remake the readme when i'll need to add the email code sender and all