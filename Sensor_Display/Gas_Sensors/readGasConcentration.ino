#include <Wire.h>
#include "DFRobot_MultiGasSensor.h"
#include <SensirionI2CScd4x.h>

// Define I2C addresses for the sensors
#define I2C_ADDRESS_1 0x74 // Address for Gas Sensor 1
#define I2C_ADDRESS_2 0x76 // Address for Gas Sensor 2
#define SCD4X_ADDRESS 0x62 // Address for SCD4X CO2 Sensor

// Initialize sensor objects
DFRobot_GAS_I2C gas1(&Wire, I2C_ADDRESS_1);
DFRobot_GAS_I2C gas2(&Wire, I2C_ADDRESS_2);
SensirionI2CScd4x scd4x; // Initialize SCD4X CO2 sensor

// Methane sensor connected to analog pin A0
int methaneSensorPin = A0;
int methaneSensorValue = 0;

// Calibration parameters (hypothetical)
float slope = 4000.0; // PPM per Volt
float intercept = -7000.0; // PPM

// Function to convert voltage to PPM based on calibration
float voltageToPPM(float voltage) {
    return slope * voltage + intercept;
}

// Function to print a 16-bit integer as a hexadecimal value
void printUint16Hex(uint16_t value) {
    Serial.print(value < 4096 ? "0" : "");
    Serial.print(value < 256 ? "0" : "");
    Serial.print(value < 16 ? "0" : "");
    Serial.print(value, HEX);
}

// Function to print the serial number of the SCD4X sensor
void printSerialNumber(uint16_t serial0, uint16_t serial1, uint16_t serial2) {
    Serial.print("Serial: 0x");
    printUint16Hex(serial0);
    printUint16Hex(serial1);
    printUint16Hex(serial2);
    Serial.println();
}

// Function to send sensor data over I2C to Jetson
void sendDataToJetson(uint16_t co2, float temperature, float humidity, float methanePPM, float gas1PPM, float gas2PPM) {
    Wire.beginTransmission(0x08); // Replace with the Jetson's I2C address (e.g., 0x08)
    
    // Send CO2 concentration
    Wire.write((uint8_t)(co2 >> 8)); // High byte
    Wire.write((uint8_t)(co2 & 0xFF)); // Low byte
    
    // Send Temperature
    Wire.write((uint8_t*)&temperature, sizeof(temperature)); // Cast to byte array
    
    // Send Humidity
    Wire.write((uint8_t*)&humidity, sizeof(humidity));
    
    // Send Methane concentration
    Wire.write((uint8_t*)&methanePPM, sizeof(methanePPM));
    
    // Send Gas Sensor 1 concentration
    Wire.write((uint8_t*)&gas1PPM, sizeof(gas1PPM));
    
    // Send Gas Sensor 2 concentration
    Wire.write((uint8_t*)&gas2PPM, sizeof(gas2PPM));
    
    Wire.endTransmission(); // End the I2C transmission
}

void setup() {
    Serial.begin(115200);
    while (!Serial) {
        delay(100);
    }

    Wire.begin();

    // Initialize Gas Sensor 1
    while(!gas1.begin()) {
        Serial.println("Gas Sensor 1 not detected!");
        delay(1000);
    }
    Serial.println("Gas Sensor 1 connected!");

    // Initialize Gas Sensor 2
    while(!gas2.begin()) {
        Serial.println("Gas Sensor 2 not detected!");
        delay(1000);
    }
    Serial.println("Gas Sensor 2 connected!");

    // Initialize SCD4X CO2 Sensor
    uint16_t error;
    char errorMessage[256];
    scd4x.begin(Wire);

    // Stop any previous measurements on the SCD4X
    error = scd4x.stopPeriodicMeasurement();
    if (error) {
        Serial.print("Error trying to execute stopPeriodicMeasurement(): ");
        errorToString(error, errorMessage, 256);
        Serial.println(errorMessage);
    }

    // Get and print SCD4X serial number
    uint16_t serial0, serial1, serial2;
    error = scd4x.getSerialNumber(serial0, serial1, serial2);
    if (error) {
        Serial.print("Error trying to execute getSerialNumber(): ");
        errorToString(error, errorMessage, 256);
        Serial.println(errorMessage);
    } else {
        printSerialNumber(serial0, serial1, serial2);  // Function call
    }

    // Start periodic measurement for SCD4X
    error = scd4x.startPeriodicMeasurement();
    if (error) {
        Serial.print("Error trying to execute startPeriodicMeasurement(): ");
        errorToString(error, errorMessage, 256);
        Serial.println(errorMessage);
    }

    Serial.println("Waiting for first measurement... (5 sec)");

    // Configure gas sensors (optional, based on your requirements)
    gas1.setTempCompensation(gas1.OFF);
    gas2.setTempCompensation(gas2.OFF);
}

void loop() {
    // Read from Gas Sensor 1
    float gas1PPM = gas1.readGasConcentrationPPM();
    Serial.print("Gas Sensor 1 (");
    Serial.print(gas1.queryGasType());
    Serial.print(") concentration: ");
    Serial.print(gas1PPM);
    Serial.println(" PPM");

    // Read from Gas Sensor 2
    float gas2PPM = gas2.readGasConcentrationPPM();
    Serial.print("Gas Sensor 2 (");
    Serial.print(gas2.queryGasType());
    Serial.print(") concentration: ");
    Serial.print(gas2PPM);
    Serial.println(" PPM");

    // Read from SCD4X CO2 Sensor
    uint16_t co2;
    float temperature;
    float humidity;
    uint16_t error = scd4x.readMeasurement(co2, temperature, humidity);
    if (error) {
        char errorMessage[256];
        Serial.print("Error trying to execute readMeasurement(): ");
        errorToString(error, errorMessage, 256);
        Serial.println(errorMessage);
    } else if (co2 == 0) {
        Serial.println("Invalid sample detected, skipping.");
    } else {
        Serial.print("CO2 concentration: ");
        Serial.print(co2);
        Serial.println(" PPM");

        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.println(" °C");

        Serial.print("Humidity: ");
        Serial.println(humidity);
    }

    // Read Methane Sensor Value
    methaneSensorValue = analogRead(methaneSensorPin);
    float voltage = (methaneSensorValue / 1023.0) * 5.0; // Assuming a 5V reference
    float methanePPM = voltageToPPM(voltage);
    Serial.print("Methane Concentration: ");
    Serial.print(methanePPM);
    Serial.println(" PPM");

    Serial.println("-----------------------------");

    // Send data to Jetson over I2C
    sendDataToJetson(co2, temperature, humidity, methanePPM, gas1PPM, gas2PPM);

    delay(2000); // Wait 2 seconds before the next loop
}
