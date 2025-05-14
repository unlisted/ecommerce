POC of a small e-commerce application

## Items
- Items are commodity like, meaning there could a lot of the same thing.

## Reservations
- Each reservation represents a single item (currently, this will change).
- Each reservation is associated with a single member.


# Testing
Use a Postgres instance running on bare-metal or a container that exposes the port
```
(venv) ~/d/m/ecommerce$>dotenv run docker compose run --service-ports -d postgres
```
