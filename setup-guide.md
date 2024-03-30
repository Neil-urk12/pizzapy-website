** Python version 3.11^ **

Initial Setup (NEED TO DO)

- venv
  python -m venv venv_name

- activating the script
  venv_name\Scripts\activate
  (to exit, type deactivate)

- to install all packages
  pip install .

RUN django project
(in the PizzaPyWebApp dir)
python manage.py runserver

""" SIDE NOTES: """

Django setup
django-admin startproject project_name
python manage.py startapp app_name

Writes all python dependecies for tracking only (and deployment)
python -m pip freeze > requirements.txt

Installing of packages
pip install package_name

For production to collect static files
python manage.py collectstatic

Removing files from the repo and not locally

directory
git rm --cached -r venv
rm 'venv'

files
git rm --cached venv
rm 'venv'

do the git ignore and remove at the same the time
git rm --cached (git ls-files -i -c -X .gitignore)
rm 'venv'
rm '/PizzaPyWebApp/js_lib/node_modules'
