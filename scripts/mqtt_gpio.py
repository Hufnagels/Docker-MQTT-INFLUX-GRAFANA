#mosquitto_pub -h 192.168.1.68 -t "octopi/gpio/status/printer" -m "off"
#mosquitto_pub -h 192.168.1.68 -t "octopi/gpio/status/psu" -m "off"

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json


mqtt_broker = '192.168.1.68'
mqtt_base_topic = "Octopi/gpio/"
psu_topic = "psu"
printer_topic = "printer"
psuPin = 6
printerPin = 12 

def main():
    GPIO.setmode(GPIO.BCM) #set numbering scheme
    GPIO.setup(psuPin,GPIO.OUT)
    GPIO.setup(printerPin,GPIO.OUT)
    GPIO.setwarnings(False)
    client = mqtt.Client()
    # Register connect callback
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, 1883, 60)
    try:
        client.loop_forever()
        sleep(60)
    except KeyboardInterrupt:
        #GPIO.cleanup()
        #client.unsubscribe(mqtt_topic)
        client.unsubscribe(mqtt_base_topic+psu_topic)
        client.unsubscribe(mqtt_base_topic+printer_topic)
        

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+str(rc))
    client.subscribe(mqtt_base_topic+psu_topic)
    client.subscribe(mqtt_base_topic+printer_topic)

def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode('utf-8')) + " on topic "+ message.topic + " with QoS " + str(message.qos))
    print(str(message.payload.decode('utf-8')))
    state = 0
    if (str(message.payload.decode('utf-8')) == "off"):
        state = 0
    elif (str(message.payload.decode('utf-8')) == "on"):
        state = 1
    else:
        print("nincs jo adat (on/off)")
        return
    print("state",state)
    if (message.topic == mqtt_base_topic+psu_topic):
        GPIO.output(psuPin, state)
    elif (message.topic == mqtt_base_topic+printer_topic):
        GPIO.output(printerPin, state)
    else:
        print("Nincs topic")

def set_gpio_status(pin, status):
    # Output GPIOs state
    GPIO.output(pin, GPIO.HIGH if status else GPIO.LOW)
    # Update GPIOs state
    #gpio_state[pin] = status


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        client.disconnect()
        print('MQTT client disconnected, exiting now.')
        pass
