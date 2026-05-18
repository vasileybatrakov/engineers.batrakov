import mcp4725_driver
import time
import math

def main():
    """
    Основная функция для генерации синусоидального сигнала
    """
    # Параметры сигнала (можно изменять)
    dynamic_range = 3.3    # Динамический диапазон ЦАП (В)
    amplitude = 1.5        # Амплитуда сигнала (В)
    frequency = 50         # Частота сигнала (Гц)
    sampling_rate = 1000   # Частота дискретизации (Гц)
    address = 0x61        # I2C адрес MCP4725
    
    dac = None
    
    try:
        # Создание объекта для управления MCP4725
        dac = mcp4725_driver.MCP4725(dynamic_range, address, verbose=False)
        
        print("\n" + "="*60)
        print("ГЕНЕРАЦИЯ СИНУСОИДАЛЬНОГО СИГНАЛА НА MCP4725")
        print("="*60)
        print(f"Динамический диапазон: {dynamic_range} В")
        print(f"Амплитуда сигнала: {amplitude} В")
        print(f"Частота сигнала: {frequency} Гц")
        print(f"Частота дискретизации: {sampling_rate} Гц")
        print(f"I2C адрес: 0x{address:02X}")
        print("-"*60)
        print("Для остановки нажмите Ctrl+C")
        print("="*60)
        print()
        
        # Бесконечная генерация синусоидального сигнала
        while True:
            dac.sine_wave_generation(amplitude, frequency, sampling_rate)
            
    except KeyboardInterrupt:
        print("\n\nГенерация остановлена пользователем")
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        
    finally:
        if dac:
            dac.deinit()
            print("Ресурсы освобождены")

def sine_wave_with_duration(duration=10):
    """
    Генерация синусоиды в течение заданного времени
    
    Args:
        duration: Длительность генерации в секундах
    """
    dynamic_range = 3.3
    amplitude = 1.5
    frequency = 50
    sampling_rate = 1000
    address = 0x61
    
    dac = None
    
    try:
        dac = mcp4725_ddriver.MCP4725(dynamic_range, address, verbose=False)
        
        print(f"\nГенерация синусоиды в течение {duration} секунд...")
        print(f"Частота: {frequency} Гц, Амплитуда: {amplitude} В")
        
        start_time = time.time()
        periods_generated = 0
        
        while (time.time() - start_time) < duration:
            dac.sine_wave_generation(amplitude, frequency, sampling_rate)
            periods_generated += 1
            
            # Показываем прогресс каждую секунду
            elapsed = time.time() - start_time
            if int(elapsed) > int(elapsed - 1/sampling_rate):
                print(f"\rПрогресс: {elapsed:.1f}/{duration} сек, периодов: {periods_generated}", end='', flush=True)
        
        print(f"\n\nГенерация завершена! Сгенерировано {periods_generated} периодов")
        dac.set_voltage(0)
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        
    finally:
        if dac:
            dac.deinit()

def test_different_frequencies():
    """
    Тест генерации синусоид с разными частотами
    """
    frequencies = [1, 5, 10, 20, 50, 100]
    duration_per_freq = 3  # секунд на каждую частоту
    
    dac = None
    
    try:
        dac = mcp4725_ddriver.MCP4725(3.3, 0x61, verbose=False)
        
        print("\n" + "="*60)
        print("ТЕСТ РАЗЛИЧНЫХ ЧАСТОТ")
        print("="*60)
        
        for freq in frequencies:
            print(f"\nГенерация {freq} Гц в течение {duration_per_freq} секунд...")
            
            start_time = time.time()
            while (time.time() - start_time) < duration_per_freq:
                dac.sine_wave_generation(1.0, freq, freq * 20)
            
            print(f"Частота {freq} Гц - завершено")
            time.sleep(0.5)
        
        dac.set_voltage(0)
        print("\nТест завершён!")
        
    except KeyboardInterrupt:
        print("\nТест прерван")
        
    finally:
        if dac:
            dac.deinit()

if __name__ == "__main__":
    # Выберите режим работы:
    
    # Режим 1: Бесконечная генерация
    main()
    
    # Режим 2: Генерация в течение заданного времени
    # sine_wave_with_duration(duration=10)
    
    # Режим 3: Тест различных частот
    # test_different_frequencies()
