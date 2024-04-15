import sys
import pika
import csv
import datetime as dt

# Create a global channel variable to hold our channel object in
channel = None
exchange_name = None
acc_x = 0
acc_y = 0
acc_z = 0
gy_x = 0
gy_y = 0
gy_z = 0
mf_x = 0
mf_y = 0
mf_z = 0
prox = 0
li = 0
label = 'unlabelled'
i = 0
j = 0
csvfile = None
writer = None
# Step #2
def on_open(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    global csvfile, writer
    csvfile = open('buffer.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(["SL_NO", "ACCELEROMETER_X", "ACCELEROMETER_Y", "ACCELEROMETER_Z", "GYROSCOPE_X", "GYROSCOPE_Y", "GYROSCOPE_Z", "MAGNETIC_FIELD_X", "MAGNETIC_FIELD_Y", "MAGNETIC_FIELD_Z", "PROXIMITY", "LIGHT", "TIME", "CONTEXT"])
    connection.channel(on_open_callback=on_channel_open)

def on_channel_open(new_channel):
    global channel
    global exchange_name
    channel = new_channel
    channel.queue_declare(queue="", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

def on_queue_declared(frame):
    queue_name = frame.method.queue
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='ACCELEROMETER.0')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='ACCELEROMETER.1')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='ACCELEROMETER.2')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='GYROSCOPE.0')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='GYROSCOPE.1')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='GYROSCOPE.2')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='MAGNETIC_FIELD.0')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='MAGNETIC_FIELD.1')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='MAGNETIC_FIELD.2')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='PROXIMITY.0')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='LIGHT.0')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='CONTEXT')

    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.basic_consume(
    queue=queue_name, on_message_callback=handle_delivery, auto_ack=True)


# Step #5
def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    global i, j, acc_x, acc_y, acc_z, gy_x, gy_y, gy_z, mf_x, mf_y, mf_z, prox, li, label
    if method.routing_key == 'ACCELEROMETER.0':
        acc_x = body.decode()
    if method.routing_key == 'ACCELEROMETER.1':
        acc_y = body.decode()
    if method.routing_key == 'ACCELEROMETER.2':
        acc_z = body.decode()
    if method.routing_key == 'GYROSCOPE.0':
        gy_x = body.decode()
    if method.routing_key == 'GYROSCOPE.1':
        gy_y = body.decode()
    if method.routing_key == 'GYROSCOPE.2':
        gy_z = body.decode()
    if method.routing_key == 'MAGNETIC_FIELD.0':
        mf_x = body.decode()
    if method.routing_key == 'MAGNETIC_FIELD.1':
        mf_y = body.decode()
    if method.routing_key == 'MAGNETIC_FIELD.2':
        mf_z = body.decode()
    if method.routing_key == 'PROXIMITY.0':
        prox = body.decode()
    if method.routing_key == 'LIGHT.0':
        li = body.decode()
    if method.routing_key == 'CONTEXT':
        label = body.decode()

    i = i + 1

    if i % 15 == 0 :
        j = j + 1
        print(f" [{j}]: {acc_x}, {acc_y}, {acc_z}, {gy_x}, {gy_y}, {gy_z}, {mf_x}, {mf_y}, {mf_z}, {prox}, {li}, {dt.datetime.now().strftime('%H:%M:%S.%f')}, {label}")
        writer.writerow([j, acc_x, acc_y, acc_z, gy_x, gy_y, gy_z, mf_x, mf_y, mf_z, prox, li, dt.datetime.now().strftime('%H:%M:%S.%f'), label])
        csvfile.flush()

# Closing
def on_close(connection, exception):
    # Invoked when the connection is closed
    connection.ioloop.stop()

# Step #1: Connect to RabbitMQ using the default parameters
credentials = pika.PlainCredentials('rishiagl', '1234')
parameters = pika.ConnectionParameters('52.66.250.239', 5672, 'vh1', credentials)
connection = pika.SelectConnection(parameters=parameters, on_open_callback=on_open, on_close_callback=on_close)

try:
    # Loop so we can communicate with RabbitMQ
    if len(sys.argv) < 2:
        print("Please Exchange Name")
        sys.exit(0)
    exchange_name = sys.argv[1]
    connection.ioloop.start()
    
except KeyboardInterrupt:
    # Gracefully close the connection
    
    connection.close()
    csvfile.close()
    # Loop until we're fully closed.
    # The on_close callback is required to stop the io loop
    connection.ioloop.start()