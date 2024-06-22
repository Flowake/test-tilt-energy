FROM node:21-alpine3.18

RUN apk add --no-cache libc6-compat

RUN corepack enable
RUN corepack prepare yarn@latest --activate

WORKDIR /app

COPY package.json yarn.lock* .yarnrc.yml ./
RUN yarn install --immutable
