import time
from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const
import struct

I2C_ADDR                   = const(0x64)  # Get sensor raw data
REG_CLEAR_REG_STATE      = const(0x65)  # Get sensor raw data
REG_DATA_GET_RAM_DATA      = const(0x66)  # Get sensor raw data
REG_DATA_GET_CALIBRATION   = const(0x67)  # Gets the automatic calibration value
REG_DATA_GET_PEEL_FLAG     = const(0x69)  # Obtain peeling position
REG_DATA_INIT_SENSOR     = const(0x70)  # Module initialization
REG_SET_CAL_THRESHOLD      = const(0x71)  # Set the calibration trigger threshold
REG_SET_TRIGGER_WEIGHT     = const(0x72)  # Set calibration weight

REG_CLICK_RST      = const(0x73)  # Simulation of RST
REG_CLICK_CAL     = const(0x74)  # Simulation of CAL

class DFRobot_HX711_I2C:
  def __init__(self, i2c, addr = I2C_ADDR):
    self._addr = addr
    self.i2c_device = I2CDevice(i2c, self._addr)
    self.buffer = bytearray(3)
    self.rxbuf = bytearray(16)

  def begin(self):
    time.sleep(0.03)
    self.buffer[0] = REG_DATA_INIT_SENSOR
    self._write_register()
    time.sleep(0.03)
    self.buffer[0] = REG_CLEAR_REG_STATE
    self._write_register()
    time.sleep(0.03)
    self._offset = self.average(1)
    self._calibration = 1752.60
    self.setCalibration(self._calibration)

  def average(self, times = 1):
    sum = 0
    for i in range(times):
        sum += self.raw_weight()
    return (sum / times)

  def weight(self, times = 1):
    weight = self.average(times)
    
    time.sleep(0.05)
    peel_flag = self.peelFlag()
    if peel_flag == 1:
        self._offset = self.average(times)
    elif peel_flag == 2:
        self._calibration = self.calibration()
        
    return (weight - self._offset) / self._calibration

  def raw_weight(self):
    self.buffer[0] = REG_DATA_GET_RAM_DATA
    self._write_register()
    time.sleep(0.03)
    self._read_register(4)
    return ((self.rxbuf[0]<<24)|(self.rxbuf[1]<<16)|(self.rxbuf[2]<<8)|self.rxbuf[3])

  def peel(self):
    self._offset = self.average(1)
    self.buffer[0] = REG_CLICK_RST
    self._write_register()
    time.sleep(0.03)

  def peelFlag(self):
    self.buffer[0] = REG_DATA_GET_PEEL_FLAG
    self._write_register()
    time.sleep(0.03)
    self._read_register(1)
    if self.rxbuf[0] == 1:
        return 1
    elif self.rxbuf[0] == 2:
        return 2
    
    return 0

  def calibration(self):
    self.buffer[0] = REG_DATA_GET_CALIBRATION
    self._write_register()
    time.sleep(0.03)
    self._read_register(4)

    data = bytearray(self.rxbuf)
    value = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
    return struct.unpack('>f', struct.pack('>I', value))[0]

  def enableCalibration(self):
    self.buffer[0] = REG_CLICK_CAL
    self._write_register()
    time.sleep(0.03)

  def setCalibration(self,cal):
    self._calibration = cal
  
  def setCalThreshold(self,cal):
    self.buffer[0] = REG_SET_CAL_THRESHOLD
    tx_data = struct.pack('>H', cal)
    self.buffer[1] = tx_data[0]
    self.buffer[2] = tx_data[1]
    self._write_register()
    time.sleep(0.03)

  def setTriggerWeight(self,weight):
    self.buffer[0] = REG_SET_TRIGGER_WEIGHT
    tx_data = struct.pack('>H', weight)
    self.buffer[1] = tx_data[0]
    self.buffer[2] = tx_data[1]
    self._write_register()
    time.sleep(0.03)

  def _write_register(self):
    with self.i2c_device as i2c:
      i2c.write(self.buffer)

  def _read_register(self, length):
    with self.i2c_device as i2c:
        i2c.readinto(self.rxbuf)
