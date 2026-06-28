using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Urls.Add("http://localhost:5080");

Console.WriteLine("[SISTEMA] Microservicio de Login inicializado en http://localhost:5080");

app.MapPost("/login", ([FromBody] LoginRequest request) =>
{
    Console.WriteLine($"\n[LLAMADO RECIBIDO] -> POST /login desde el API Gateway");
    Console.WriteLine($"[PROCESANDO] -> Verificando credenciales para el usuario: '{request.Username}'");

    if (request.Username == "alumno" && request.Password == "unlam")
    {
        Console.WriteLine("[RESULTADO] -> Autenticación EXITOSA. Generando respuesta.");
        return Results.Ok(new
        {
            Success = true,
            Message = "¡Bienvenido al sistema!",
            User = request.Username,
            FakeToken = "token_simulado_microservicios_2026"
        });
    }

    Console.WriteLine("[RESULTADO] -> Autenticación FALLIDA. Contraseña o usuario incorrecto.");
    return Results.Json(new { Success = false, Message = "Credenciales incorrectas" }, statusCode: 401);
});

app.MapFallback((HttpContext context) =>
{
    Console.WriteLine($"\n[ERROR 404 INTERNO] Petición rechazada en el microservicio.");
    Console.WriteLine($"Método recibido: {context.Request.Method}");
    Console.WriteLine($"Ruta recibida: {context.Request.Path}");
    return Results.NotFound("Ruta no encontrada en el microservicio destino");
});

app.Run();

public record LoginRequest(string Username, string Password);