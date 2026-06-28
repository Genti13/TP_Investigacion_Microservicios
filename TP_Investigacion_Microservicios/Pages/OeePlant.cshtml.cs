using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace TP_Investigacion_Microservicios.Pages
{
    public class OeePlantModel : PageModel
    {
        private readonly HttpClient _httpClient;

        public List<EquipmentOeeData> Equipos { get; set; } = new();

        public OeePlantModel(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task OnGetAsync()
        {
            try
            {
                //string urlOee = "http://localhost:5070/api/oee/all-equipment";
                //string urlOee = "http://localhost:8000/api/oee/all-equipment";
                string urlOee = "http://tp-apigateway:8080/api/oee/all-equipment";

                var response = await _httpClient.GetAsync(urlOee);

                if (response.IsSuccessStatusCode)
                {
                    var jsonString = await response.Content.ReadAsStringAsync();

                    var opciones = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };

                    Equipos = JsonSerializer.Deserialize<List<EquipmentOeeData>>(jsonString, opciones) ?? new();
                }
            }
            catch (Exception ex)
            {
                ModelState.AddModelError(string.Empty, $"Error al conectar con Microservicio OEE: {ex.Message}");
            }
        }
    }
    public class EquipmentOeeData
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("nombre")]
        public string Nombre { get; set; } = string.Empty;

        [JsonPropertyName("area")]
        public string Area { get; set; } = string.Empty;

        [JsonPropertyName("disponibilidad")]
        public double Disponibilidad { get; set; }

        [JsonPropertyName("rendimiento")]
        public double Rendimiento { get; set; }

        [JsonPropertyName("calidad")]
        public double Calidad { get; set; }

        [JsonPropertyName("oee")]
        public double Oee { get; set; }
    }
}