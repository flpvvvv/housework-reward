#!/bin/bash

# Recreate config file
rm -rf /usr/share/nginx/html/config.js
touch /usr/share/nginx/html/config.js

# Add assignment
echo "window._env_ = {" >> /usr/share/nginx/html/config.js

# Read environment variables and set them in config.js
echo "  REACT_APP_API_BASE_URL: \"$REACT_APP_API_BASE_URL\"," >> /usr/share/nginx/html/config.js
echo "  REACT_APP_MINIO_ENDPOINT: \"$REACT_APP_MINIO_ENDPOINT\"," >> /usr/share/nginx/html/config.js

echo "}" >> /usr/share/nginx/html/config.js
