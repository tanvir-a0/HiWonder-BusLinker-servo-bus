from lewansoul_servo_bus import ServoBusCommunication

class SafeServoBus:
    """Wrapper for ServoBusCommunication with position limits protection"""
    
    def __init__(self, port, servo_limits):
        """
        :param port: Serial port (e.g., 'COM10')
        :param servo_limits: Dictionary of {servo_id: (min_pos, max_pos)}
        """
        self.bus = ServoBusCommunication(port)
        self.servo_limits = servo_limits
    
    def pos_set(self, servo_id, position, time_s):
        """Move servo with automatic position limit protection"""
        if servo_id in self.servo_limits:
            min_pos, max_pos = self.servo_limits[servo_id]
            if position < min_pos or position > max_pos:
                raise ValueError(
                    f"Position {position} out of bounds for servo {servo_id}! "
                    f"Allowed range: {min_pos}-{max_pos}"
                )
        self.bus.pos_set(servo_id, position, time_s)
    
    def __getattr__(self, name):
        """Forward all other methods to the underlying bus"""
        return getattr(self.bus, name)

# Configure servo limits - add more servos as needed
SERVO_LIMITS = {
    4: (300, 1000),  # Servo 4: min=300, max=1000
    5: (0, 1000),    # Servo 5: min=0, max=1000
    2: (500, 850),   # Servo 2: min=200, max=800 #if more then 850 servo just clases with holder and 500 is toal vertical up
}

servo_bus = SafeServoBus('COM12', SERVO_LIMITS)
servo_id = 4

def get_servo_info(servo_id):
    """Get display info for current servo"""
    if servo_id in SERVO_LIMITS:
        min_pos, max_pos = SERVO_LIMITS[servo_id]
        return f"Servo {servo_id} | Limits: {min_pos}-{max_pos}"
    else:
        return f"Servo {servo_id} | No limits set (use 0-1000)"

print("Servo Control Interface")
print("Commands:")
print("  select <id>     - Switch to servo ID")
print("  <position>      - Move to position (1s default)")
print("  <position> <time> - Move to position in time seconds")
print("  Ctrl+C          - Exit")
print(f"\nCurrent: {get_servo_info(servo_id)}\n")

try:
    while True:
        user_input = input(f"[Servo {servo_id}] > ").strip()
        
        if not user_input:
            continue
        
        try:
            parts = user_input.split()
            
            # Check for select command
            if parts[0].lower() == 'select' and len(parts) == 2:
                new_servo_id = int(parts[1])
                servo_id = new_servo_id
                print(get_servo_info(servo_id))
                continue
            
            if len(parts) == 1:
                # Just position, use default time of 1 second
                position = int(parts[0])
                time_s = 1.0
            elif len(parts) == 2:
                # Position and time provided
                position = int(parts[0])
                time_s = float(parts[1])
            else:
                print("Invalid format. Use: position, position time, or select <id>")
                continue
            
            # Validate position is within limits if defined
            if servo_id in SERVO_LIMITS:
                min_position, max_position = SERVO_LIMITS[servo_id]
                if position < min_position or position > max_position:
                    print(f"ERROR: Position {position} is out of bounds!")
                    print(f"Allowed range: {min_position} - {max_position}")
                    continue
            
            # Move the servo
            servo_bus.pos_set(servo_id, position, time_s)
            print(f"Moving servo {servo_id} to {position} in {time_s}s")
            
        except ValueError:
            print("Invalid input. Please enter numbers only.")
        except Exception as e:
            print(f"Error: {e}")

except KeyboardInterrupt:
    print("\n\nExiting...")
finally:
    # Optional: Power off servo or cleanup
    pass
