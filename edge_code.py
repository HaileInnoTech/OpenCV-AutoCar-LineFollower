import paho.mqtt.client as mqtt
import pymysql

broker_address = "35.165.89.144"
topic = "linetracking"
port = 1883

# Connect to the database
try:
    connection = pymysql.connect(
        host='35.165.89.144',
        user='haile',
        password='12345678',
        database='Project3',
    )   
    print("Connection to the database successful!")
    
except pymysql.MySQLError as error:
    print("Failed to connect to the database: {}".format(error))
    # Close the connection
    connection.close()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    # Insert the message payload into the database
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Movement (CarMovement) VALUES (%s)"
            cursor.execute(sql, (str(msg.payload.decode()),))
            connection.commit()
            print("Message inserted successfully!")
            
    except pymysql.MySQLError as error:
        print("Failed to insert message into the database: {}".format(error))

    print("Received message: " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port, 60)
client.loop_forever()