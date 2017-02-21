

# recipes

recipes is a _short description_. It is built with [Python][0] using the [Django Web Framework][1].

This project has the following basic apps:

* Recipe APIs - http://localhost:8000/apis/recipes/

## Installation

### Quick start

To set up a development environment quickly, first install Python 3. It
comes with virtualenv built-in. So create a virtual env by:

    1. `$ python3 -m venv recipes`
    2. `$ . recipes/bin/activate`

Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate

### Detailed instructions

Take a look at the docs for more information.

**Request Body**

        {
            "title": "",
            "ingredient": [],
            "preparation": "",
            "time_for_preparation": null,
            "number_of_portions": null,
            "difficulty": null,
            "categories": [],
            "comment": []
        }


**Response Body**


[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
