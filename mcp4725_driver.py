import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        """
        dynamic_range: опорное напряжение (например, 5.0 В)
        address: I2C адрес MCP4725 (по умолчанию 0x61)
        verbose: вывод отладочной информации
        """
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00       # обычный режим записи
        self.pds = 0x00      # нормальный режим работы (не power-down)
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        """Закрыть шину I2C"""
        self.bus.close()

    def set_number(self, number):
        """Установить выходное напряжение напрямую 12-битным числом (0–4095)"""
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
            print(f"Число: {number}, отправленные по I2C данные: "
                  f"[0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        """Выставить напряжение на выходе (0 ... dynamic_range)"""
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В выходит за диапазон 0..{self.dynamic_range} В")
            return

        # Преобразование напряжения в 12-битный код
        number = int((voltage / self.dynamic_range) * 4095)
        number = max(0, min(4095, number))  # защита от округления
        self.set_number(number)


# Основной охранник (пример использования)
if __name__ == "__main__":
    dac = MCP4725(dynamic_range=5.0, verbose=True)

    try:
        # Тест: установка 2.5 В
        dac.set_voltage(2.5)

        # Тест: прямая установка числа
        dac.set_number(2048)

    finally:
        dac.deinit()
