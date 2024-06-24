# pizzapy-website

Codebase for Official PizzaPy Website

## Installation

### Prerequisites

- [Python 3.11^](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

### Setup

Python dependencies:

```bash
python -m venv venv         # creates a Virtual Environment inside the /venv directory
./venv/Scripts/activate     # activates the venv, to exit, type "deactivate" || for MAC: source venv/bin/activate
pip install -r requirements.txt # installs all the Python dependencies
```

JavaScript dependencies:

```bash
cd PizzaPyWebApp/js_lib
npm install
```

## Usage

Once you've installed the dependencies, you can now run the application or build scripts.

```bash
cd PizzaPyWebApp/
python manage.py runserver
```

If you want to watch for TailwindCSS changes, run the following commands in **another terminal instance**:

```bash
cd PizzaPyWebApp/js_lib/
npm run watch
```

This will create a `/PizzaPyWebApp/static/css/output.css` stylesheet based on the `/PizzaPyWebApp/js_lib/input.css` file.

## Side Notes

```txt
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
```
