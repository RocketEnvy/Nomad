import sys
import time
sys.path.append('/home/pi/MasterPi/')
import HiwonderSDK.Board as Board

from smbus2 import SMBus, i2c_msg
import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Float32
from sensor_msgs.msg  import Range


class MinimalPublisherV2(Node):

    def __init__(self):
        super().__init__('sensors_publisher')
        self.publisher_ = self.create_publisher(Range, '/sensors/sonar', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        rangerRick = Range()
        rangerRick.radiation_type = rangerRick.ULTRASOUND
        rangerRick.field_of_view = 15.0
        rangerRick.min_range=0.01
        rangerRick.max_range=5.00
        rangerRick.range=self.getDistance() # meters
        self.publisher_.publish(rangerRick)
        if self.i % 100 == 0:
            self.get_logger().info('Range: %f' % rangerRick.range)
        self.i += 1

    #lifted and slightly modded from MasterPi/HiWonder/Sonar.py
    #This is most likely that common cheap sonar sensor HRC_??(?)
    #with some bright RGB LEDs added. Isn't clear to me if it also
    #has its own I2C controller or if trigger and data are directly
    #connected to SMBus hat. It will almost certainly never get the
    #claimed 5m ranging distance unless they have also added a boost
    #converter for the sonar TX--5-8V is too little, 50V to 150V would
    #probably be needed to send out a good ping.
    #Might eventually add another near the camera.
    def getDistance(self):
        dist = float(99999.00)
        i2c_addr = 0x77
        i2c = 1
        try:
            with SMBus(i2c) as bus:
                msg = i2c_msg.write(i2c_addr, [0,])
                bus.i2c_rdwr(msg)
                read = i2c_msg.read(i2c_addr, 2)
                bus.i2c_rdwr(read)
                dist = int.from_bytes(bytes(list(read)), byteorder='little', signed=False)
                if dist > 5000:
                    dist = 5000
        except BaseException as e:
            print(e)
        bus.close()
        # convert from millimeters to meters 
        return float(dist/1000.0)



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
