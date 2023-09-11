namespace DeviceAPI.Models
{
    public class Temperature
    {
        public string? deviceId { get; set; } //from Device
        public DateTime? timestampUTC { get; set; }
        public float temperature { get; set; }
        
    }
    public static class GlobalTemp
    {
        public static List<Temperature> temperatureList = new List<Temperature>
        {
            new Temperature {deviceId="0", timestampUTC=DateTime.Now, temperature=20.60F},
            new Temperature {deviceId="2", timestampUTC=DateTime.Now, temperature=-8.76F}
        };

    }
}
