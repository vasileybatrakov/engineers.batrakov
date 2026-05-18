import r2r_adc
import matplotlib.pyplot as plt
import time

def main():
    try:
        dynamic_range = 5.0
        adc = r2r_adc.R2R_ADC(dynamic_range, compare_time=0.0001, verbose=False)
        
        voltages = []
        times = []
        duration = 3.0  # Продолжительность в секундах
        
        print("Измерение напряжения SAR ADC...")
        print(f"Динамический диапазон: {dynamic_range} В")
        print(f"Продолжительность: {duration} с\n")
        
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            voltage = adc.get_sar_voltage()
            current_time = time.time() - start_time
            
            voltages.append(voltage)
            times.append(current_time)
            
            print(f"t={current_time:.3f}с, V={voltage:.3f}В")
        
        # Построение графика
        plt.figure(figsize=(12, 6))
        plt.plot(times, voltages, 'r-', linewidth=2)
        plt.xlabel('Время (с)')
        plt.ylabel('Напряжение (В)')
        plt.title('Зависимость напряжения от времени (SAR ADC)')
        plt.grid(True, alpha=0.3)
        plt.ylim(0, dynamic_range + 0.5)
        plt.xlim(0, duration)
        plt.show()
        
    except KeyboardInterrupt:
        print("\nПрервано")
        
    finally:
        adc.deinit()

if __name__ == "__main__":
    main()