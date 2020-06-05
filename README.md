# Geo Distance Web Application
This is quite simple application allows pick up geo points from google map and calculate distance between them using geodesic algorithm.
It allows type text adresses as well. Note that focused (where cursor is) input counts as current one, so you could control what the point you are picking.

#### Challenges
- proper Google Maps API configuration
- responsive and essential UX

#### TODO
- improve React Hooks-based state testability 

## SetUp and Run
- `$ docker-compose build`
- `$ docker-compose up`
- visit localhost:3000

## API
### Tests
`$ python backend/manage.py test`

## Frontend
### Tests
```
$ cd frontend
$ npm test
```