using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Text;
using System.Text.Json;

namespace TP_Investigacion_Microservicios.Pages
{
    public class LoginModel : PageModel
    {
        [BindProperty]
        public string Username { get; set; }

        [BindProperty]
        public string Password { get; set; }

        public string ErrorMessage { get; set; }

        public void OnGet()
        {
        }

        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            using var httpClient = new HttpClient();

            string gatewayUrl = "http://127.0.0.1:8000/api/login";

            var loginData = new
            {
                Username = this.Username,
                Password = this.Password
            };

            var jsonContent = new StringContent(
                JsonSerializer.Serialize(loginData),
                Encoding.UTF8,
                "application/json"
            );

            try
            {
                Console.WriteLine($"[FRONTEND] Enviando POST a {gatewayUrl}...");

                var response = await httpClient.PostAsync(gatewayUrl, jsonContent);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("[FRONTEND] Login exitoso. Redirigiendo al inicio.");
                    return RedirectToPage("/Index");
                }
                else
                {
                    Console.WriteLine("[FRONTEND] Login rechazado por el microservicio.");
                    ErrorMessage = "Usuario o contraseña incorrectos.";
                    return Page();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[FRONTEND] Error de conexión: {ex.Message}");
                ErrorMessage = "El API Gateway no está respondiendo. ¿Está encendido YARP?";
                return Page();
            }
        }
    }
}