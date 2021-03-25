# Docker-MQTT-INFLUX-GRAFANA-ESP2866
Smarthome system install in Mint Linux. IoT is a NodeMCU ESP2866 with BME280.
The install on Raspberry Pi is the same, because raspi is debian based and the used containers is avaiable on that platform too.

# Install and Goal
Docker, Portainer, Mosquitto, InfluxDB, Telegraf, Grafana, HomeAssistant
System is Linux Mint Debian Edition
> Note: HomeAssistant is very simple, so i don't wrote it down
> Note: Linux Mint Debian Edition is running on my MAC separatly

## UPDATE 25.03.2021
I decide to try a more convient way to set up the SMARTHOME system on my Mac with Docker-Desktop & docker-compose.
So I added the [docker-compose.yaml](https://github.com/Hufnagels/Docker-MQTT-INFLUX-GRAFANA/blob/main/docker-compose.yaml) file. In this config with Docker Desktop app u don't need the first service (portainer), so u can remove it.
Another change is downgrade of influx from latest to 1.8
In Grafana on the DB connect panel connection works only with the host computer IP (in my case --> need to check why localhost not working)

### TODO
Create the right config for influx base DB (smarthome in my case) and adding user and admin with necessary privilegs.

## GOAL
In the home network every IoT device (NodeMCU esp2866 with Esp easy firmware for testing) should be able to connect to MQTT broker.
In my tries I run every time into same **issue**: mosquitto is unreachable from outside, reachable only for localhost/inside docker. It means, from lan is unreachable.

## INSTALL

After installing docker engine starting with adding images.

#### ISSUE
***Running this command:***
~~~
sudo docker run --name mosquitto -p 1883:1883 -p 9001:9001 -v ./mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
~~~
***Results this:***
~~~
1611227315: mosquitto version 2.0.7 starting
1611227315: Config loaded from /mosquitto/config/mosquitto.conf.
1611227315: Starting in local only mode. Connections will only be possible from clients running on this machine.
1611227315: Create a configuration file which defines a listener to allow remote access.
1611227315: Opening ipv4 listen socket on port 1883.
1611227315: Opening ipv6 listen socket on port 1883.
1611227315: Error: Address not available
1611227315: mosquitto version 2.0.7 running
~~~
This issue can be solved in two ways:

- install mqtt outside docker as a local process
- or ***solve the problem***

I picked the second. So I created this readme to help with my experiences
> Note: My local IP used in every situation is `192.168.1.87`

> Note: I used User/password combo in every case (telegraf, mqtt, influxDB admin) `telegraf/telegraf` for simplicity

> Note: No SSL configured

### Used sources:
[How To Install InfluxDB Telegraf and Grafana on Docker](https://devconnected.com/how-to-install-influxdb-telegraf-and-grafana-on-docker/#Creatingupdating_the_InfluxDB_meta_database)

[Github Telegraf JSON definition](https://github.com/influxdata/telegraf/tree/master/plugins/parsers/json)

Many samples are outthere, also youtube videos. But when I followed them, I run always into the [***ISSUE***](#issue)

### usecases
- [Visualize MQTT Data with InfluxDB and Grafana](https://diyi0t.com/visualize-mqtt-data-with-influxdb-and-grafana/)
- [Send data from ESP8266 or ESP32 to Raspberry Pi via MQTT](https://diyi0t.com/microcontroller-to-raspberry-pi-wifi-mqtt-communication/)
- [ESP8266 NodeMCU MQTT – Publish BME280 Sensor Readings (Arduino IDE)](https://randomnerdtutorials.com/esp8266-nodemcu-mqtt-publish-bme280-arduino/)
- [ESP32 MQTT – Publish BME280 Sensor Readings (Arduino IDE)](https://randomnerdtutorials.com/esp32-mqtt-publish-bme280-arduino/)

### used for testing mqtt from outside docker
- MQTT.fx (on my MAC)
- [Paho mqtt python library](https://github.com/eclipse/paho.mqtt.python) (on my raspberry for octoprint)
~~~
git clone https://github.com/eclipse/paho.mqtt.python
~~~

### Advice
Use
~~~
sudo usermod -aG docker $USER
~~~
And each container user can be added to docker group also


## Docker

~~~
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository  "deb [arch=amd64] https://download.docker.com/linux/debian  $(lsb_release -cs) stable"
~~~
~~~
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
~~~
Daemon config for changeing the data-root for containers (in raspi is a good choiche for use external drive)
~~~
sudo nano /etc/docker/daemon.json
~~~
~~~
{
        "debug":true,
        "data-root":"/media/www/docker/"
}
~~~
If u want to use docker compose to build everything from yaml file
> Note: I didn't used it yet

~~~
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
docker-compose --version
~~~

## Portainer


~~~
sudo docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
~~~
> [Portainer UI](http://localhost:9000) http://<your-ip>:9000

## node red
~~~
sudo docker run -it -p 1880:1880 -v node_red_data:/data --name mynodered nodered/node-red
~~~
> [Node-Redr UI](http://localhost:1880) http://<your-ip>:1880
## mosquitto
~~~
sudo docker run --name mosquitto -p 1883:1883 --ip 192.168.1.87 -h mqtt.lmde.local -v /home/pisti/dev/smarthome/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
~~~
(# sudo docker run -it --name mqtt --net=host -p 1883:1883 -p 9001:9001 eclipse-mosquitto)

### configuration
Without auth. I think, when everything works fine, can be done.

[mosquitto.conf](https://github.com/Hufnagels/Docker-MQTT-INFLUX-GRAFANA/blob/main/mosquitto.conf)


## influxdb
~~~
sudo useradd -rs /bin/false influxdb
sudo mkdir -p /etc/influxdb
docker run --rm influxdb influxd config | sudo tee /etc/influxdb/influxdb.conf > /dev/null
sudo chown influxdb:influxdb /etc/influxdb/*
sudo mkdir -p /var/lib/influxdb
sudo chown influxdb:influxdb /var/lib/influxdb
sudo mkdir -p /etc/influxdb/scripts
sudo touch influxdb-init.iql
~~~
The influxdb-init.iql something like that
~~~
CREATE DATABASE smarthome;
CREATE RETENTION POLICY one_week ON smarthome DURATION 168h REPLICATION 1 DEFAULT;
~~~
then (don't forget `INFLUXDB_ADMIN_USER` to change)
~~~
docker run --rm -e INFLUXDB_HTTP_AUTH_ENABLED=true \
         -e INFLUXDB_ADMIN_USER=telegraf \
         -e INFLUXDB_ADMIN_PASSWORD=telegraf \
         -v /var/lib/influxdb:/var/lib/influxdb \
         -v /etc/influxdb/scripts:/docker-entrypoint-initdb.d \
         influxdb /init-influxdb.sh

cat /var/lib/influxdb/meta/meta.db | grep one_week
~~~
It should result a log without errors. I had permission errors. The reason: i use sudo docker, my external data dir (/media/www/docker) created as root and influx want create the meta.dbtmp with influx user. So I added it to docker group and changed chmod to writeable for owner/group

Enable auth
~~~
sudo nano /etc/influxdb/influxdb.conf
~~~
### configuration
[influxdb.conf](https://github.com/Hufnagels/Docker-MQTT-INFLUX-GRAFANA/blob/main/influxdb.conf)
~~~
cat /etc/passwd | grep influxdb
~~~
restart container
~~~
sudo docker run -d -p 8086:8086 --user 999:998 --name=influxdb -v /etc/influxdb/influxdb.conf:/etc/influxdb/influxdb.conf -v /var/lib/influxdb:/var/lib/influxdb influxdb -config /etc/influxdb/influxdb.conf
~~~
test
~~~
curl -G -u telegraf:telegraf http://localhost:8086/query --data-urlencode "q=SHOW DATABASES"
~~~

## telegraf
~~~
sudo useradd -rs /bin/false telegraf
sudo mkdir -p /etc/telegraf
docker run --rm telegraf telegraf config | sudo tee /etc/telegraf/telegraf.conf > /dev/null
sudo chown telegraf:telegraf /etc/telegraf/*
~~~
### ESP2866 - BME280 sensor + Rules to send data to mqtt
~~~
Firmware
Build:⋄	20111 - Mega
System Libraries:⋄	ESP82xx Core 2843a5ac, NONOS SDK 2.2.2-dev(38a443e), LWIP: 2.1.2 PUYA support
Git Build:⋄	
Plugin Count:⋄	47 [Normal]
Build Origin:	Travis
Build Time:⋄	Jan 14 2021 23:29:36
Binary Filename:⋄	ESP_Easy_mega_20210114_normal_ESP8266_4M1M
Build Platform:⋄	Linux-4.19.104-microsoft-standard-x86_64-with-glibc2.29
Git HEAD:⋄	mega-20210114_cdc8a1a
~~~
Example on [Github Telegraf JSON definition ](https://github.com/influxdata/telegraf/tree/master/plugins/parsers/json)

***JSON Example***
~~~
[[inputs.file]]
  files = ["example"]
  json_name_key = "name"
  tag_keys = ["my_tag_1"]
  json_string_fields = ["b_my_field"]
  data_format = "json"
~~~

Input:
~~~
{
    "a": 5,
    "b": {
        "c": 6,
        "my_field": "description"
    },
    "my_tag_1": "foo",
    "name": "my_json"
}
~~~

Output:
~~~
my_json,my_tag_1=foo a=5,b_c=6,b_my_field="description"
~~~
The ESP2866 (ESP Easy firmware) Rules tab:
~~~
On System#Boot do    //When the ESP boots, do
  timerSet,1,10      //Set Timer 1 for the next event in 10 seconds
endon

on MQTT#Connected do
 Publish,%sysname%/status, '{"Status":"MQTT connected", "IP":"%ip%"}'
endon

On Rules#Timer=1 do
   Publish %sysname%/BME280, '{"Sysname":"%sysname%","Taskname":"BME280","Uptime":"%uptime%","Temperature":[BME280#Temperature], "Humidity":[BME280#Humidity], "Pressure":[BME280#Pressure],"Room":"Livingroom"}'
   timerSet,1,10   //Set Timer 1 for the next event in 600 seconds
endon
~~~

In Node-Red incoming MQTT message is, where the mqtt server is 192.168.1.87, and subscribed topics: "ESP2866/status, ESP2866/BME280" are:
~~~
{
  "Sysname":"ESP2866",
  "Taskname":"BME280",
  "Uptime":"1027",
  "Temperature":22.36,
  "Humidity":48.33,
  "Pressure":1020.53,
  "Room":"Livingroom"
}
~~~
This need to translated to:
my_json,Room=Livingroom Temperature=5,Humidity=6,Pressure= 1010

### configuration
[telegraf.conf](https://github.com/Hufnagels/Docker-MQTT-INFLUX-GRAFANA/blob/main/telegraf.conf)

~~~
sudo docker container ls | grep influxdb
getent passwd | grep telegraf
~~~
if u had give name to influxdb container, then u can use `--net=container:0a1b01c54772` instead `--net=container:influxdb`. 

This will result something like that:
~~~
> SELECT * FROM mqtt_consumer
name: mqtt_consumer
time                Humidity Pressure Room       Temperature host         topic
----                -------- -------- ----       ----------- ----         -----
1614207971703269766 43.12    1021.89  Livingroom 21.8        0a1b01c54772 ESP2866/BME280
~~~
~~~
sudo docker run -d --user 998:997 --name=telegraf --net=container:0a1b01c54772 -e HOST_PROC=/host/proc -v /proc:/host/proc:ro -v /etc/telegraf/telegraf.conf:/etc/telegraf/telegraf.conf:ro telegraf

docker container logs -f --since 10m telegraf

docker exec -it 0a1b01c54772 influx -username telegraf -password telegraf
~~~

## grafana
~~~
sudo docker run -d --name=grafana -p 3000:3000 grafana/grafana
~~~
~~~
docker network inspect bridge | grep influxdb -A 5
~~~
> Default login: admin/admin
> [Grafana UI](http://localhost:3000) http://<your-ip>:3000

Sample Grafana query
~~~
SELECT mean("Temperature") FROM "one_week"."mqtt_consumer" WHERE ("topic" = 'ESP2866/BME280') AND $timeFilter GROUP BY time(10s) fill(none)
~~~
