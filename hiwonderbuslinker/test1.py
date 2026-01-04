from lewansoul_servo_bus import ServoBusCommunication

servo_bus = ServoBusCommunication('COM10')

# Move servo with ID 1 to 90 degrees in 1.0 seconds
servo_bus.pos_set(4, 500, 0.1)
