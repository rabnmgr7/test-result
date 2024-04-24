FROM nginx:latest
EXPOSE 80
RUN apt update -y \
    && apt install curl -y
RUN mkdir -p /app/static/images/
COPY ./logo_pu.png /app/static/images/logo_pu.png
CMD ["nginx", "-g", "daemon off;"]