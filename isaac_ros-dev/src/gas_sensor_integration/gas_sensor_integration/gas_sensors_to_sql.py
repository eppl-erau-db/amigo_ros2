import rclpy
from rclpy.node import Node
from smbus2 import SMBus
import mariadb
import struct


class GasSensorToSQLNode(Node):
    def __init__(self):
        super().__init__('gas_sensor_to_sql_node')

        # I2C Setup:
        self.bus = SMBus(1) # I2C bus number
        self.arduino_address = 0x08  # Replace with Arduino I2C address

        # Mariadb setup
        self.db_conn = self.connect_to_db()

        # Timer to periodically read from I2C and save data
        self.timer = self.create_timer(2.0, self.read_and_save_data)

    def connect_to_db(self):
        '''Establish connection to sql database'''
        try:
            conn = mariadb.connect(
                user="AMIGO",
                password="123",
                host="host.docker.internal",  # Replace with the IP address of the Jetson AGX
                port=3306,  # Change port if needed
                database="Gas_Sensors"
            )
            self.get_logger().info("Connected to MariaDB database.")
            return conn
        except mariadb.Error as e:
            self.get_logger().error(f"Error connected to MariaDB: {e}")
            return None
        
    def read_and_save_data(self):
        '''Read data from Arudino and save to the MariaDB database'''
        try:
            # Request 22 bytes from Arduino (CO2: 2 bytes, 5 floats: 4 bytes each)
            data = self.bus.read_i2c_block_data(self.arduino_address, 0, 22)

            # Unpack the received data (CO2: 2 bytes, floats: 4 bytes each)
            co2PPM = (data[0] << 8) | data[1]  # CO2 is sent as two bytes (16-bit int)
            # GAS1 and GAS2 are O2 or SO2
            temp, hum, methanePPM, gas1PPM, gas2PPM = struct.unpack('fffff', bytes(data[2:]))

            # Log the data
            self.get_logger().info(f"Received data: CO2={co2PPM}, Temperature={temp}, Humidity={hum}, "
                                   f"Methane={methanePPM}, Gas1={gas1PPM}, Gas2={gas2PPM}")
            
            # Save the data to the MariaDB database
            self.save_data_to_db(co2PPM, temp, hum, methanePPM, gas1PPM, gas2PPM)
        except Exception as e:
            self.get_logger().error(f"Failed to read from I2C: {e}")

    def save_data_to_db(self, co2PPM, temp, hum, methanePPM, gas1PPM, gas2PPM):
        '''Save the sensor data to the MariaDB database'''
        if self.db_conn:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute('''
                    INSERT INTO sensor_data (co2, temperature, humidity, methanePPM, gas1PPM, gas2PPM)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (co2PPM, temp, hum, methanePPM, gas1PPM, gas2PPM))
                self.db_conn.commit()
                self.get_logger().info("Data successfully saved to the MariaDB database.")
            except mariadb.Error as e:
                self.get_logger().error(f"Failed to save data to the database: {e}")
        else:
            self.get_logger().error("Database connection is not available.")

def main(args=None):
    rclpy.init(args=args)
    node = GasSensorToSQLNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()