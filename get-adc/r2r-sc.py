import r2r_adc
import adc_plot
import time

def main():
    try:
        dynamic_range = 5.0
        adc = r2r_adc.R2R_ADC(dynamic_range, compare_time=0.0001, verbose=False)
        
        voltages = []
        times = []
        duration = 3.0
        
        print("Измерение напряжения SC ADC...")
        print(f"Динамический диапазон: {dynamic_range} В")
        print(f"Продолжительность: {duration} с\n")
        
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            voltage = adc.get_sc_voltage()
            current_time = time.time() - start_time
            
            voltages.append(voltage)
            times.append(current_time)
            
            print(f"t={current_time:.3f}с, V={voltage:.3f}В")
        
        # Построение графика
        adc_plot.plot_voltage_vs_time(times, voltages, dynamic_range)
        
        # Построение гистограммы периодов
        adc_plot.plot_sampling_period_hist(times)
        
    except KeyboardInterrupt:
        print("\nПрервано")
        
    finally:
        adc.deinit()

if __name__ == "__main__":
    main()