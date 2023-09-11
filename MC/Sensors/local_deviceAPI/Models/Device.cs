namespace DeviceAPI.Models
{
    public class Device
    {
        public string deviceId { get; set; }

        public static int FindId()
        {
            int maxId = int.MinValue;
            foreach (var item in GlobalDevice.devicesList)
            {
                if (int.TryParse(item.deviceId, out int itemId))
                {
                    maxId = Math.Max(maxId, itemId);
                }
            }
            return maxId+1;
        }
    }
    public static class GlobalDevice
    {
        public static List<Device> devicesList = new List<Device>
        {
            new Device { deviceId="0" },
            new Device { deviceId="1" },
            new Device { deviceId="2" },
            new Device { deviceId="3" },
            new Device { deviceId="4" },
            new Device { deviceId="5" }
        };
    }
}
