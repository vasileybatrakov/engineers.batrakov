import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2          
signal_frequency = 10
sampling_frequency = 1000 

try:
    dac = r2r.R2R_DAC()
    
    start_time = time.time()
    
    while True:
        current_time = time.time() - start_time
        normalized_amplitude = sg.get_sin_wave_amplitude(signal_frequency, current_time)
        output_voltage = normalized_amplitude * amplitude
        dac.set_voltage(output_voltage)
        sg.wait_for_sampling_period(sampling_frequency)
        
except KeyboardInterrupt:
    print("\nГенерация остановлена пользователем")
finally:
    if 'dac' in locals():
        dac.cleanup()
    print("Ресурсы освобождены")