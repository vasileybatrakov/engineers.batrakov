def plot_histogram_with_voltages():
    try:
        dynamic_range = 5.0
        adc = mcp3021_driver.MCP3021(dynamic_range, verbose=False)
        
        voltages = []
        times = []
        duration = 10.0
        
        print("Сбор данных для гистограммы...")
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            start_measure = time.time()
            voltage = adc.get_voltage()
            measure_time = time.time() - start_measure
            
            voltages.append(voltage)
            times.append(measure_time * 1000)  # в миллисекундах
            
            print(f"Время измерения: {measure_time*1000:.2f} мс")
            time.sleep(0.05)
        
        # График напряжения
        plt.figure(figsize=(14, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(range(len(voltages)), voltages, 'g-')
        plt.xlabel('Номер измерения')
        plt.ylabel('Напряжение (В)')
        plt.title('Зависимость напряжения от времени')
        plt.grid(True, alpha=0.3)
        
        # Гистограмма
        plt.subplot(1, 2, 2)
        plt.hist(times, bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Время измерения (мс)')
        plt.ylabel('Количество измерений')
        plt.title('Распределение периодов измерений')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
    except KeyboardInterrupt:
        print("\nПрервано")
    finally:
        adc.deinit()