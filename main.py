import platform
import time
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
        if autoOpen:
            client.publish("/home/doorbell","openDoor")#publish

    elif pl == "bellInt":
        print("RING RING Drin")
        notify()


def main():
    global alarm
    global autoOpen
    timeout = 0
    h = platform.uname()[1]
    broker_address="192.168.178.54"
    client = mqtt.Client(str(h))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address)
    client.loop_start()
    #openDoor(client)
    menu_def = ['BLANK', ['&Open Door', '&Activate Auto-Open', '---', '&Close']]

    tray = sg.SystemTray(menu=menu_def)
    #tray.ShowMessage("RING", "The doorbell rung", filename=None, data=None, data_base64=None, messageicon=None, time=5000)

    while True:  # The event loop
        menu_item = tray.Read(timeout=10)
        #print(menu_item)
        if menu_item == 'Close':
            break
        elif menu_item == 'Open Door':
            print(timeout)
            client.publish("/home/doorbell","openDoor")#publish
        elif menu_item == 'Deactivate Auto-Open':
            autoOpen = False
            timeout = 0
            sg.popup('Feature was deactivated!')
            menu_def = ['BLANK', ['&Open Door', '&Activate Auto-Open', '---', '&Close']]
            tray.Update(menu=menu_def)
        elif menu_item == 'Activate Auto-Open':
            input = sg.popup_get_text('Please input how long this feature should be activated in minutes (max. 60)', 'Automated Door Opening', '10', size = (50, 30))
            if input == None:
                sg.popup('Feature was not activated!')  # Shows OK button
            elif int(input) < 1 or int(input) > 60:
                sg.popup('Not a valid value!')  # Shows OK button
            else:
                autoOpen = True
                menu_def = ['BLANK', ['&Open Door', '&Deactivate Auto-Open', '---', '&Close']]
                tray.Update(menu=menu_def)
                timeout = time.time() + int(input)*60



        if alarm:
            print("alarm")
            if autoOpen:
                autoOpen = False
                tray.ShowMessage("RING - Opening", "The door has been opened automatically", filename=None, data=None, data_base64=None, messageicon=None, time=5000)
            else:
                playsound('alarm.mp3')
                tray.ShowMessage("RING", "The doorbell just rang", filename=None, data=None, data_base64=None, messageicon=SYSTEM_TRAY_MESSAGE_ICON_INFORMATION, time=5000)
            alarm = False

        #Update autoOpen
        if time.time() > timeout and timeout != 0:
            print("Timeout reached -- Disabling autoOpen")
            autoOpen = False
            timeout = 0
            menu_def = ['BLANK', ['&Open Door', '&Activate Auto-Open', '---', '&Close']]
            tray.Update(menu=menu_def)

if __name__ == "__main__":
    main()
