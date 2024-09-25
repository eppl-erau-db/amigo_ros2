#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import Jetson.GPIO as GPIO
from example_interfaces.srv import SetBool
from DRV8825 import DRV8825


class PanTiltService(Node):
    def __init__(self):
        super.__init__('controller_service')
        self.srv = self.create_service()

        # Initialize motors
        self.motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        self.motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        
        # Set both motors to full step
        self.motor1.SetMicroStep('software', 'fullstep')
        self.motor2.SetMicroStep('software', 'fullstep')

        # Create service
        self.srv = self.create_service(SetBool, 'motor_control', self.handle_motor_control_request)
    
    def handle_motor_control_request(self, request, response):
        motor = self.motor1 if request.data else self.motor2
        direction = 'forward' if request.data else 'backward'

        if direction == 'forward':
            self.move_motor_up(motor)
        else:
            self.move_motor_down(motor)

        response.success = True
        return response

    def move_motor_up(self, motor):
        motor.TurnStep(Dir='forward', steps=2048, stepdelay=0.005)
        self.get_logger().info("Motor moved forward")

    def move_motor_down(self, motor):
        motor.TurnStep(Dir='backward', steps=2048, stepdelay=0.005)
        self.get_logger().info("Motor moved backward")
    
    def destroy(self):
        self.motor1.Stop()
        self.motor2.Stop()
        GPIO.cleanup()
        super().destroy()

def main(args=None):
    rclpy.init(args=args)
    node = PanTiltService()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
