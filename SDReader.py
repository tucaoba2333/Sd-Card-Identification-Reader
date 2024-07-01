from ctypes import *
import objc
from Foundation import *
from IOKit import *


def get_device_tree_path():
    IOServiceGetMatchingServices = cdll.LoadLibrary(
        "/System/Library/Frameworks/IOKit.framework/IOKit").IOServiceGetMatchingServices
    IOServiceGetMatchingServices.restype = c_uint
    IOServiceGetMatchingServices.argtypes = [c_void_p, c_void_p, POINTER(c_void_p)]

    kIOMasterPortDefault = c_void_p.in_dll(cdll.LoadLibrary("/System/Library/Frameworks/IOKit.framework/IOKit"),
                                           "kIOMasterPortDefault")

    matching = IOServiceMatching("IODeviceTree")
    iterator = c_void_p()
    result = IOServiceGetMatchingServices(kIOMasterPortDefault, matching, byref(iterator))
    if result != 0:
        return None

    devices = []
    while True:
        device = IOIteratorNext(iterator)
        if device == 0:
            break
        devices.append(device)

    IOObjectRelease(iterator)
    return devices


def read_device_data(device_path):
    # 使用open或其他文件操作来访问设备文件
    with open(device_path, 'rb') as device_file:
        data = device_file.read(512)  # 读取前512字节的数据
        return data


if __name__ == "__main__":
    devices = get_device_tree_path()
    if not devices:
        print("No devices found.")
    else:
        for device in devices:
            # 在这里，你可以进一步筛选找到你的记忆卡设备
            # 例如，打印设备信息或读取特定路径的数据
            device_path = "/dev/rdisk2"  # 替换为实际设备路径
            data = read_device_data(device_path)
            print(data)
