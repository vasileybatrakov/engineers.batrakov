import smbus
import time
import math

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range
        self.resolution = 12
        self.max_value = 4095
        
        if self.verbose:
            print(f"MCP4725 инициализирован: адрес=0x{address:02x}, диапазон={dynamic_range}В")
    
    def deinit(self):
        try:
            self.set_number(0)  # Сброс на 0 перед закрытием
            self.bus.close()
            if self.verbose:
                print("I2C шина закрыта")
        except:
            pass
    
    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return
        
        if not (0 <= number <= self.max_value):
            print(f"Число выходит за разрядность MCP4725 (12 бит, 0-{self.max_value})")
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
        
        number = int((voltage / self.dynamic_range) * self.max_value)
        self.set_number(number)
        
        if self.verbose:
            print(f"Установлено напряжение: {voltage:.3f} В")
    
    def sine_wave_generation(self, amplitude, frequency, sampling_rate):
        """
        Генерация синусоидального сигнала
        
        Args:
            amplitude: Амплитуда сигнала (В)
            frequency: Частота сигнала (Гц)
            sampling_rate: Частота дискретизации (Гц)
        """
        # Проверка параметров
        if amplitude <= 0 or amplitude > self.dynamic_range / 2:
            print(f"Предупреждение: амплитуда {amplitude}В должна быть в диапазоне (0, {self.dynamic_range/2}]В")
            amplitude = min(amplitude, self.dynamic_range / 2)
        
        if frequency <= 0:
            print("Частота должна быть положительной")
            return
        
        if sampling_rate <= 2 * frequency:
            print(f"Предупреждение: частота дискретизации {sampling_rate}Гц должна быть минимум в 2 раза выше частоты сигнала (теорема Котельникова)")
        
        # Параметры генерации
        period = 1.0 / frequency
        samples_per_period = int(sampling_rate / frequency)
        sample_period = 1.0 / sampling_rate
        offset = self.dynamic_range / 2.0  # Смещение для центрирования синусоиды
        
        if self.verbose:
            print(f"\nГенерация синусоиды:")
            print(f"  Амплитуда: {amplitude} В")
            print(f"  Частота: {frequency} Гц")
            print(f"  Частота дискретизации: {sampling_rate} Гц")
            print(f"  Период: {period:.3f} с")
            print(f"  Отсчётов на период: {samples_per_period}")
            print(f"  Смещение: {offset:.3f} В")
        
        sample_index = 0
        
        while True:
            # Вычисление фазы (0 до 2π)
            phase = 2 * math.pi * sample_index / samples_per_period
            
            # Вычисление мгновенного напряжения
            voltage = offset + amplitude * math.sin(phase)
            
            # Ограничение напряжения
            voltage = max(0, min(voltage, self.dynamic_range))
            
            # Установка напряжения на ЦАП
            self.set_voltage(voltage)
            
            # Задержка для достижения нужной частоты дискретизации
            time.sleep(sample_period)
            
            # Переход к следующему отсчёту
            sample_index += 1
            if sample_index >= samples_per_period:
                sample_index = 0


def test_sine_wave():
    """Тестовая функция для проверки генерации синусоиды"""
    try:
        # Создание объекта ЦАП
        dac = MCP4725(dynamic_range=3.3, address=0x61, verbose=True)
        
        print("\n" + "="*60)
        print("ТЕСТ ГЕНЕРАЦИИ СИНУСОИДАЛЬНОГО СИГНАЛА")
        print("="*60)
        
        # Параметры сигнала для теста
        amplitude = 1.0       # Амплитуда 1В
        frequency = 2         # Частота 2 Гц
        sampling_rate = 100   # Частота дискретизации 100 Гц
        
        print("Будет сгенерировано 3 периода синусоиды")
        print("Нажмите Ctrl+C для остановки\n")
        
        # Генерация 3 периодов
        period = 1.0 / frequency
        duration = 3 * period
        
        start_time = time.time()
        cycles_completed = 0
        
        while (time.time() - start_time) < duration:
            dac.sine_wave_generation(amplitude, frequency, sampling_rate)
            cycles_completed += 1
            
            if cycles_completed >= 3:
                break
        
        # Сброс напряжения на 0
        dac.set_voltage(0)
        print("\nТест завершён")
        
    except KeyboardInterrupt:
        print("\n\nТест прерван пользователем")
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        
    finally:
        if 'dac' in locals():
            dac.deinit()


if __name__ == "__main__":
    test_sine_wave()
