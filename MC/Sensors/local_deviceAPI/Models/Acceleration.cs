namespace DeviceAPI.Models
{
    public class Acceleration
    {
        public string? deviceId { get; set; }
        public DateTime?timestampUTC { get; set; }
        public float ax { get; set; }
        public float ay { get; set; }
        public float az { get; set; }
    }

    public static class GlobalAcceleration
    {
        public static List<Acceleration> accelerationList = new List<Acceleration>
        {
            new Acceleration {deviceId="1", timestampUTC=DateTime.Now, ax=1.2F, ay=0.4F, az=0.7F},
            new Acceleration {deviceId="3", timestampUTC=DateTime.Now, ax=1.9F, ay=0.7F, az=1.2F}
        };
    }
}
