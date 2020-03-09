# MyFit

## 1. requirements

- Python3 >= 3.7.0.
- Pip3:
```
pip3 install -r requirements.txt                            # install all needed packages 
```

## 2. database set up
```
python manage.py makemigrations fitness_app
python manage.py sqlmigrate fitness_app 0001
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_db                                # fills db with default data
```

## 3. run
```
python manage.py runserver                                  # default port 8000
```
- access website http://localhost:8000/fitness

## 4. tests
```
python manage.py test -v 2                                  # all tests
python manage.py test -v 2 fitness_app.tests.tests_ut       # only ut's
```

## 5. covarage
```
coverage run --source='.' manage.py test                    # generate coverage
coverage report --omit="*/test*,*/management*"              # view report
coverage html --omit="*/test*,*/management*"                # generate full html report
```

## 6. documentation
generate models diagram:
```
./manage.py graph_models -a -I User,Goals,Activity,Sport,Meal,Portion,Food,  -o models.png
```