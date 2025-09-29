Install Docker (if not already installed)

Download Docker Desktop for Mac (free): https://www.docker.com/products/docker-desktop

Verify installation:
docker --version
docker pull postgres:16
docker run --name my_postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -d postgres:16


Explanation:

--name my_postgres → container name

-e POSTGRES_USER=admin → username

-e POSTGRES_PASSWORD=secret → password

-e POSTGRES_DB=mydb → database created at startup

-p 5432:5432 → maps Postgres port to your Mac

-d → run in background

docker ps
docker stop my_postgres
docker start my_postgres

Connect to PostgreSQL
docker exec -it my_postgres psql -U admin -d mydb


Persist Data with a Volume
docker run --name my_postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=mydb \
  -v $HOME/postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres:16



docker-compose.yml

version: "3.9"

services:
  postgres:
    image: postgres:16
    container_name: my_postgres
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:


Start Postgres in the background:
docker-compose up -d
docker-compose logs -f
docker-compose down
docker-compose down --volumes=false
docker-compose down -v

