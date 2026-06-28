# Usamos la imagen oficial de SDK 10.0
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# Copiamos solo el .csproj primero para optimizar el caché
COPY *.csproj ./
RUN dotnet restore

# Copiamos el resto de los archivos y publicamos
COPY . .
RUN dotnet publish -c Release -o /app/publish

# Imagen final
FROM mcr.microsoft.com/dotnet/aspnet:10.0
WORKDIR /app
COPY --from=build /app/publish .

# Usamos el nombre del dll resultante (generalmente es el nombre de la carpeta)
# Si tu carpeta es TP_ApiGateway, el dll será TP_ApiGateway.dll
ENTRYPOINT ["dotnet", "Microservicio_Login.dll"]