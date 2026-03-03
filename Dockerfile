FROM node:22-slim
WORKDIR /app
RUN npm install -g serve
COPY dist/ ./dist/
EXPOSE 3000
CMD ["serve", "dist", "-l", "3000", "-s"]
