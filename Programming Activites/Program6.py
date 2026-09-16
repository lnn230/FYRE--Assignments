from machine import Pin, PWM
from time import sleep_ms

# -----------------------------
# Pin setup
# -----------------------------

# Microservo connected to D4
servo = PWM("D4", freq=50)

# Push button/switch connected to D8
switch = Pin("D8", Pin.IN, Pin.PULL_UP)

# -----------------------------
# Servo position function
# -----------------------------

def set_servo_angle(angle):
    # Convert 0-180 degrees to servo duty cycle
    min_duty = 26
    max_duty = 128

    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty(duty)


# Start servo at 0 degrees
position = 0
set_servo_angle(position)

# -----------------------------
# Main loop
# -----------------------------

last_switch_state = 1

while True:

    current_switch_state = switch.value()

    # Detect button press
    if last_switch_state == 1 and current_switch_state == 0:

        # Toggle servo position
        if position == 0:
            position = 180
        else:
            position = 0

        set_servo_angle(position)

        # Debounce
        sleep_ms(300)

    last_switch_state = current_switch_state

    sleep_ms(10)

