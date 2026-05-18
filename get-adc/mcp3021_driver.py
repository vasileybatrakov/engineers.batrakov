import smbus

class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose
        self.resolution = 10
        self.max_value = 2 ** self.resolution - 1
    
    def deinit(self):
        """Освобождение шины I2C"""
        self.bus.close()
        if self.verbose:
            print("I2C шина закрыта")
    
    def get_number(self):
        """
        Чтение числа из микросхемы MCP3021
        Возвращает 10-битное значение (0-1023)
        """
        # Чтение двух байт из устройства
        data = self.bus.read_word_data(self.address, 0)
        
        # Разделение на старший и младший байты
        lower_data_byte = data >> 8   # байт, пришедший вторым
        upper_data_byte = data & 0xFF  # байт, пришедший первым
        
        # Извлечение 10-битного числа (согласно документации MCP3021)
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        
        if self.verbose:
            print(f"Принятые данные: {data}")
            print(f"Старший байт: {upper_data_byte:x}")
            print(f"Младший байт: {lower_data_byte:x}")
            print(f"Число: {number}")
        
        return number
    
    def get_voltage(self):
        """
        Возвращает измеренное напряжение в вольтах
        """
        digital_value = self.get_number()
        voltage = (digital_value / self.max_value) * self.dynamic_range
        
        return voltage


# Основной охранник
if __name__ == "__main__":
    try:
        # Динамический диапазон измерить мультиметром на контакте PWR блока AUX
        dynamic_range = 5.0  # Примерное значение
        adc = MCP3021(dynamic_range, verbose=False)
        
        print("Измерение напряжения через MCP3021...")
        print("Для остановки нажмите Ctrl+C\n")
        
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nИзмерение остановлено")
        
    finally:
        adc.deinit()