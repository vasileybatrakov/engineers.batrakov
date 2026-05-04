import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)
        
        if self.verbose:
            print(f"R2R_DAC инициализирован")
            print(f"  Пины: {self.gpio_bits}")
            print(f"  Динамический диапазон: 0.00 - {self.dynamic_range:.3f} В")
    
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
        
        if self.verbose:
            print("R2R_DAC деинициализирован")
    
    def set_number(self, number):
        if number < 0:
            if self.verbose:
                print(f"Число {number} меньше 0, устанавливаем 0")
            number = 0
        elif number > 255:
            if self.verbose:
                print(f"Число {number} больше 255, устанавливаем 255")
            number = 255
        
        for i, pin in enumerate(self.gpio_bits):
            bit_value = (number >> i) & 1
            GPIO.output(pin, bit_value)
        
        if self.verbose:
            binary_repr = bin(number)[2:].zfill(8)
            print(f"Установлено число: {number} (двоичное: {binary_repr})")
    
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.3f} В выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.3f} В)")
            print("Устанавливаем 0.0 В")
            number = 0
        else:
            number = int(voltage / self.dynamic_range * 255)
        
        self.set_number(number)
        
        if self.verbose:
            expected_voltage = (number / 255) * self.dynamic_range
            print(f"Запрошено напряжение: {voltage:.4f} В")
            print(f"Ожидаемое напряжение: {expected_voltage:.4f} В")
        
        return number

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
        
        print("\nR2R 8-битный ЦАП (управление через класс)")
        print("Для выхода нажмите Ctrl+C\n")
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
                print()  # Пустая строка для разделения выводов
                
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
                
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        
    finally:
        dac.deinit()