# rtd_conversion
We're using a **PT-1000 RTD** (resistance temperature detector) to measure the cold junction temperature of a thermocouple. This is to provide the reference temperature needed to calcualte the measured temperature of the thermocouples. All data is being recorded in the [PicoLog ADC 20/24](https://www.picotech.com/data-logger/adc-20-adc-24/precision-data-acquisition) datalogger.

The **RTD's resistance changes with temperature**. We implemented a simple voltage divider circuit. By measuring the voltage drop (with the datalogger), we can calculate the resistance by Ohm's Law (V = iR). See schematic for details.

This program takes in a .csv file containing the measured voltage drops across the RTD. It adds another column to the .csv file with the corresponding temperature. The input file format is `{'measured_voltage'}` and the output file format is `{'measured_voltage', 'temp'}`.

## Some Notes
- PT-1000 means a platnium RTD such that R = 1000Ω at 0°C
- i = V_2.5 / (R_100K + R_rtd)
- R_rtd varies from about 1060-1130Ω (15-33°C), but since the R_100K is so much bigger, the current can be assumed to be constant
- i_measured is around 27uA

## About the Project
I'm on a 12 week summer research exchange at the National University of Singapore (NUS). I'm working with the the [Nanomaterials and Nanosystems Innovation](http://www.hoghimwei.com/) research group. Our goal is to develop a solar reflective glass coating that can be used for ambient cooling. We are in the final testing stage. There are 2 glass houses sitting on the rooftop of the engineering buildings. One made from coated glass panels and another from regular glass panels. We are measuring the power consumption of air conditioning units placed inside the house, set to keep the room at 25°C. The coating is 5 layers of TiO2 and Ag which reflect IR radiation. We expect to see the coated glass house experience less heating from the sun and thus less energy consumption of the AC units.