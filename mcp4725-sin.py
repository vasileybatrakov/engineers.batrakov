import time
import math
import smbus

# Простая настройка
DYNAMIC_RANGE = 5.0
ADDRESS = 0x61
FREQUENCY = 0.5  # Очень низкая частота для теста
SAMPLING_RATE = 50

def main():
    try:
        bus = smbus.SMBus(1)
        print("I2C инициализирован")
        
        period_samples = int(SAMPLING_RATE / FREQUENCY)
        delay = 1.0 / SAMPLING_RATE
        
        print("Начинаем генерацию...")
        while True:
            for i in range(period_samples):
                t = i / SAMPLING_RATE
                voltage = 2.5 + 2.0 * math.sin(2 * math.pi * FREQUENCY * t)
                value = int((voltage / DYNAMIC_RANGE) * 4095)
                value = max(0, min(4095, value))
                
                first_byte = (value >> 8) & 0x0F
                second_byte = value & 0xFF
                
                bus.write_i2c_block_data(ADDRESS, first_byte, [second_byte])
                time.sleep(delay)
                
    except KeyboardInterrupt:
        print("Стоп")
    finally:
        bus.close()

if __name__ == "__main__":
    main()
