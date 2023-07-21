

# Shortform - Mini Project

## What is currently done
- The web app is availabale here [https://flashcardapp-fe-uhrgp63gla-uc.a.run.app/](https://flashcardapp-fe-uhrgp63gla-uc.a.run.app/)
- Study interface is implemented as required.
- Admin interface is implemented as required + Full flashcard CRUD capabilities.
- Implemented Multiple users.
- Implemented as a single-page app.
- The backend is hosted on Google Cloud Run, connected to a Postgres instance (both reside in the same VPC).
- The frontend is exposed to the public internet (makes use of gcp ingress and LB), hosted on a different Cloud Run instance, communicating securely with the backend (they also reside in the same VPC)
- The infrastructure is implemented in Terraform, Bash, and "few" ClickOps.

## Future improvements
- Add CI/CD (GH actions will be do), to automate building/ pushing images, and re-deploying to cloudrun 
- Make the UI look better. This is where i'm not an expert so I didn't spend much time
- For the study interface, it would be better to load the flashcards in a sorted qeue instead of calling the backend every time.
- Move completetly away from Cloud Run and run it on Kubernetes. For better scale, lower cost, code structure, and easier dev experience.
- I can keep mentioning more improvements depending on how far we want to go:) but for now, I think what I mentioned (especially improving the UI) would be enough given that we are looking to build an MVP

# Setup

Backend is powered by Flask, flask-rest-api, marshmallow and SQLAlchemy to create a solid framework for REST API backend development:

- Application structure
- Routing
- Data validation, serialization and de-serialization
- DB layer with ORM and migrations
- API documentation with apispec and Swagger
- Testing with pytest

Backend setup:

- [Flask 2](http://flask.pocoo.org/)
- [SQLAlchemy 1.4](https://www.sqlalchemy.org/) and [PostgreSQL 13.0](https://www.postgresql.org/)
- [Marshmallow 3](https://marshmallow.readthedocs.io/) for validation and serialization
- Testing with [pytest](https://docs.pytest.org/en/latest/)
- Linting with [mypy](http://mypy-lang.org/), [flake8](http://flake8.pycqa.org/en/latest/) and [black](https://github.com/ambv/black)
- Code formatting with [black](https://github.com/ambv/black)

Frontend setup:

- [Vue.js 2.6](https://v2.vuejs.org/) with [vue-cli 4.0](https://cli.vuejs.org/)
- [Typescript 3.4.5](https://www.typescriptlang.org/)
- [axios](https://github.com/axios/axios) for HTTP requests
- [bootstrap-vue](https://bootstrap-vue.js.org/) for UI
- Testing with [jest](https://jestjs.io/)
- Linting with typescript, eslint and prettier
- Code formatting with prettier

Note: on linux, to fix permissions between host / docker shared containers, it is necessary to export `$UID` and `$GID` variables, this can be done in ~/.bashrc or ~/.zshrc.
This is because UID and GID are shell variables, not env variables.
It allows to have dependencies (python venv and node.js node_modules shared from the container to the host, so we can have IDE completion on the host, or just easily access the dependencies from the editor).
See also: https://github.com/docker/compose/issues/2380.

Backend dependencies are in `backend/venv` and frontend dependencies are in the `frontend/node_modules`.

# Local Setup

- Rebuild images / reinstall dependencies: `make build`
- Run docker compose setup: `make up`
- Create the initial DB (once the setup is running): `make recreate-local-db`
- Run linters: `make lint`
- Run tests: `make test`

Reformat sources: `make format-code`.

# Backend DB Migrations

DB migrations are handled by [alembic](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) and [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/).

`Flask-Migrate` runs migrations in the context of flask application, to use it, run `make backend-bash` and then use one of the following commands:

- `flask db migrate -m "change description"` - generate new migrations from models
- `flask db upgrade` - apply migrations to the database
- `flask db downgrade` - downgrade the database
- `flask db --help` - get help and list of available commands
