from machine import Pin
import time


# ============================================================
# PIN ASSIGNMENTS
# ============================================================

BUTTON_PIN = 8          # D5 / GPIO8
LIGHT_SENSOR_PIN = 9    # D6 / GPIO9
EXTERNAL_LED_PIN = 6    # D3 / GPIO6
YELLOW_LED_PIN = 48     # Built-in yellow LED


# ============================================================
# PIN SETUP
# ============================================================

# ------------------------------------------------------------
# BUTTON
# ------------------------------------------------------------
#
# Wiring:
#
#       D5 / GPIO8
#             |
#          SWITCH
#             |
#            GND
#
# Internal pull-up means:
#
# NOT PRESSED = HIGH (1)
# PRESSED     = LOW  (0)
#
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)


# ------------------------------------------------------------
# LIGHT SENSOR
# ------------------------------------------------------------

sensor = Pin(LIGHT_SENSOR_PIN, Pin.IN)


# ------------------------------------------------------------
# EXTERNAL LED
# ------------------------------------------------------------

external_led = Pin(EXTERNAL_LED_PIN, Pin.OUT)


# ------------------------------------------------------------
# BUILT-IN YELLOW LED
# ------------------------------------------------------------

yellow_led = Pin(YELLOW_LED_PIN, Pin.OUT)


# ============================================================
# SYSTEM STATE
# ============================================================

armed = False


# ============================================================
# INITIAL STATE
# ============================================================

# Start disarmed
yellow_led.on()
external_led.off()


# ============================================================
# STARTUP MESSAGE
# ============================================================

print()
print("======================================")
print("       NANO ESP32 SENSOR SYSTEM")
print("======================================")
print()
print("BUTTON:       D5 / GPIO8")
print("SENSOR:       D6 / GPIO9")
print("D3 LED:       GPIO6")
print("YELLOW LED:   GPIO48")
print()
print("SYSTEM: DISARMED")
print()
print("Press button to ARM.")
print("======================================")


# ============================================================
# BUTTON DEBOUNCE VARIABLES
# ============================================================

last_button_state = button.value()

last_press_time = 0

DEBOUNCE_MS = 250


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # ========================================================
    # READ BUTTON
    # ========================================================

    current_button_state = button.value()


    # ========================================================
    # DETECT BUTTON PRESS
    # ========================================================
    #
    # We only react to the transition:
    #
    # HIGH -> LOW
    #
    # This means the button has just been pressed.
    #
    # We do NOT repeatedly toggle while the button is held.
    # ========================================================

    if current_button_state == 0 and last_button_state == 1:

        now = time.ticks_ms()

        if time.ticks_diff(now, last_press_time) > DEBOUNCE_MS:

            # Toggle armed/disarmed
            armed = not armed

            last_press_time = now


            # =================================================
            # ARMED
            # =================================================

            if armed:

                # Yellow LED OFF
                yellow_led.off()

                # Start external LED OFF
                external_led.off()

                print()
                print("--------------------------------------")
                print("SYSTEM ARMED")
                print("Sensor monitoring ACTIVE")
                print("--------------------------------------")


            # =================================================
            # DISARMED
            # =================================================

            else:

                # Yellow LED ON
                yellow_led.on()

                # D3 LED MUST be OFF
                external_led.off()

                print()
                print("--------------------------------------")
                print("SYSTEM DISARMED")
                print("Sensor monitoring INACTIVE")
                print("--------------------------------------")


    # Save button state
    last_button_state = current_button_state


    # ========================================================
    # SENSOR
    # ========================================================
    #
    # IMPORTANT:
    #
    # The sensor is ONLY read when armed.
    #
    # While disarmed, its readings have absolutely no effect.
    # ========================================================

    if armed:

        sensor_value = sensor.value()


        # ----------------------------------------------------
        # DEBUG INFORMATION
        # ----------------------------------------------------
        #
        # Uncomment this section if you want to see the
        # sensor value in the REPL.
        #
        # print("Sensor:", sensor_value)
        # ----------------------------------------------------


        # ----------------------------------------------------
        # DARKNESS
        # ----------------------------------------------------
        #
        # ASSUMPTION:
        #
        # sensor = 0 --> DARK
        # sensor = 1 --> LIGHT
        #
        # ----------------------------------------------------

        if sensor_value == 0:

            # Darkness detected
            external_led.on()

        else:

            # Light detected
            external_led.off()


    # ========================================================
    # DISARMED STATE
    # ========================================================

    else:

        # Sensor is ignored.

        # External LED must remain OFF.
        external_led.off()


    # ========================================================
    # LOOP SPEED
    # ========================================================

    time.sleep_ms(10)
