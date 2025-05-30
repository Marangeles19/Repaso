# Construcción de la app con Node.js
FROM node:20 AS build

WORKDIR /app

# Copiar archivos de dependencias e instalar
COPY client/package.json client/package-lock.json ./
RUN npm install --frozen-lockfile

# Copiar el código y compilar
COPY client ./
RUN npm run build

# ------------------- #
# Servir la app con un servidor ligero como nginx
FROM nginx:alpine

WORKDIR /usr/share/nginx/html
COPY --from=build /app/dist ./

# Exponer el puerto 80 para servir la aplicación
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]