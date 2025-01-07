FROM nginx:1.24-alpine AS proxy

LABEL maintainer="AI-AGENT" \
      version="1.0" \
      description="Nginx - Production-Ready Reverse Proxy for React Application"

# Set working directory
WORKDIR /etc/nginx

# Install required tools and create necessary directories
RUN apk add --no-cache curl openssl && \
    mkdir -p /var/run/nginx \
             /var/cache/nginx \
             /var/cache/nginx/cache \
             /var/log/nginx \
             /etc/nginx/conf.d \
             /etc/nginx/ssl \
             /var/www/certbot \
             /usr/share/nginx/html

# Generate SSL certificate before changing user
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Copy configuration files
COPY --chown=nginx:nginx ./nginx/nginx.conf /etc/nginx/
COPY --chown=nginx:nginx ./nginx/security-headers.conf /etc/nginx/
COPY --chown=nginx:nginx ./nginx/mime.types /etc/nginx/
COPY --chown=nginx:nginx ./nginx/proxy.conf /etc/nginx/

# Set permissions after all files are in place
RUN chown -R nginx:nginx /var/run/nginx \
                        /var/cache/nginx \
                        /var/log/nginx \
                        /etc/nginx \
                        /usr/share/nginx/html \
                        /var/www/certbot && \
    chmod -R 755 /etc/nginx && \
    chmod 644 /etc/nginx/ssl/nginx.crt && \
    chmod 640 /etc/nginx/ssl/nginx.key && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

# Switch to non-root user
USER nginx

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Expose ports
EXPOSE 80 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]