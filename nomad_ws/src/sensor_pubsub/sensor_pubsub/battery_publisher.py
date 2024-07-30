import sys
import time
sys.path.append('/home/pi/MasterPi/')
import HiwonderSDK.Board as Board

from smbus2 import SMBus, i2c_msg
import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Float32
from sensor_msgs.msg  import BatteryState


class MinimalPublisherV2(Node):

    def __init__(self):
        super().__init__('sensor_publisher')
        self.publisher_ = self.create_publisher(BatteryState, '/sensors/battery_state', 10)
        timer_period = 30  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        biffBattery = BatteryState()
        #not doing this correctly. getBattery returns
        #millivolts to a varying number of significant digits so
        #the divide by causes order of magnitude errors.
        biffBattery.voltage = Board.getBattery()/1000.0
        biffBattery.design_capacity = 1.500    #A-hr maybe wrong, can't see
        biffBattery.location = "Under Body"      #string
        biffBattery.serial_number = "18650"     #string
        biffBattery.power_supply_status = BatteryState.POWER_SUPPLY_STATUS_NOT_CHARGING
        biffBattery.power_supply_health =  BatteryState.POWER_SUPPLY_HEALTH_UNKNOWN
        biffBattery.power_supply_technology = BatteryState.POWER_SUPPLY_TECHNOLOGY_LION
#        std_msgs/msg/Header header
#        float voltage
#        float temperature
#        float current
#        float charge
#        float capacity
#        float design_capacity
#        float percentage
#        uint8 power_supply_status
#        uint8 power_supply_health
#        uint8 power_supply_technology
#        boolean present
#        float[] cell_voltage
#        float[] cell_temperature
#        string location
#        string serial_number

        self.publisher_.publish(biffBattery)
        self.get_logger().info('Volts: %f' % biffBattery.voltage)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisherV2()
    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
