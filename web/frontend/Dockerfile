FROM node:20-alpine

WORKDIR /app

COPY web/frontend/package.json web/frontend/package-lock.json ./
RUN npm ci

COPY web/frontend ./

EXPOSE 5173
CMD ["npm", "run", "dev"]
