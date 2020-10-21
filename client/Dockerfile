FROM node:10
WORKDIR /usr/src/app/ui
COPY ./package*.json ./
RUN npm install
RUN npm install -g http-server
RUN npm install --save-dev webpack
RUN npm install --save-dev webpack-dev-server 
RUN npm install --save-dev webpack-cli
COPY . .
EXPOSE 8081
CMD ["npm", "test:dev"]
