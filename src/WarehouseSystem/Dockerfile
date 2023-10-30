FROM node:20.9.0-slim

WORKDIR app

COPY package-lock.json .
COPY package.json .
COPY system.js .

RUN npm install

CMD ["node", "system.js"]