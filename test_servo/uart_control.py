import serial
import time

class RobotArmController:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/serial0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        time.sleep(2)
    
    def send_command(self,cmd):
        self.ser.write(f"{cmd}\n".encode())
        response=self.ser.readline().decode().strip()
        return response

if __name__ == "__main__":
    arm=RobotArmController()
    
    while True:
        user_input= input("Commande (open/close/quit): ")
        if user_input == "quit":
            break
        response =arm.send_command(user_input)
        print(f"ESP32 > {response}")
        
    arm.ser.close()
    