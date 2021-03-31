import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json


mqtt_broker = '192.168.1.68'
mqtt_topic = "octopi/pins/status"
PSUpin = 6

def main():
    GPIO.setmode(GPIO.BCM) #set numbering scheme
    GPIO.setup(PSUpin,GPIO.OUT)
    client = mqtt.Client()
    # Register connect callback
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, 1883, 60)
    try:
        client.loop_forever()
        sleep(60)
    except KeyboardInterrupt:
        GPIO.cleanup()

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode('utf-8')) + " on topic "+ message.topic + " with QoS " + str(messa$
    print(str(message.payload.decode('utf-8')))
    if (str(message.payload.decode('utf-8')) == "off"):
        GPIO.output(PSUpin, 1)
    elif (str(message.payload.decode('utf-8')) == "on"):
        GPIO.output(PSUpin, 0)
    else:
        print("nincs jo adat (on/off)")

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