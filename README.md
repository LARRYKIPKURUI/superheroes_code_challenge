# Superheroes API

A simple Flask API for managing superheroes, their powers, and associated strengths.

## Features

- View all heroes and specific hero details
- View all powers and update power descriptions
- Assign powers to heroes with varying strength levels

## Endpoints

- `GET /heroes` — List all heroes
- `GET /heroes/<id>` — Get a specific hero (with powers)
- `GET /powers` — List all powers
- `GET /powers/<id>` — Get or update a specific power
- `POST /hero_powers` — Assign a power to a hero

## Setup

```bash
git clone https://github.com/LARRYKIPKURUI/superheroes_code_challenge.git
cd superheroes_code_challenge

pipenv install && pipenv shell

cd server
 flask run 
 python seed.py
 flask db upgrade head

``` 
## Aurthor
Kipkurui Larry
