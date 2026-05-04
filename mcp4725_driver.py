import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range
    
    def deinit(self):
        self.bus.close()
        if self.verbose:
            print("I2C шина закрыта")
    
    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return
        
        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return
        
        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)
        
        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]")
    
    def set_voltage(self, voltage):
        if voltage < 0:
            voltage = 0
        if voltage > self.dynamic_range:
            voltage = self.dynamic_range
        
        number = int((voltage / self.dynamic_range) * 4095)
        self.set_number(number)
        
        if self.verbose:
            print(f"Установлено напряжение: {voltage:.3f} В")

if __name__ == "__main__":
    try:
        dac = MCP4725(5.0, 0x61, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()