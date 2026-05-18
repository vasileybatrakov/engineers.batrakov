import mcp4725_ddriver
import signal_generator
import time
amplitude = 3.3      
frequency = 50
sampling_rate = 1000 
dynamic_range = 3.3  

try:
    dac = mcp4725_ddriver.MCP4725(dynamic_range, verbose=False)
    
    print("Генерация синусоидального сигнала...")
    print(f"Амплитуда: {amplitude} В")
    print(f"Частота: {frequency} Гц")
    print(f"Частота дискретизации: {sampling_rate} Гц")
    print("Для остановки нажмите Ctrl+C")
    
    while True:
        dac.sine_wave_generation(amplitude, frequency, sampling_rate)
        
except KeyboardInterrupt:
    print("\nГенерация остановлена пользователем")
    
finally:
    dac.deinit()
    print("Ресурсы освобождены")