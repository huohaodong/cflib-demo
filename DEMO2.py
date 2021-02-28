"""
控制无人机飞行
"""

import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# 无人机的地址，根据需求自行更改
URI = 'radio://0/3/2M'

# 设置只输出log框架本身的信息
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # 初始化底层驱动
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # 当MotionCommander对象被创建后，其类内部的__enter__函数被触发。
        # 该函数调用了takeoff()函数，因此无需手动起飞，降落时也同理，其触发了__exit__函数（内部调用了land()降落函数）。
        with MotionCommander(scf) as mc:
            time.sleep(1)

            # MotionCommand封装了一些函数来供我们以米为单位来控制无人机的移动
            # 我们可以控制无人机朝着前后、上下、左右等方向来移动
            mc.forward(0.5)
            mc.back(0.5)
            time.sleep(1)

            mc.up(0.5)
            mc.down(0.5)
            time.sleep(1)

            # 移动的同时，我们也可以设置速度大小
            mc.right(0.5, velocity=0.8)
            time.sleep(1)
            mc.left(0.5, velocity=0.4)
            time.sleep(1)

            # 我们同样可以控制无人机进行旋转
            mc.circle_right(0.5, velocity=0.5, angle_degrees=180)

            # 向左掉头，本质上是封装了向左旋转的函数
            mc.turn_left(90)
            time.sleep(1)

            # 在三维空间中沿着一条线来移动
            mc.move_distance(-1, 0.0, 0.5, velocity=0.6)
            time.sleep(1)

            # MotionCommand也提供了持续移动的函数供使用，比如说开始向左保持0.5m的速度移动直到收到下个指令
            mc.start_left(velocity=0.5)
            # 该动作开始后我们可以做其他事情
            for _ in range(5):
                print('做一些其他事情')
                time.sleep(0.2)

            # 当然了，我们也可以发送命令来停止移动
            mc.stop()

            # With是Python的语法糖，在 `With` 这个 `Scope` 结束的时候，我们新建的MotionCommander对象的生命周期结束了。
            # 这个时候会触发__exit__（会调用land()函数），无人机会自行降落。