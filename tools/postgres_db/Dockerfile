FROM postgres:12-alpine
ENV POSTGRES_PASSWORD ahomepass123
ADD init_00_creater_used_and_db.sql /docker-entrypoint-initdb.d/
EXPOSE 5432