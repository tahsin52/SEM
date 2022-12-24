# Project Setup



```bash 
$ git clone
$ python3 -m venv venv or virtualenv venv
$ source venv/bin/activate or venv\Scripts\activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

# First Of All

```bash
    GET  /api/get_data/ verilen linkteki verileri çeker ve json dosyasına yazar ve gösterir (1-3 min)
    POST /api/data/ verileri database e kaydeder sadece post isteği atmak yeterli
    GET  /api/data/ verileri listeler ve gösterir
```
```bash
    query parametreleri
    GET /api/data/?make ?model= , ?year= , ?exterior_color= , ?make= , ?count= , ?transmission= 
    
    çoklu query
    GETT /api/data/?make=BMW&model=X6&year=2022&exterior_color=Black&transmission=Automatic
```