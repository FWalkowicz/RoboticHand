using DeviceAPI.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace DeviceAPI.Controllers
{
    [Route("/acceleration")]
    [ApiController]
    public class AccelerationControler : ControllerBase
    {
        [HttpPost]
        public IActionResult PostAcceleration(Acceleration acceleration)
        {
            if (acceleration.timestampUTC == null)
            {
                acceleration.timestampUTC = DateTime.UtcNow;
            }
            if (acceleration.deviceId == null)
            {
                acceleration.deviceId = "unknow";
            }
            GlobalDevice.devicesList.Add(new Device { deviceId = acceleration.deviceId });
            GlobalAcceleration.accelerationList.Add(acceleration);
            return CreatedAtAction(nameof(GetAcceleration),new {id=acceleration.deviceId},acceleration);
        }
        
        [HttpGet("{id}")]
        public IActionResult GetAcceleration(string id) 
        {
            var acceleration = GlobalAcceleration.accelerationList.FirstOrDefault(p=>p.deviceId == id);
            if (acceleration == null)
            {
                return NotFound();
            }
            return Ok(acceleration);
        }
        [HttpGet]
        public IActionResult GetAcceleration()
        {
            return Ok(GlobalAcceleration.accelerationList);
        }
    }
}
