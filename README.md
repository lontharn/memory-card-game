# Memory Card Game
A minimal memory card game app developed with [Flask](http://flask.pocoo.org/) framework.

* Python
* Flask
* Flask-JWT
* flask-restplus
* flask-sqlalchemy

## Project Structure
  ```sh
  ├── README.md
  ├── app.Dockerfile
  ├── docker-compose.yml
  ├── autoapp.py
  ├── config.py
  ├── requirements.txt
  ├── app
  │   ├── __init__.py
  │   ├── jwt.py 
  │   ├── models.py 
  │   ├── api_v1
  │   │   ├── __init__.py
  │   │   ├── routes.py
  │   │   └── serializers.py
  │   ├── static
  │   │   ├── images
  │   │   │   └── bluePid.jpeg
  │   │   ├── index.css
  │   │   └── index.js
  │   └── templates
  │       └── index.html
  └── tests
          ├── test_routes.py
          ├── test_db.py
          └── conftest.py
  ```

## Running with docker-compose
```
>> docker-compose up
```
* http://127.0.0.1:5000 to play the game.
* http://127.0.0.1:5000/api/v1/doc to open swagger ui document
![Demo swagger ui](https://user-images.githubusercontent.com/12784602/86539802-b6396300-bf29-11ea-94c7-a4ba442eadbe.png)


### Testing with docker-compose
```
docker exec -i -t memory-card-game_app_1 flask test
```
