## About Us

- Team Name : `RU LEGION`
- Member1 : `Moontasir Mahmood` - `moontasir042@gmail.com`
- Member2 : `Md Atikur Rahman` - `md.atik.dev@gmail.com`
- Member3 : `Abdullah Al Ghalib` - `abdullah.ice.ru@gmail.com`

## Getting started

### Step-1 : To start project, install docker and from command line run:

- `docker-compose up --build`

The API will then be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Step 2 : Celery

- Note: Here For each command open a new terminal and run each server
- `docker-compose run app sh -c "celery -A core worker -l INFO"`
- `docker-compose run app sh -c "celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"`

### Step 3 : Load Initial Data (For running first time)

- `docker-compose run --rm app sh -c "python manage.py start_periodic_tasks"`
- `docker-compose run --rm app sh -c "python manage.py load_initial_waste_db"`
- `docker-compose run --rm app sh -c "python manage.py load_initial_auth_db"`
- `docker-compose run --rm app sh -c "python manage.py load_some_waste_transfer"` (optional)
