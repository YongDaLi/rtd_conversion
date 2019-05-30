'''
Yong Da Li
Thursday, May 30, 2019
Professor Ho Ghim Wei

Using RTD to measure cold junction temperature of data loggger on rooftop experiment.
Implemented simple voltage divider circuit with 2V5 input (from PicoLog breakout)
This program converts .csv with measured ADC voltages from RTD to temperature.
'''

import math
import csv

# coefficients from standard ITS 90
a = 3.90830E-03
b = -5.775E-07
c = -4.183E-12

# since PT1000, assume R = 1000Ω at 0°C
r0 = 1000
r_100K = 89.6e3
v_supply = 2.50 

# measured current is 23uA, by i = V / (R_100K + R_rtd)
i_measured = 27e-6


# converts temperature to resistance
def temp_to_res(temp):
    if (temp > 0):
        r = r0 * (1 + a*temp + b*temp*temp + c*(temp - 100)*temp*temp*temp)
    else: #temp > 0
        r = r0 * (1 + a*temp + b*temp*temp)

    return r


# converts resistance to temperature
def res_to_temp(res):

    # quadratic equation
    num = -r0*a + math.sqrt(r0*r0*a*a - 4*r0*b*(r0-res))
    denum = 2*r0*b

    temp = num/denum

    return temp


# converts voltage drop across RTD to temperature
def voltage_to_temp(v_measured):
    res = (r_100K*v_measured) / (v_supply - v_measured)
    temp = res_to_temp(res)

    print("volt:", v_measured, "\tres:", round(res, 4), "\ttemp:", round(temp, 4))

    return temp


# converts temperature to expected voltage drop across RTD
def temp_to_voltage(temp):
    res = temp_to_res(temp)
    volt = v_supply * res /(res + r_100K)

    print("temp:", round(temp, 4), "\tres:", round(res, 4), "\tvolt:", volt)

    return volt


# driver for command line conversion mode
def convert_cli():
    print("\nCommand line mode selected\n")
    choice = 0

    while (1):
        print("   (command line mode)")
        print("0. quit")
        print("1. temperature to resistance")
        print("2. resistance to temperature")
        print("3. voltage to temperature")
        print("4. temperature to voltage")

        choice = float(input("\nEnter choice: "))

        if choice == 0:
            return

        elif choice == 1:
            temp = float(input("Enter temperature (°C): "))
            print("Resistance: ", temp_to_res(temp), "Ω")

        elif choice == 2:
            res = float(input("Enter resistance (Ω): "))
            print("Temperature: ", res_to_temp(res), "°C")

        elif choice == 3:
            volt = float(input("Enter measured voltage (V): "))
            print("Temperature: ", voltage_to_temp(volt), "°C")

        elif choice == 4:
            temp = float(input("Enter measured temp (°C): "))
            print("Expected Voltage: ", temp_to_voltage(temp), "V")

        print("-"*30, "\n")


# driver for .csv file conversion mode
def convert_csv():
    print("\ncsv mode selected")
    print("Enter `quit` to quit\n")

    input_file = input("Enter a input file name: ")
    if input_file == "quit":
        return

    output_file = input("Enter output file name: ")

    line_count = 0
    measured_voltage = []

    # read input file
    with open(input_file) as in_csv:
        reader = csv.DictReader(in_csv)

        for row in reader:
            measured_voltage.append(float(row['measured_voltage']))
            line_count = line_count + 1

    print("\nRead " + str(line_count) + " lines in file: " + input_file)

    # write output file
    with open("output/" + output_file, 'w', newline='') as out_csv:
        fieldnames = ['measured_voltage', 'R_rtd', 'temp']
        writer = csv.DictWriter(out_csv, fieldnames = fieldnames)
        writer.writeheader()

        for i in range (0, line_count):
            temp = voltage_to_temp(measured_voltage[i]);
            res = temp_to_res(temp)
            writer.writerow({'measured_voltage': measured_voltage[i], 'R_rtd': res, 'temp': temp})

    print("Conversion finished, converted " + str(line_count) + " lines to output file: " + output_file)


def main():
    print("\n--- PT1000 Resistance Temperature Detector ---")
    print("- calibrated for PicoLog voltage divider circuit")
    print("last modified May 30, 2019 by Yong Da Li")
    print("------------------------------------------------\n")

    while(1):
        print("   (main menu)")
        print("0. quit")
        print("1. command line")
        print("2. csv\n")
        choice = int(input("Enter choice: "))

        if choice == 0:
            return
        elif choice == 1:
            convert_cli()
        elif choice == 2:
            convert_csv()

        print("-" * 20)

main()