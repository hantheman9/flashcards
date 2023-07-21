# Stage 1: Build the Vue.js application
FROM node:16.11 as build-stage

WORKDIR /app

COPY package*.json ./
COPY yarn.lock ./

RUN yarn install

COPY . .

RUN yarn build

# Stage 2: Set up the Nginx server to serve the Vue.js application
FROM nginx:1.21.1 as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
