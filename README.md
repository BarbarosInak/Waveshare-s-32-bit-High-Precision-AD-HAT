# Waveshare-s-32-bit-High-Precision-AD-HAT
In this project, I tried to make 32-bit High-Precision AD HAT work on Jetson Nano. The codes below could be used on Raspberry Pi too. Because they have the same pin structure as the Jetson Nano. Before running codes, you should change your device's mode to SPI. You can switch mode from the following code block, which could be used in the terminal(for Jetson Nano).

$ sudo /opt/nvidia/jetson-io/jetson-io.py

for further information about SPI, you can check: https://www.jetsonhacks.com/2020/05/04/spi-on-jetson-using-jetson-io/

Unfortunately, AD HAT is not working as they intended to. You can get a maximum sampling rate between 4500 SPS and 5000 SPS. I recommend you to work with only one channel instead of using all channels. Switching channel for getting values makes lose a lot of time that you will not be able to sample signals around 2 kHz.

--ads1263.py -- This python file is an edited version of the original ADS1263.py. You can find the original file from:https://www.waveshare.com/wiki/High-Precision_AD_HAT This file is arranged to work faster than the original file.

--config.py-- This file is also edited. The difference from the original file is that the delay_miliseconds function has been changed to not work and SPI speed has been set to the maximum level.

--32_bit_ad_hat.py-- When you run this python file you will see a UI. With this UI you can arrange the number of samples, starting frequency of the frequency spectrum, and the sampling rate of the AD HAT.

--dc_live_plotting.py-- This code plots only the time-domain version of the input signal. As time passes points on the plot increase, not like 32_bit_ad_hay.py.

Thanks for reading.
