import pathlib
f = open("autostart.bat", "w")
f.write("CALL " + str(pathlib.Path(__file__).parent.absolute()) + "\env\Scripts\\activate.bat\n")
f.write("start pythonw " + str(pathlib.Path(__file__).parent.absolute()) + "\main.pyw\n")
f.write("exit\n")
f.close()


#CALL C:\Users\nicho\Documents\Projekte\Windows-HomeControl\env\Scripts\activate.bat
#start pythonw C:\Users\nicho\Documents\Projekte\Windows-HomeControl\main.pyw
#exit
