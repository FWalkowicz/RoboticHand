namespace DeviceAPI.Models
{
    public class Gyroscope
    {
        public string? deviceId { get; set; }
        public DateTime? timestampUTC { get; set;}
        public float gx { get; set; }
        public float gy { get; set; }
        public float gz { get; set; }
    }
    public static class GlobalGyro
    {
        public static List<Gyroscope> gyroList = new List<Gyroscope>
        {
            new Gyroscope {deviceId="4", timestampUTC=DateTime.UtcNow, gx=0.5F, gy=1.02F, gz=2.1F},
            new Gyroscope {deviceId="5", timestampUTC=DateTime.UtcNow, gx=0.01F, gy=0.61F, gz=0.8F}
        };
    }
}
