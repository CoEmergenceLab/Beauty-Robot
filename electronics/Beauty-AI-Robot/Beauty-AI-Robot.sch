EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Beauty"
Date "2021-09-12"
Rev ""
Comp "[phylum]"
Comment1 "Carlos Castellanos"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MCU_Module:Arduino_UNO_R3 A1
U 1 1 613D262C
P 6100 3700
F 0 "A1" H 6100 4881 50  0000 C CNN
F 1 "Arduino_UNO_R3" H 6100 4790 50  0000 C CNN
F 2 "Module:Arduino_UNO_R3" H 6100 3700 50  0001 C CIN
F 3 "https://www.arduino.cc/en/Main/arduinoBoardUno" H 6100 3700 50  0001 C CNN
	1    6100 3700
	1    0    0    -1  
$EndComp
$Comp
L dotstar:DotStar A3
U 1 1 613ED595
P 3850 4900
F 0 "A3" H 3850 5431 50  0000 C CNN
F 1 "DotStar" H 3850 5340 50  0000 C CNN
F 2 "" H 3850 4900 50  0001 C CNN
F 3 "" H 3850 4900 50  0001 C CNN
	1    3850 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 4550 3850 4550
Connection ~ 2450 4550
Wire Wire Line
	2450 5950 3700 5950
$Comp
L Motor:Motor_Servo M3
U 1 1 613F220D
P 4000 5950
F 0 "M3" H 4332 6015 50  0000 L CNN
F 1 "Motor_Servo" H 4332 5924 50  0000 L CNN
F 2 "" H 4000 5760 50  0001 C CNN
F 3 "http://forums.parallax.com/uploads/attachments/46831/74481.png" H 4000 5760 50  0001 C CNN
	1    4000 5950
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 4550 2450 5950
$Comp
L power:Earth #PWR?
U 1 1 61407324
P 3850 5350
F 0 "#PWR?" H 3850 5100 50  0001 C CNN
F 1 "Earth" H 3850 5200 50  0001 C CNN
F 2 "" H 3850 5350 50  0001 C CNN
F 3 "~" H 3850 5350 50  0001 C CNN
	1    3850 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 5300 3850 5350
$Comp
L power:Earth #PWR?
U 1 1 61408091
P 3700 6150
F 0 "#PWR?" H 3700 5900 50  0001 C CNN
F 1 "Earth" H 3700 6000 50  0001 C CNN
F 2 "" H 3700 6150 50  0001 C CNN
F 3 "~" H 3700 6150 50  0001 C CNN
	1    3700 6150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 6050 3700 6150
$Comp
L power:Earth #PWR?
U 1 1 61408EE5
P 6100 4900
F 0 "#PWR?" H 6100 4650 50  0001 C CNN
F 1 "Earth" H 6100 4750 50  0001 C CNN
F 2 "" H 6100 4900 50  0001 C CNN
F 3 "~" H 6100 4900 50  0001 C CNN
	1    6100 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 4800 6100 4900
$Comp
L SparkFun-Capacitors:100UF-POLAR-RADIAL-2.5MM-25V-20% C2
U 1 1 6140E8A9
P 1800 4800
F 0 "C2" H 1928 4845 45  0000 L CNN
F 1 "100UF-25V" H 1928 4761 45  0000 L CNN
F 2 "CPOL-RADIAL-2.5MM-6.5MM" H 1800 5050 20  0001 C CNN
F 3 "" H 1800 4800 50  0001 C CNN
F 4 "electrolytic" H 1928 4666 60  0000 L CNN "Field4"
	1    1800 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	1800 4700 1800 4550
Wire Wire Line
	1800 4550 2450 4550
Wire Wire Line
	1800 5000 1800 6050
Wire Wire Line
	1800 6050 3700 6050
Connection ~ 3700 6050
Wire Wire Line
	3700 5850 3700 5700
Wire Wire Line
	3700 5700 5450 5700
Wire Wire Line
	5450 5700 5450 4000
Wire Wire Line
	5450 4000 5600 4000
Wire Wire Line
	3600 4950 3600 5550
Wire Wire Line
	3600 5550 5000 5550
Wire Wire Line
	3600 4850 3450 4850
Wire Wire Line
	3450 4850 3450 5600
Wire Wire Line
	3450 5600 5300 5600
Wire Wire Line
	5300 5600 5300 4400
Wire Wire Line
	5300 4400 5600 4400
$Comp
L power:+5V #PWR?
U 1 1 613FB061
P 2450 4500
F 0 "#PWR?" H 2450 4350 50  0001 C CNN
F 1 "+5V" H 2465 4673 50  0000 C CNN
F 2 "" H 2450 4500 50  0001 C CNN
F 3 "" H 2450 4500 50  0001 C CNN
	1    2450 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 4500 2450 4550
$Comp
L Device:R_US R1
U 1 1 613D9CFF
P 5000 5400
F 0 "R1" H 5068 5446 50  0000 L CNN
F 1 "470" H 5068 5355 50  0000 L CNN
F 2 "" V 5040 5390 50  0001 C CNN
F 3 "~" H 5000 5400 50  0001 C CNN
	1    5000 5400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 5250 5000 4200
Wire Wire Line
	5000 4200 5600 4200
$Comp
L Beauty-AI-Robot-rescue:BigEasyDriver-BigEasyDriver A2
U 1 1 613E90F8
P 3900 1450
F 0 "A2" H 3875 2181 50  0000 C CNN
F 1 "BigEasyDriver" H 3875 2090 50  0000 C CNN
F 2 "" H 3900 1600 50  0001 C CNN
F 3 "http://www.schmalzhaus.com/BigEasyDriver/BigEasyDriver_UserManal.pdf" H 3900 1600 50  0001 C CNN
	1    3900 1450
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1400 1950 3250 1950
Wire Wire Line
	3250 1950 3250 1850
Wire Wire Line
	3150 1850 3150 1750
Wire Wire Line
	3150 1750 3250 1750
Wire Wire Line
	2800 1850 3150 1850
$Comp
L Motor:Stepper_Motor_bipolar M1
U 1 1 613F4373
P 2500 1750
F 0 "M1" H 2687 1874 50  0000 L CNN
F 1 "Stepper_Motor_bipolar" H 2687 1783 50  0000 L CNN
F 2 "" H 2510 1740 50  0001 C CNN
F 3 "http://www.infineon.com/dgdl/Application-Note-TLE8110EE_driving_UniPolarStepperMotor_V1.1.pdf?fileId=db3a30431be39b97011be5d0aa0a00b0" H 2510 1740 50  0001 C CNN
	1    2500 1750
	-1   0    0    -1  
$EndComp
Wire Wire Line
	2800 1650 3250 1650
Wire Wire Line
	2600 1450 3050 1450
Wire Wire Line
	3050 1450 3050 1550
Wire Wire Line
	3050 1550 3250 1550
Wire Wire Line
	2400 1450 2400 1350
Wire Wire Line
	2400 1350 3150 1350
Wire Wire Line
	3150 1350 3150 1450
Wire Wire Line
	3150 1450 3250 1450
$Comp
L power:Earth #PWR?
U 1 1 6140409B
P 3900 2050
F 0 "#PWR?" H 3900 1800 50  0001 C CNN
F 1 "Earth" H 3900 1900 50  0001 C CNN
F 2 "" H 3900 2050 50  0001 C CNN
F 3 "~" H 3900 2050 50  0001 C CNN
	1    3900 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 2000 3900 2050
$Comp
L SparkFun-Capacitors:10UF-POLAR-RADIAL-2.5MM-25V-20% C1
U 1 1 6140A070
P 1400 2150
F 0 "C1" H 1528 2195 45  0000 L CNN
F 1 "10UF-50V" H 1528 2111 45  0000 L CNN
F 2 "CPOL-RADIAL-2.5MM-5MM" H 1400 2400 20  0001 C CNN
F 3 "" H 1400 2150 50  0001 C CNN
F 4 "electrolytic" H 1528 2016 60  0000 L CNN "Field4"
	1    1400 2150
	1    0    0    -1  
$EndComp
Wire Wire Line
	1400 2050 1400 1950
Connection ~ 1400 1950
Wire Wire Line
	2150 2350 2150 2000
Wire Wire Line
	2150 2000 3900 2000
Connection ~ 3900 2000
Wire Wire Line
	4600 1750 5500 1750
Wire Wire Line
	4600 1550 5250 1550
$Comp
L power:+24V #PWR?
U 1 1 613F687D
P 1400 850
F 0 "#PWR?" H 1400 700 50  0001 C CNN
F 1 "+24V" H 1415 1023 50  0000 C CNN
F 2 "" H 1400 850 50  0001 C CNN
F 3 "" H 1400 850 50  0001 C CNN
	1    1400 850 
	1    0    0    -1  
$EndComp
Wire Wire Line
	1400 850  1400 1950
$Comp
L Beauty-AI-Robot-rescue:BigEasyDriver-BigEasyDriver A3
U 1 1 61498DC1
P 3900 3250
F 0 "A3" H 3875 3981 50  0000 C CNN
F 1 "BigEasyDriver" H 3875 3890 50  0000 C CNN
F 2 "" H 3900 3400 50  0001 C CNN
F 3 "http://www.schmalzhaus.com/BigEasyDriver/BigEasyDriver_UserManal.pdf" H 3900 3400 50  0001 C CNN
	1    3900 3250
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3150 3650 3150 3550
Wire Wire Line
	3150 3550 3250 3550
Wire Wire Line
	2800 3650 3150 3650
$Comp
L Motor:Stepper_Motor_bipolar M2
U 1 1 61498DCC
P 2500 3550
F 0 "M2" H 2687 3674 50  0000 L CNN
F 1 "Stepper_Motor_bipolar" H 2687 3583 50  0000 L CNN
F 2 "" H 2510 3540 50  0001 C CNN
F 3 "http://www.infineon.com/dgdl/Application-Note-TLE8110EE_driving_UniPolarStepperMotor_V1.1.pdf?fileId=db3a30431be39b97011be5d0aa0a00b0" H 2510 3540 50  0001 C CNN
	1    2500 3550
	-1   0    0    -1  
$EndComp
Wire Wire Line
	2800 3450 3250 3450
Wire Wire Line
	2600 3250 3050 3250
Wire Wire Line
	3050 3250 3050 3350
Wire Wire Line
	3050 3350 3250 3350
Wire Wire Line
	2400 3250 2400 3150
Wire Wire Line
	2400 3150 3150 3150
Wire Wire Line
	3150 3150 3150 3250
Wire Wire Line
	3150 3250 3250 3250
$Comp
L power:Earth #PWR?
U 1 1 61498DDA
P 3900 3850
F 0 "#PWR?" H 3900 3600 50  0001 C CNN
F 1 "Earth" H 3900 3700 50  0001 C CNN
F 2 "" H 3900 3850 50  0001 C CNN
F 3 "~" H 3900 3850 50  0001 C CNN
	1    3900 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 3800 3900 3850
Wire Wire Line
	1400 2350 2150 2350
Wire Wire Line
	3250 3650 3250 3750
Wire Wire Line
	3250 3750 1050 3750
Wire Wire Line
	1050 3750 1050 1950
Wire Wire Line
	1050 1950 1400 1950
Wire Wire Line
	4600 1850 5550 1850
Wire Wire Line
	5550 1850 5550 3300
Wire Wire Line
	5550 3300 5600 3300
Wire Wire Line
	5500 1750 5500 3400
Wire Wire Line
	5500 3400 5600 3400
Wire Wire Line
	5250 3500 5600 3500
Wire Wire Line
	5250 1550 5250 3500
Wire Wire Line
	5500 3650 5500 3600
Wire Wire Line
	5500 3600 5600 3600
Wire Wire Line
	4600 3650 5500 3650
Wire Wire Line
	4600 3550 4650 3550
Wire Wire Line
	4650 3550 4650 3700
Wire Wire Line
	4650 3700 5600 3700
Wire Wire Line
	4600 3350 4750 3350
Wire Wire Line
	4750 3350 4750 3800
Wire Wire Line
	4750 3800 5600 3800
$EndSCHEMATC
