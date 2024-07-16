# Pet_AirportAPIService

The MateAcademy DRF-API project

![airport_diagram](airport_diagram.webp?raw=true)

## How to run

1. Set in .env file variables:
   - POSTGRES_PASSWORD=`your_variable`
   - POSTGRES_USER=`your_variable`
   - POSTGRES_DB=`your_variable`
   - POSTGRES_HOST=`your_variable`
   - POSTGRES_PORT=`your_variable` (`5432` by default)
   - PGDATA=`your_variable` (`/var/lib/postgresql/data` by default)

2. Install Docker
3. Run commands: 
   - `docker-compose build`
   - `docker-compose up`
4. Go to `127.0.0.1:8001/api/`

## Getting access
- create user via api/user/register/
- get access token via api/user/token/

## Features
- JWT authenticated
- Admin panel `/admin/`
- Documentation is located at `/api/schema/` and `/api/schema/swagger-ui/`
- Managing orders and tickets being authenticated
- Order list is paginated
- Creating _airports_, _routes_, _crew_, _airplanetypes_, _airplanes_, _flights_ with only is_staff permitions
- Filtering flights with _sources_, _destination_ and _departure time_
- Trottle for unauthenticated and authenticated users with different settings
