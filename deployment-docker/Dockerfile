FROM node:21-alpine3.17
WORKDIR /app
EXPOSE 3000

COPY package*.json ./
RUN echo "MONGO_URI=mongodb://127.0.0.1:27017" > .env
RUN mkdir node_modules
RUN npm install 

COPY . .
CMD ["node", "index.js"]
