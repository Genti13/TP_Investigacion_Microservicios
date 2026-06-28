using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace TP_Investigacion_Microservicios.Pages
{
    public class DashboardModel : PageModel
    {
        private readonly HttpClient _httpClient;
        public DashboardData Metricas { get; set; } = new();
        public DashboardModel(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task OnGetAsync()
        {
            try
            {
                //string pythonDashboardUrl = "http://localhost:5060/api/dashboard/metrics";
                //string pythonDashboardUrl = "http://localhost:8000/api/dashboard/metrics";
                string pythonDashboardUrl = "http://tp-apigateway:8080/api/dashboard/metrics";

                var response = await _httpClient.GetAsync(pythonDashboardUrl);
                if (response.IsSuccessStatusCode)
                {
                    var jsonString = await response.Content.ReadAsStringAsync();
                    var opciones = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                    Metricas = JsonSerializer.Deserialize<DashboardData>(jsonString, opciones) ?? new DashboardData();
                }
            }
            catch (Exception ex)
            {
                ModelState.AddModelError(string.Empty, $"No se pudo cargar el Dashboard: {ex.Message}");
            }
        }
    }

    public class DashboardData
    {
        [JsonPropertyName("titulo")]
        public string Titulo { get; set; } = string.Empty;

        [JsonPropertyName("datos")]
        public Dictionary<string, double> Datos { get; set; } = new();

        [JsonPropertyName("total_procesado")]
        public int TotalProcesado { get; set; }

        [JsonPropertyName("estado_sistema")]
        public string EstadoSistema { get; set; } = string.Empty;
    }
}