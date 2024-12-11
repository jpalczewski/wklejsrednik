# syntax = docker/dockerfile:1
FROM node:16.15.1-alpine AS appbuild
WORKDIR /app
COPY package.json yarn.lock tsconfig.json schema.graphql ./
#COPY .babelrc ./
RUN --mount=type=cache,id=yarn,target=/usr/local/share/.cache/yarn  mkdir "/node" && \
     yarn install  && \
     adduser --disabled-password  app && \
     chown -R app:app /app /node && \
     sed -i "s/localhost:8000/backend:8000/g" package.json
COPY src/ ./src/
COPY public/ ./public/

RUN yarn relay

USER app

CMD yarn fast-start

# Build Stage 2
# FROM node:10.15.2-alpine

# WORKDIR /usr/src/app

# COPY package.json ./

# COPY .babelrc ./

# RUN yarn

# #COPY --from=appbuild /usr/src/app/dist ./dist
# COPY --from=appbuild /usr/src/app/ .

# EXPOSE 4002

# CMD yarn start
