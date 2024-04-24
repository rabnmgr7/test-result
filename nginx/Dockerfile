FROM nginx:latest
EXPOSE 80
RUN apt update -y \
    && apt install curl -y
RUN mkdir -p /app/static/images/
CMD ["nginx", "-g", "daemon off;"]