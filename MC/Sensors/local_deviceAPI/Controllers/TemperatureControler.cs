using DeviceAPI.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace DeviceAPI.Controllers
{

    [Route("/temperature")]
    [ApiController]
    public class TemperatureControler : ControllerBase
    {
        [HttpPost]
        public IActionResult PostTemperature(Temperature temperature) 
        {
            if (temperature.timestampUTC == null)
            {
                temperature.timestampUTC = DateTime.UtcNow;
            }
            if (temperature.deviceId == null) 
            {
                temperature.deviceId = "unknow";
            }
            GlobalDevice.devicesList.Add(new Device {deviceId=temperature.deviceId});
            GlobalTemp.temperatureList.Add(temperature);

            return CreatedAtAction(nameof(GetTemperature), new { id = temperature.deviceId }, temperature);
        }
        [HttpGet("{id}")]
        
        public IActionResult GetTemperature(string id)
        {
            var temperature = GlobalTemp.temperatureList.FirstOrDefault(p => p.deviceId == id);
            if (temperature == null)
            {
                return NotFound(); //404
            }
            return Ok(temperature);
        }
        [HttpGet]
        public IActionResult GetTemperature()
        {
            return Ok(GlobalTemp.temperatureList);
        }

    }
}
