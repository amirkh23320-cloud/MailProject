FROM nginx:alpine

COPY frontend/static /usr/share/nginx/html/static

COPY frontend_docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80