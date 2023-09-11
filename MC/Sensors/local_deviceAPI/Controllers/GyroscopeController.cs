using DeviceAPI.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace DeviceAPI.Controllers
{
    [Route("/gyroscope")]
    [ApiController]
    public class GyroscopeController : ControllerBase
    {
        [HttpPost]
        public IActionResult PostGyroscope(Gyroscope gyroscope)
        {
            if (gyroscope.timestampUTC == null) 
            {
                gyroscope.timestampUTC = DateTime.UtcNow;
            }
            if (gyroscope.deviceId == null)
            {
                gyroscope.deviceId = "unknow";
            }
            GlobalDevice.devicesList.Add(new Device { deviceId = gyroscope.deviceId });
            GlobalGyro.gyroList.Add(gyroscope);
            return CreatedAtAction(nameof(Gyroscope), new {id=gyroscope.deviceId}, gyroscope);
        }
        
        [HttpGet("{id}")]
        public IActionResult GetGyroscope(string id)
        {
            var gyroscope = GlobalGyro.gyroList.FirstOrDefault(p => p.deviceId == id);
            if (gyroscope == null) 
            {
                return NotFound();
            }
            return Ok(gyroscope);
        }
        [HttpGet]
        public IActionResult GetGyroscope()
        {
            return Ok(GlobalGyro.gyroList);
        }
    }
}
