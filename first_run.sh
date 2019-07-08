docker volume create serp_db_data
docker volume create serp_redis_data
docker-compose up --build
docker exec -it serp_backend_1 python manage.py makemigrations
docker exec -it serp_backend_1 python manage.py migrate
docker exec -it serp_backend_1 python manage.py createsuperuser