import platform
import PySimpleGUIQt as sg
import paho.mqtt.client as mqtt
from playsound import playsound

alarm = False;
autoOpen = False;

def notify():
    global alarm
    alarm = True
    #ShowMessage("RING", "The doorbell rung", filename=None, data=None, data_base64=None, messageicon=None, time=5000)
    #    '''
    # Shows a balloon above icon in system tray
     #:param title:  Title shown in balloon
    # :param message: Message to be displayed
    # :param filename: Optional icon filename
    # :param data: Optional in-ram icon
    # :param data_base64: Optional base64 icon
    # :param time: How long to display message in milliseconds  :return:
    # '''

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/home/doorbell")

def on_message(client, userdata, message):
    pl = message.payload.decode("utf-8")
    print("Received message '" + pl + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    if pl == "bellExt":
        print("RING RING")
        notify()
    elif pl == "bellInt":
        print("RING RING Drin")
        notify()


def main():
    global alarm
    h = platform.uname()[1]
    broker_address="192.168.178.54"
    client = mqtt.Client(str(h))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address)
    client.loop_start()
    #openDoor(client)
    menu_def = ['BLANK', ['&Open Door', '&Auto open', '---', '&Close']]

    tray = sg.SystemTray(menu=menu_def)
    #tray.ShowMessage("RING", "The doorbell rung", filename=None, data=None, data_base64=None, messageicon=None, time=5000)

    while True:  # The event loop
        menu_item = tray.Read(timeout=10)
        #print(menu_item)
        if menu_item == 'Close':
            break
        elif menu_item == 'Open Door':
            client.publish("/home/doorbell","openDoor")#publish
        elif menu_item == 'Auto open':
            autoOpen = True


        if alarm:
            print("alarm")
            playsound('alarm.mp3')
            alarm = False
            tray.ShowMessage("RING", "The doorbell just rang", filename=None, data=None, data_base64=None, messageicon=None, time=5000)

if __name__ == "__main__":
    main()
