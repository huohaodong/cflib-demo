"""
获取与设置Log信息
"""

import logging
from threading import Timer

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# 无人机的地址，根据需求自行更改
URI = 'radio://0/3/2M'

# 设置只输出log框架本身的信息
logging.basicConfig(level=logging.ERROR)


def stab_log_error(self, logconf, msg):
    """Callback from the log API when an error occurs"""
    print('Error when logging %s: %s' % (logconf.name, msg))


def stab_log_data(self, timestamp, data, logconf):
    """Callback from a the log API when data arrives"""
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))


if __name__ == '__main__':
    cflib.crtp.init_drivers()
    cf = Crazyflie(rw_cache="./cache")
    cf.open_link(link_uri=URI)

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')

    try:
        cf.log.add_config(lg_stab)
        # This callback will receive the data
        lg_stab.data_received_cb.add_callback(stab_log_data)
        # This callback will be called on errors
        lg_stab.error_cb.add_callback(stab_log_error)
        # Start the logging
        lg_stab.start()
    except KeyError as e:
        print('Could not start log configuration,'
              '{} not found in TOC'.format(str(e)))
    except AttributeError:
        print('Could not add Stabilizer log config, bad configuration.')

    t = Timer(5, cf.close_link)
    t.start()

    cf.close_link()

import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    # Scan for Crazyflies and use the first one found
    print('Scanning interfaces for Crazyflies...')
    available = cflib.crtp.scan_interfaces()
    print('Crazyflies found:')
    for i in available:
        print(i[0])

    if len(available) == 0:
        print('No Crazyflies found, cannot run example')
    else:
        lg_stab = LogConfig(name='TSranging', period_in_ms=10)
        lg_stab.add_variable('TSranging.error', 'uint16_t')
        lg_stab.add_variable('TSranging.total', 'uint16_t')

        cf = Crazyflie(rw_cache='./cache')
        with SyncCrazyflie(available[0][0], cf=cf) as scf:
            # Note: it is possible to add more than one log config using an
            # array.
            # with SyncLogger(scf, [lg_stab, other_conf]) as logger:
            with SyncLogger(scf, lg_stab) as logger:
                endTime = time.time() + 10

                for log_entry in logger:
                    timestamp = log_entry[0]
                    data = log_entry[1]
                    logconf_name = log_entry[2]

                    print('[%d][%s]: %s' % (timestamp, logconf_name, data))

                    if time.time() > endTime:
                        break
