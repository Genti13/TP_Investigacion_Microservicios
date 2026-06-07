using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Text;
using System.Text.Json;

namespace TP_Investigacion_Microservicios.Pages
{
    public class ReportModel : PageModel
    {
        private readonly HttpClient _httpClient;
        public ReportModel(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public void OnGet()
        {
        }
        public async Task<IActionResult> OnPostGenerarReporteAsync()
        {
            try
            {
                //string pythonUrl = "http://localhost:5050/api/reportes/decorado";
                string pythonUrl = "http://localhost:8000/api/reportes/decorado";
                var datosReporte = new
                {
                    titulo = "Reporte de Investigación de Microservicios",
                    datos = new Dictionary<string, int>
                    {
                        { "Enero", 30 },
                        { "Febrero", 65 },
                        { "Marzo", 90 },
                        { "Abril", 140 }
                    }
                };

                HttpResponseMessage response = await _httpClient.GetAsync(pythonUrl);

                if (!response.IsSuccessStatusCode)
                {
                    ModelState.AddModelError(string.Empty, $"Python respondió con error: {response.StatusCode}");
                    return Page();
                }
                var pdfStream = await response.Content.ReadAsStreamAsync();
                return File(pdfStream, "application/pdf", "reporte_facultad.pdf");
            }
            catch (Exception ex)
            {
                ModelState.AddModelError(string.Empty, $"Error de conexión con el microservicio: {ex.Message}");
                return Page();
            }
        }
    }
}