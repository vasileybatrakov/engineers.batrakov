import matplotlib.pyplot as plt
import numpy as np

def plot_voltage_vs_time(time, voltage, max_voltage):
    """Построение графика зависимости напряжения от времени"""
    plt.figure(figsize=(12, 6))
    plt.plot(time, voltage, 'b-', linewidth=2)
    plt.xlabel('Время (с)')
    plt.ylabel('Напряжение (В)')
    plt.title('Зависимость напряжения на выходе АЦП от времени')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, max_voltage + 0.5)
    if time:
        plt.xlim(0, max(time))
    plt.show()

def plot_sampling_period_hist(time):
    """
    Построение гистограммы распределения периодов измерений
    time: список моментов времени каждого измерения
    """
    if len(time) < 2:
        print("Недостаточно данных для построения гистограммы")
        return
    
    # Вычисление периодов между измерениями
    sampling_periods = []
    for i in range(1, len(time)):
        period = time[i] - time[i-1]
        sampling_periods.append(period)
    
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Период измерения (с)')
    plt.ylabel('Количество измерений')
    plt.title('Гистограмма распределения периодов измерений')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 0.06)
    plt.show()
    
    # Статистика
    print(f"\nСтатистика периодов измерений:")
    print(f"Средний период: {np.mean(sampling_periods)*1000:.2f} мс")
    print(f"Медианный период: {np.median(sampling_periods)*1000:.2f} мс")
    print(f"Максимальный период: {np.max(sampling_periods)*1000:.2f} мс")
    print(f"Минимальный период: {np.min(sampling_periods)*1000:.2f} мс")
    print(f"Стандартное отклонение: {np.std(sampling_periods)*1000:.2f} мс")