using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args); // Usa el Builder estándar para YARP

// 1. Forzar a que el Gateway escuche en el puerto 8000
builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenLocalhost(8000);
});

// 2. Cargar el motor de YARP leyendo el archivo appsettings.json
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

var app = builder.Build();

// 3. Habilitar el ruteo del proxy inverso
app.MapReverseProxy();

app.Run();