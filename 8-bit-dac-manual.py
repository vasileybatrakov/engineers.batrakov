import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
leds = [22, 27, 17, 26, 25, 21, 20, 16]
GPIO.setup(leds, GPIO.OUT)
dynamic_range = 3.3

def voltage_to_number(voltage):
    if not(0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00-{dynamic_range:.2f} B")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    if number < 0:
        number = 0
    elif number >255:
        number = 255
    for i, pin in enumerate(leds):
        bit_value = (number >> i) & 1
        GPIO.output(pin, bit_value)
    print(f"Установлено значение {number} ({bin(number)[2:].zfill(8)})")

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")

finally:
    GPIO.output(leds, 0)
    GPIO.cleanup()