from machine import Pin, ADC, PWM
from time import sleep_ms

# ==========================
# SENSORS
# ==========================

light_sensor = ADC(Pin("A1"))
moisture_sensor = ADC(Pin("A2"))

LIGHT_THRESHOLD = 65000
MOISTURE_THRESHOLD = 64000

# ==========================
# LED
# ==========================

led = Pin(10, Pin.OUT)

# ==========================
# SERVO MOTOR
# ==========================

servo = PWM(Pin(8))
servo.freq(50)

current_angle = 0

def set_servo(angle):
    global current_angle

    pulse_min = 500
    pulse_max = 2500

    pulse = pulse_min + ((pulse_max - pulse_min) * angle / 180)

    duty = int((pulse / 20000) * 65535)

    servo.duty_u16(duty)
    current_angle = angle

# Start at 0掳
set_servo(0)
led.on()

print("Program Started")

# ==========================
# MAIN LOOP
# ==========================

while True:

    try:
        light_value = light_sensor.read_u16()
        moisture_value = moisture_sensor.read_u16()

        print(
            "Light =", light_value,
            "| Moisture =", moisture_value
        )

        if (light_value < 4000) or (moisture_value < MOISTURE_THRESHOLD):

            print("LIGHT OR MOISTURE DETECTED -> MOVING TO 0掳")

            set_servo(0)
            led.on()

        else:

            print("NOTHING DETECTED -> MOVING TO 90掳")

            set_servo(90)
            led.off()

    except Exception as e:
        print("Sensor Error:", e)

    sleep_ms(500) 