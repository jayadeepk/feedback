## Course Feedback Website

##### Summary
This website takes feedback from the students on each course they are alloted to and on their professors. Professors can view these feedbacks along with statistics. Admin can allot students and professors to courses and modify questions.

##### Software requirements
- [Python == 2.7](https://www.python.org/downloads/)
- [Django == 1.7](https://pypi.python.org/pypi/Django/1.7)
- [Django-Graphos](https://github.com/agiliq/django-graphos)
- [Django-Nocaptcha-Recaptcha](https://github.com/ImaginaryLandscape/django-nocaptcha-recaptcha)

Note that while logging in as student/professor, the server needs to be connected to internet, as required by django-nocaptcha-recaptcha.

##### Installation
- After installing Python 2.7, download Django 1.7, extract it and install using `python2 setup.py install` inside the source folder.
- Now, clone the repository and go to `feedback/feedback/` folder to find the file 'manage.py'. In the terminal, enter `python2 manage.py migrate` to migrate the database. In case you get any error you might need to enter `python2 manage.py makemigrations feedback` before migrating.
- To run the server, enter `python2 manage.py runserver` in the same folder and to access it type `localhost:8000/feedback` in browser and login.
