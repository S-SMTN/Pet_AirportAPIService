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
