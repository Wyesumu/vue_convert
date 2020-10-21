FROM node:11.12.0-alpine as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
RUN npm install
COPY ./client .
RUN npm run build

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./ .

CMD gunicorn -b 0.0.0.0:5000 app:app --daemon
CMD npm run dev
