import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        self.resolution = 8
        self.max_value = 2 ** self.resolution - 1
        
        # GPIO пины для R2R ЦАП
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def deinit(self):
        """Деструктор"""
        self.number_to_dac(0)
        GPIO.cleanup(self.bits_gpio + [self.comp_gpio])
        if self.verbose:
            print("GPIO очищены")
    
    def number_to_dac(self, number):
        """Подача числа на ЦАП"""
        if number < 0 or number > self.max_value:
            number = self.max_value if number > self.max_value else 0
        
        for i, pin in enumerate(self.bits_gpio):
            bit = (number >> (self.resolution - 1 - i)) & 1
            GPIO.output(pin, bit)
    
    def sequential_counting_adc(self):
        """
        Алгоритм последовательного счёта для АЦП
        Возвращает найденное число (0-255)
        """
        self.number_to_dac(0)
        time.sleep(self.compare_time)
        
        # Последовательно увеличиваем число пока ЦАП не превысит входное
        for number in range(self.max_value + 1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            
            comparator_output = GPIO.input(self.comp_gpio)
            
            if self.verbose and number % 50 == 0:
                print(f"Проверка числа: {number}")
            
            # Если напряжение ЦАП превысило входное
            if comparator_output == 1:
                return number
        
        return self.max_value
    
    def get_sc_voltage(self):
        """Возвращает измеренное напряжение в вольтах"""
        digital_value = self.sequential_counting_adc()
        voltage = (digital_value / self.max_value) * self.dynamic_range
        return voltage


# Основной охранник
if __name__ == "__main__":
    try:
        dynamic_range = 5.0  # Измерить мультиметром
        adc = R2R_ADC(dynamic_range, compare_time=0.01, verbose=False)
        
        print("Измерение напряжения (последовательный счёт)...")
        print("Вращайте потенциометр U\n")
        
        while True:
            voltage = adc.get_sc_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nИзмерение остановлено")
        
    finally:
        adc.deinit()