# DFRobot HX711 i2c Scale Circuit Python support

This is a circuit python library for interfacing with the DFRobot HX711 scale that communicates over i2c. You can see their libraries for integration with arduino here: https://github.com/DFRobot/DFRobot_HX711_I2C

Video showing it in use: https://youtu.be/K0jk2dn-1A8

Product page: https://www.dfrobot.com/product-2289.html

## Using

```
i2c = board.STEMMA_I2C()
hx711_sensor = dfrobot_hx711.DFRobot_HX711_I2C(i2c)
hx711_sensor.begin()
```

These calls start up the i2c link and start the scale initialization logic by sending that associated instruction. After this point the scale can be queried via the weight method.

```
hx711_sensor.weight(20)
```

From this example it's calling the weight 20 times and averaging it out.

In addition there's logic for reseting the scale to 0 pare/peel it. Example code for the adafruit clue shows using the buttons for both calibration and later pareing it back to 0.

## Background

I had originally attempted to use their sample code for their python library but no matter what I did I couldn't get the scale to be recognized. I then looked over their arduino code and was able to emulate the same i2c procedure here for getting data off of the scale. Their python library appears to reference the wrong i2c address and it lacks the instruction to initialize ths scale so I'm not sure if it ever or could work for that matter.
