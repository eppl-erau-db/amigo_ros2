#include <Wire.h>
#include "DFRobot_MultiGasSensor.h"
#include <SensirionI2CScd4x.h>

// Define I2C addresses for the gas sensors
#define I2C_ADDRESS_1 0x74 // Address for Gas Sensor 1
#define I2C_ADDRESS_2 0x76 // Address for Gas Sensor 2

// Initialize sensor objects
DFRobot_GAS_I2C gas1(&Wire, I2C_ADDRESS_1);
DFRobot_GAS_I2C gas2(&Wire, I2C_ADDRESS_2);
SensirionI2CScd4x scd4x; // Initialize SCD4X CO2 sensor

void printUint16Hex(uint16_t value) {
    Serial.print(value < 4096 ? "0" : "");
    Serial.print(value < 256 ? "0" : "");
    Serial.print(value < 16 ? "0" : "");
    Serial.print(value, HEX);
}

void printSerialNumber(uint16_t serial0, uint16_t serial1, uint16_t serial2) {
    Serial.print("Serial: 0x");
    printUint16Hex(serial0);
    printUint16Hex(serial1);
    printUint16Hex(serial2);
    Serial.println();
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
        printSerialNumber(serial0, serial1, serial2);
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
    Serial.print("Gas Sensor 1 (");
    Serial.print(gas1.queryGasType());
    Serial.print(") concentration: ");
    Serial.print(gas1.readGasConcentrationPPM());
    Serial.println(" PPM");

    // Read from Gas Sensor 2
    Serial.print("Gas Sensor 2 (");
    Serial.print(gas2.queryGasType());
    Serial.print(") concentration: ");
    Serial.print(gas2.readGasConcentrationPPM());
    Serial.println(" PPM");

    // Read from SCD4X CO2 Sensor
    uint16_t error;
    char errorMessage[256];
    delay(5000); // Wait for 5 seconds between readings

    uint16_t co2;
    float temperature;
    float humidity;
    error = scd4x.readMeasurement(co2, temperature, humidity);
    if (error) {
        Serial.print("Error trying to execute readMeasurement(): ");
        errorToString(error, errorMessage, 256);
        Serial.println(errorMessage);
    } else if (co2 == 0) {
        Serial.println("Invalid sample detected, skipping.");
    } else {
        Serial.print("SCD4X CO2 concentration: ");
        Serial.print(co2);
        Serial.print(" PPM\t");

        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.print(" °C\t");

        Serial.print("Humidity: ");
        Serial.println(humidity);
    }

    Serial.println("-----------------------------");
    delay(2000); // Wait 2 seconds before the next loop
}

