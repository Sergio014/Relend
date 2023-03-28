# Relend
Marketplace
A simple marketplace to sell/buy accounts in mobile games, to run it you need:
1. create .env file in base directory with TOKEN1 variable(for telegram bot) and DJANGO_SECRET_KEY for django project
2. Run:
  -python manage.py makemigrations
  -python manage.py migrate
  -python manage.py runserver
3. In second terminal run python manage.py bot to run a telegram bot
