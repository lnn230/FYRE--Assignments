from machine import ADC, Pin
import time

# -----------------------------
# SETTINGS
# -----------------------------

# Moisture sensor connected to A0
moisture_sensor = ADC(Pin("A0"))

# 12-bit ADC resolution: 0-4095
moisture_sensor.width(ADC.WIDTH_12BIT)

# ADC attenuation
moisture_sensor.atten(ADC.ATTN_11DB)

# ADC reference voltage
VREF = 3.3

# CSV file name
FILE_NAME = "moisture_data.csv"

# Time between readings
READ_INTERVAL = 1

# Total recording time
RECORDING_TIME = 10


# -----------------------------
# CREATE CSV FILE
# -----------------------------

with open(FILE_NAME, "w") as file:
    file.write("Time_ms,ADC_Value,Voltage_V\n")


# -----------------------------
# START RECORDING
# -----------------------------

print("Moisture Sensor Data Logger")
print("---------------------------")
print("Recording for 10 seconds...")
print()

start_time = time.ticks_ms()

while time.ticks_diff(time.ticks_ms(), start_time) < RECORDING_TIME * 1000:

    # Read ADC value
    adc_value = moisture_sensor.read()

    # Convert ADC value to voltage
    voltage = (adc_value / 4095) * VREF

    # Time since recording started
    elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)

    # Print to Serial Monitor
    print(
        "Time:", elapsed_time,
        "ms | ADC:", adc_value,
        "| Voltage:", round(voltage, 3), "V"
    )

    # Save reading to CSV
    with open(FILE_NAME, "a") as file:
        file.write("{},{},{}\n".format(
            elapsed_time,
            adc_value,
            round(voltage, 3)
        ))

    # Wait 1 second
    time.sleep(READ_INTERVAL)


# -----------------------------
# FINISHED
# -----------------------------

print()
print("---------------------------")
print("Recording complete!")
print("10 seconds of data saved to:")
print(FILE_NAME)
