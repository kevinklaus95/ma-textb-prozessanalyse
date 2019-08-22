# first part - create production build
FROM node:8 as build-stage

ADD yarn.lock /yarn.lock
ADD package.json /package.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN yarn

WORKDIR /app
ADD . /app

RUN yarn build

# second part - put production build into nginx' context and serve it
FROM nginx:1.15.9-alpine
COPY default.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]