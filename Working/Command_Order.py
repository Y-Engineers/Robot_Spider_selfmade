import machine, time, pca9685, servo

i2c = machine.I2C( 0, sda=machine.Pin(21), scl=machine.Pin(22) )
servos = servo.Servos(i2c)


Fehler ="Angle out of range"


# Define a dictionary for servo configurations
servo_config = {
    "j1": {"index": 0, "min_angle": 45, "max_angle": 110, "reverse": True, "current_angle": 90},
    "j2": {"index": 1, "min_angle": 45, "max_angle": 110, "reverse": False, "current_angle": 90},
    "j3": {"index": 2, "min_angle": 45, "max_angle": 110, "reverse": True, "current_angle": 90},
    "j4": {"index": 3, "min_angle": 45, "max_angle": 110, "reverse": True, "current_angle": 90},
    "j5": {"index": 9, "min_angle": 45, "max_angle": 110, "reverse": False, "current_angle": 90},
    "j6": {"index": 5, "min_angle": 45, "max_angle": 110, "reverse": False, "current_angle": 90},
    "j7": {"index": 10, "min_angle": 45, "max_angle": 110, "reverse": False, "current_angle": 90},
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

def move_with_speed(servo, angle, speed):
    # Check if we're dealing with multiple servos
    if isinstance(servo, list) and isinstance(angle, list):
        if len(servo) != len(angle):
            print("Error: Number of servos and angles must match")
            return
            
        # Get current angles and calculate max steps needed
        servo_data = []
        max_steps = 0
        
        for i, servo_name in enumerate(servo):
            config = servo_config.get(servo_name)
            if not config:
                print(f"Unknown servo: {servo_name}")
                return
                
            current_angle = config["current_angle"]
            target_angle = angle[i]
            
            # Check if angle is in range
            if not (config["min_angle"] <= target_angle <= config["max_angle"]):
                print(f"{Fehler} for {servo_name}: {target_angle}")
                return
                
            steps_needed = abs(target_angle - current_angle)
            max_steps = max(max_steps, steps_needed)
            
            servo_data.append({
                "name": servo_name,
                "start": current_angle,
                "target": target_angle
            })
        
        # Execute simultaneous movement
        for step in range(1, max_steps + 1):
            for s in servo_data:
                start = s["start"]
                target = s["target"]
                
                if start == target:
                    continue
                
                # Calculate progress ratio
                progress = step / max_steps
                
                # Calculate new angle for this step
                if target > start:
                    new_angle = start + int(progress * (target - start))
                else:
                    new_angle = start - int(progress * (start - target))
                
                Servo(s["name"], new_angle)
            
            time.sleep(0.01 * speed)
        
    else:
        # Original single servo code
        config = servo_config.get(servo)
        anglestart = config["current_angle"]
        to_clear = angle - anglestart
        print("start angle "+str(anglestart))
        print("goal angle "+str(angle))
        print("to clear "+str(to_clear))
        print("with speed "+str(speed))
        if to_clear < 0:
            for i in range(0,to_clear*(-1)+1):
                Servo(servo,(anglestart-i))
                time.sleep(0.01*speed)
        if to_clear >0:
            for i in range(0,to_clear+1):
                Servo(servo,(anglestart+i))
                time.sleep(0.01*speed)

            
def execute_sequence(sequence):
    for command in sequence:
        if command[0]=="wait":
            time.sleep(command[1])
        else:
            move_with_speed(command[0],command[1],command[2])

time.sleep(1.2)

def generate_sequences(factor=1):
    global wave, stand_up, step_forward, step_backward, turn_left, turn_right
    wave = [
        ["j1",135,0.5],
        ["j2",110,0.5],
        ["j2",45,0.5],
    ]
    stand_up= [
        [["j1","j3","j5","j7"], [90,90,90,90],0.5],
        [["j2","j4","j6","j8"], [45,45,45,45],0.5],
        ["wait", 0.3],
    ]


    step_forward=[
        [["j2","j6",], [60,60],0.4],
        [["j1","j5",], [90+(20*factor),90+(20*factor)],0.5],
        [["j2","j6",], [45,45],0.4],
        
        [["j4","j8","j1","j5"], [60,60,90,90],0.4],
        [["j3","j7",], [90+(20*factor),90+(20*factor)],0.5],
        [["j4","j8",], [45,45],0.4],
        
        [["j3","j7"], [90,90],0.4],
        
        ]

    step_backward=[
        [["j2","j6",], [60,60],0.4],
        [["j1","j5",], [90-(20*factor),90-(20*factor)],0.5],
        [["j2","j6",], [45,45],0.4],
        
        [["j4","j8","j1","j5"], [60,60,90,90],0.4],
        [["j3","j7",], [90-(20*factor),90-(20*factor)],0.5],
        [["j4","j8",], [45,45],0.4],
        
        [["j3","j7"], [90,90],0.4],
        
    ]

    turn_left = [
        [["j4","j8","j3","j7"], [60,60,90-(20*factor),90+(20*factor),],0.4],
        [["j4","j8"], [45,45,],0.4],
        
        [["j2","j6",], [60,60],0.4],
        [["j3","j7","j1","j5"], [90,90,90-(20*factor),90+(20*factor)],0.4],
        [["j2","j6",], [45,45],0.4],
        [["j4","j8","j1","j5"], [60,60,90,90],0.4],
        [["j4","j8",], [45,45],0.4],
    ]
    turn_right = [
        [["j4","j8","j3","j7"], [60,60,90+(20*factor),90-(20*factor)],0.4],
        [["j4","j8"], [45,45],0.4],
        
        [["j2","j6",], [60,60],0.4],
        [["j3","j7","j1","j5"], [90,90,90+(20*factor),90-(20*factor)],0.4],
        [["j2","j6",], [45,45],0.4],
        [["j4","j8","j1","j5"], [60,60,90,90],0.4],
        [["j4","j8",], [45,45],0.4],  
    ] 
generate_sequences()

execute_sequence(stand_up)
for i in range(5):
    execute_sequence(step_forward)
generate_sequences(0.5)
time.sleep(2)
for i in range(5):
    execute_sequence(step_forward)

