#setup nginx
FROM nginx:stable-alpine

# #remove any existing config files
RUN rm -rf /etc/nginx/conf.d/*
# ## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*
# #copy default from dev
COPY /docker/nginx/dev/default.conf /etc/nginx/conf.d/

# #COPY --from=build /app/frontend/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]