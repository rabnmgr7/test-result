FROM nginx:latest
EXPOSE 80
RUN apt update -y \
    && apt install curl -y
CMD ["nginx", "-g", "daemon off;"]