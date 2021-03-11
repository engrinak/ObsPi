# ObsPi

## GetMagData.py
The script "GetMagData.py" was written to get magnetometer readings from the magnetometer below:
  * [Military-Grade Magnetometer Compensation Chip] PNI RM3100
  * This sensor can easily be found online for about $38. 

Anyway, this script is really all there is to it - just copy it to your Pi, connect up the sensor and run it. The output goes to a text file called "magtest.txt"
The readings are not calibrated to any known value, but they do respond to changes and fluctuations in the earth's magnetic field.

## Jupyter Notebooks
There are several jupyter notebooks that I used for analyzing the data collected and comparing with data from a USGS observatory. Basically I wanted to see 
if the sensor could detect changes in the earth's magnetic field during geomagnetic disturbances (Aurora). And I found that it does, although there is quite a lot of
noise to filter out.

