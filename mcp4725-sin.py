import mcp4725_driver
import time
import math

def generate_sine(amplitude, frequency, sample_rate, duration):
    samples = []
    num_samples = int(sample_rate * duration)
    for i in range(num_samples):
        t = i / sample_rate
        voltage = amplitude * (1 + math.sin(2 * math.pi * frequency * t)) / 2
        samples.append(voltage)
    return samples

if __name__ == "__main__":
    try:
        amplitude = float(input("Введите амплитуду сигнала (В, 0-5): "))
        frequency = float(input("Введите частоту сигнала (Гц): "))
        sample_rate = float(input("Введите частоту дискретизации (Гц): "))
        duration = 10
        
        dac = mcp4725_driver.MCP4725(5.0, 0x61, False)
        
        while True:
            samples = generate_sine(amplitude, frequency, sample_rate, duration)
            
            for voltage in samples:
                dac.set_voltage(voltage)
                time.sleep(1.0 / sample_rate)
                
    except KeyboardInterrupt:
        print("\nГенерация синусоидального сигнала остановлена")
    finally:
        dac.deinit()