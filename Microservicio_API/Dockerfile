FROM python:3.13

ENV DEBIAN_FRONTEND=noninteractive

# 1. Instalar dependencias base
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar el driver ODBC para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 3. CREAR ARCHIVO DE CONFIGURACIÓN OPENSSL PERSONALIZADO
# Esto baja el nivel de seguridad a 0 y permite TLSv1 para SQL Server 2014
RUN echo "openssl_conf = default_conf" > /etc/ssl/openssl_custom.cnf && \
    echo "" >> /etc/ssl/openssl_custom.cnf && \
    echo "[default_conf]" >> /etc/ssl/openssl_custom.cnf && \
    echo "ssl_conf = ssl_sect" >> /etc/ssl/openssl_custom.cnf && \
    echo "" >> /etc/ssl/openssl_custom.cnf && \
    echo "[ssl_sect]" >> /etc/ssl/openssl_custom.cnf && \
    echo "system_default = ssl_default_sect" >> /etc/ssl/openssl_custom.cnf && \
    echo "" >> /etc/ssl/openssl_custom.cnf && \
    echo "[ssl_default_sect]" >> /etc/ssl/openssl_custom.cnf && \
    echo "MinProtocol = TLSv1" >> /etc/ssl/openssl_custom.cnf && \
    echo "CipherString = DEFAULT:@SECLEVEL=0" >> /etc/ssl/openssl_custom.cnf

# 4. Forzar al sistema a usar la configuración personalizada
ENV OPENSSL_CONF=/etc/ssl/openssl_custom.cnf

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "runserver.py"]