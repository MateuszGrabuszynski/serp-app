<!--TODO: Check before sending-->
# Appchance SERP recruitment task
**Author:** Mateusz Grabuszyński  
**E-mail:** mgrabuszynski@gmail.com

## How to run
First run:
```
docker-compose up --build
docker exec -it serp_backend_1 python manage.py makemigrations
docker exec -it serp_backend_1 python manage.py migrate
docker exec -it serp_backend_1 python manage.py createsuperuser
```

Later:
```
docker-compose up
```

## Explain
* Normally, I should not add `.env` file with `SECRET_KEY` here because of security, but it's more convenient to do it like that right now.
* `no` is often used as an abbreviation of `number_of`, so i.e. `no_results` is `number_of_results`