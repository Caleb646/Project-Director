FROM nginx:stable-alpine
#Remove any existing config files
RUN rm -rf /etc/nginx/conf.d/*
#Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*
#Copy default config from dev folder
COPY /docker/nginx/staging/default.conf /etc/nginx/conf.d/

# #COPY --from=build /app/frontend/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]