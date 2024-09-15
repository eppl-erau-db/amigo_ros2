**Setup Grapaha**


1. Get Update
```
sudo apt-get update
sudo apt-get upgrade
```

2.Install Grapha
```
sudo apt-get install -y software-properties-common
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```

```
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
```

```
sudo apt-get update
sudo apt-get install grafana
```

3. Start Graphana and set to run on boot
```
sudo systemctl start grafana-server
```
```
sudo systemctl enable grafana-server
```

4.Setup Website

Get your IP address
```
hostname -I
```

Go to a web browser on device on the same network
```
http://<your_IP_address>:3000
```

Use admin, admin initially when setting up Graphana and change later 

**Setup SQL database**

This is meant to set the storing of gas sensor data to a SQL database to then be visualized by Graphana

1. Install MariaDB
```
sudo apt-get install mariadb-server
sudo mysql_secure_installation
```

2. Enter MariaDB 
```
sudo mariadb
```
On first start-up only
Once in the database 
```
CREATE USER 'AMIGO'@'localhost' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'AMIGO'@'localhost';
FLUSH PRIVILEGES;
```


3. Setup the place for gas sensor data to be stored
This creates the Database and table to store the gas sensor data in
```
CREATE DATABASE Gas_Sensors;
CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    Methane FLOAT,
    O2 FLOAT,
    CO2 FLOAT,
    SO2 FLOAT,
    Humidity Float,
    Temp Float
);
```

