import mcp3021_driver
import matplotlib.pyplot as plt
import time

def main():
    try:
        # Динамический диапазон АЦП (измерить мультиметром)
        dynamic_range = 5.0
        
        # Создание объекта
        adc = mcp3021_driver.MCP3021(dynamic_range, verbose=False)
        
        # Списки для хранения данных
        voltages = []
        times = []
        
        # Продолжительность измерений (секунды)
        duration = 10.0
        
        print(f"Измерение напряжения...")
        print(f"Продолжительность: {duration} секунд")
        print(f"Динамический диапазон: {dynamic_range} В")
        
        # Начало эксперимента
        start_time = time.time()
        
        # Сбор данных
        while (time.time() - start_time) < duration:
            voltage = adc.get_voltage()
            current_time = time.time() - start_time
            
            voltages.append(voltage)
            times.append(current_time)
            
            print(f"t={current_time:.2f}с, V={voltage:.3f}В")
            time.sleep(0.1)  # Задержка между измерениями
        
        # Построение графика
        plt.figure(figsize=(12, 6))
        plt.plot(times, voltages, 'b-', linewidth=2)
        plt.xlabel('Время (с)')
        plt.ylabel('Напряжение (В)')
        plt.title('Зависимость напряжения на входе MCP3021 от времени')
        plt.grid(True, alpha=0.3)
        plt.ylim(0, dynamic_range + 0.5)
        plt.xlim(0, duration)
        plt.show()
        
    except KeyboardInterrupt:
        print("\nИзмерение прервано пользователем")
        
    finally:
        adc.deinit()

if __name__ == "__main__":
    main()