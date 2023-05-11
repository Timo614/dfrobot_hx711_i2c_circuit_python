import sys
import time
import board
import dfrobot_hx711
from adafruit_clue import clue

clue_display = clue.simple_text_display(text_scale=2, colors=(clue.WHITE,))
clue_display[1].text = "Scale"

i2c = board.STEMMA_I2C()
hx711_sensor = dfrobot_hx711.DFRobot_HX711_I2C(i2c)
hx711_sensor.begin()

"""
  @brief Initialization function
"""

while True:
    if clue.button_a:
        clue_display[8].text = "Calibrating 50g"
        hx711_sensor.setTriggerWeight(50)
        hx711_sensor.setCalThreshold(1)
        hx711_sensor.enableCalibration()

        i = 0
        while hx711_sensor.peelFlag() != 2:
            time.sleep(1)
            i += 1
            if i >= 7:
                break
            
        calibration = hx711_sensor.calibration()
        clue_display[8].text = "Calibration: {:.2f}".format(calibration)
        hx711_sensor.setCalibration(calibration)
    if clue.button_b:
        hx711_sensor.peel()

    temperature = clue.temperature
    humidity = clue.humidity

    clue_display[3].text = "Temp: {:.1f} C".format(temperature)
    clue_display[5].text = "Humidity: {:.1f} %".format(humidity)
    clue_display[7].text = "Weight: {:.2f} g".format(hx711_sensor.weight(20))
    
    time.sleep(1)