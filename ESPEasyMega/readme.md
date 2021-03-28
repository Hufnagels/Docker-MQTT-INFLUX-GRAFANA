# ESP EASY Mega firmware on NodeMCU
[Config parameters](espeasy-data_ESP_Easy_mega_20210114_normal_ESP8266_4M1M.json), include firmware params

## Update 28.03.2021
Not working yet. ESP MEGA firmware --> [rules tab](espeasy.rules) --> can't configure json output yet.

## Example

Config:
~~~
[[inputs.file]]
  files = ["example"]
  json_name_key = "name"
  tag_keys = ["my_tag_1"]
  json_string_fields = ["my_field"]
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
my_json,my_tag_1=foo a=5,b_c=6,my_field="description"
~~~
## Telegraf config section
~~~
[[inputs.mqtt_consumer]]
  json_name_key = "name"
  tag_keys = ["location"]
  json_string_fields = ["Room"]
  data_format = "json"
~~~
## ESP Easy Mega Rules section

Input:
~~~
{
    "Sysname":"%sysname%",
    "Taskname":"BME280",
    "temperature": [BME280#Temperature],
    "humidity": [BME280#Humidity],
    "pressure": [BME280#Pressure],
    "Room": "Livingroom",
    "location": "hu-budapest",
    "name": "esp2866"
}
~~~
Rule:
~~~
Publish %sysname%/BME280, '{
    "Sysname":"%sysname%",
    "Taskname":"BME280",
    "temperature": [BME280#Temperature],
    "humidity": [BME280#Humidity],
    "pressure": [BME280#Pressure],
    "Room": "Livingroom",
    "location": "hu-budapest",
    "name": "esp2866"
}'
~~~
