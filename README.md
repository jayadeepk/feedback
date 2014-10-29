## Course Feedback Portal

###### Developers:
- Akhil Reddy Ellore
- Bhanu Prakash Vandana
- Jayadeep Karnati

Developed as a part of project in system softwares laboratory in third semester of B.tech in Computer Science at Indian Institute of Technology, Guwahati.

###### Introduction
- This portal takes feedback about a course from students all year round and displays these to the Professor at the end of the year.

###### Software requirements
- [Python == 2.7](https://www.python.org/downloads/)
- [Django == 1.7](https://pypi.python.org/pypi/Django/1.7)

###### Installation Details
- After installing Python 2.7, download Django 1.7, extract it and install using `python2 setup.py install` inside the source folder.
- Now, clone the repository and go to `feedback/feedback/` folder to find the file 'manage.py'. In the terminal, enter `python2 manage.py migrate` to migrate the database. In case you get any error you might need to enter `python2 manage.py makemigrations feedback` before migrating.
- To run the server, enter `python2 manage.py runserver` in the same folder and to access it type `localhost:8000/Permission` in browser and login.
