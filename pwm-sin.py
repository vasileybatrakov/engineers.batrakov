import pwm_dac
import signal_generator as sg
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

amplitude = 3.2          
signal_frequency = 10
sampling_frequency = 1000 

gpio_pin = 12
pwm_frequency = 5000
dynamic_range = 3.3

try:
    dac = pwm_dac.PWM_DAC(gpio_pin, pwm_frequency, dynamic_range)
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