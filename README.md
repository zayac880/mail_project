### Installation

Type in terminal:

```sh
$ git clone гыты клонЭ ссылка
$ cd mail_project
```

Install all dependencies:

```sh
$ poetry install
```

Custom commands:

- Create SuperUser
```sh
$ python manage.py create_su 
```

- Load initial countries 
```sh
$ python manage.py load_countries
```

- Send mail once  
```sh
$ python manage.py send_mail <mailing pk> 
```


