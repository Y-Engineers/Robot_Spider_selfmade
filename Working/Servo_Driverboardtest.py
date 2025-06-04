import machine, time, pca9685, servo

i2c = machine.I2C( 0, sda=machine.Pin(21), scl=machine.Pin(22) )
servos = servo.Servos(i2c)


Fehler ="Angle out of range"


# Define a dictionary for servo configurations
servo_config = {
    "j1": {"index": 0, "min_angle": 45, "max_angle": 110, "reverse": False, "current_angle": 90},
    "j2": {"index": 1, "min_angle": 45, "max_angle": 110, "reverse": False, "current_angle": 90},
    "j3": {"index": 2, "min_angle": 45, "max_angle": 110, "reverse": True, "current_angle": 90},
    "j4": {"index": 3, "min_angle": 45, "max_angle": 110, "reverse": True, "current_angle": 90},
    "j5": {"index": 9, "min_angle": 45, "max_angle": 110, "reverse": False, "current_angle": 90},
    "j6": {"index": 5, "min_angle": 45, "max_angle": 110, "reverse": False, "current_angle": 90},
    "j7": {"index": 10, "min_angle": 45, "max_angle": 110, "reverse": True, "current_angle": 90},
    "j8": {"index": 11, "min_angle": 45, "max_angle": 110, "reverse": True, "current_angle": 90},
}

def Servo(servo, angle):
    if servo == "all":
        if 34 < angle < 121:
            for s in servo_config.keys():
                Servo(s, angle)
        else:
            print(Fehler)
        return

    config = servo_config.get(servo)
    if config:
        if config["min_angle"] <= angle <= config["max_angle"]:
            adjusted_angle = 180 - angle if config["reverse"] else angle
            servos.position(config["index"], degrees=adjusted_angle)
            # Aktualisiere den aktuellen Winkel im servo_config Dictionary
            servo_config[servo]["current_angle"] = angle
        else:
            print(Fehler)
    else:
        print(f"Unknown servo: {servo}")

Servo("all",90)
   
while True:
    welcher = input("servo? ")
    winkel = input("winkel? ")
    Servo(welcher, int(winkel))