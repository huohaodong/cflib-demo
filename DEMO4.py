"""
SyncLogger示例
"""
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
