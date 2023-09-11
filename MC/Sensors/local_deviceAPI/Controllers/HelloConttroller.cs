using DeviceAPI.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace DeviceAPI.Controllers
{
    [Route("/")]
    [ApiController]
    public class HelloConttroller : ControllerBase
    {
        [HttpGet]
        public IActionResult GetDevices()
        {

            return Ok(GlobalDevice.devicesList);
        }
    }
}
