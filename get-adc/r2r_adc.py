import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.0001, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        self.resolution = 8  # 8-bit ADC
        self.max_value = 2 ** self.resolution - 1
        
        # GPIO пины для R2R ЦАП (биты от старшего к младшему)
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21  # Пин компаратора
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def deinit(self):
        """Деструктор - сброс ЦАП в 0 и очистка GPIO"""
        self.number_to_dac(0)
        GPIO.cleanup(self.bits_gpio + [self.comp_gpio])
        if self.verbose:
            print("GPIO очищены")
    
    def number_to_dac(self, number):
        """Подача числа на параллельный вход ЦАП"""
        if number < 0 or number > self.max_value:
            raise ValueError(f"Число должно быть в диапазоне 0-{self.max_value}")
        
        for i, pin in enumerate(self.bits_gpio):
            bit = (number >> (self.resolution - 1 - i)) & 1
            GPIO.output(pin, bit)
        
        if self.verbose:
            print(f"На ЦАП подано число: {number}")
    
    def successive_approximation_adc(self):
        number = 0
        
        # Бинарный поиск от старшего бита к младшему
        for bit in range(self.resolution - 1, -1, -1):
            test_value = number | (1 << bit)
            self.number_to_dac(test_value)
            time.sleep(self.compare_time)
            
            # Чтение выхода компаратора
            comparator_output = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"Бит {bit}: тест={test_value}, комп={comparator_output}")
            
            # Если напряжение ЦАП меньше входного, сохраняем бит
            if comparator_output == 0:
                number = test_value
        
        return number
    
    def get_sar_voltage(self):
        """
        Возвращает измеренное напряжение в вольтах
        """
        digital_value = self.successive_approximation_adc()
        voltage = (digital_value / self.max_value) * self.dynamic_range
        
        if self.verbose:
            print(f"Цифровое значение: {digital_value}, Напряжение: {voltage:.3f} В")
        
        return voltage


# Основной охранник
if __name__ == "__main__":
    try:
        # Динамический диапазон нужно измерить мультиметром
        dynamic_range = 5.0  # Примерное значение, нужно измерить
        adc = R2R_ADC(dynamic_range, compare_time=0.0001, verbose=False)
        
        print("Измерение напряжения...")
        print("Вращайте потенциометр U на плате get-adc")
        print("Для остановки нажмите Ctrl+C\n")
        
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nИзмерение остановлено")
        
    finally:
        adc.deinit()