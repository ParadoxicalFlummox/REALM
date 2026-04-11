# Stage 1: build the Vue app
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# In Docker, nginx proxies /api/ to the backend — no hostname in the URL needed.
ARG VITE_API_URL=/api
ARG VITE_COMPANY_NAME=TAP·re
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_COMPANY_NAME=$VITE_COMPANY_NAME

RUN npm run build

# Stage 2: serve with nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
