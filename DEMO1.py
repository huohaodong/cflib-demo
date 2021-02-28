"""
连接Crazyflie
"""
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie


def connected_callback(link_uri):
    print("连接到了无人机")


if __name__ == '__main__':
    # 初始化驱动
    cflib.crtp.init_drivers()
    # 扫描无人机
    available = cflib.crtp.scan_interfaces()
    # 获取并初始化第一个扫描到的无人机对象
    FIRST_LINK_URL = ""
    if len(available) > 0:
        FIRST_LINK_URL = available[0][0]
    else:
        print("没有扫描到无人机")

    cf = Crazyflie(rw_cache="./cache")
    cf.connected.add_callback(connected_callback)

    # 使用SyncCrazyflie来包装上面初始化的Crazyflie对象
    with SyncCrazyflie(FIRST_LINK_URL, cf=cf) as scf:
        print("do something......")
