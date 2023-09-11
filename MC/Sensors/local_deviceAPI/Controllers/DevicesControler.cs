using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using DeviceAPI.Models;


namespace DeviceAPI.Controllers
{

    [ApiController]
    [Route("/devices")]

    public class DevicesController : ControllerBase
    {
        
        

        [HttpGet]
        public IActionResult GetDevices()
        {
            return Ok(GlobalDevice.devicesList);
        }
        

    }
}
