import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Параметры генерации
np.random.seed(42)
# DAYS_BACK = 30  # Глубина исторических данных
# COURIERS_TOTAL = 200  # Общее количество курьеров
ORDERS_PER_DAY_MEAN = 6  # Среднее число доставок на курьера в день
CITIES = ['Москва', 'Липецк', 'Омск']
CITY_PROBS = [0.6, 0.2, 0.2]  # Доли курьеров по городам

# Параметры времени доставки (в минутах) для каждого города: (среднее, стандартное отклонение)
CITY_PARAMS = {
    'Москва': (45, 15),
    'Липецк': (25, 8),
    'Омск': (30, 10)
}

def generate_couriers(n, cities=CITIES, probs=CITY_PROBS):
    """Генерация списка курьеров с их характеристиками"""
    couriers = []
    city_choices = np.random.choice(cities, size=n, p=probs)
    
    for i in range(n):
        city = city_choices[i]
        # Индивидуальный множитель скорости курьера
        speed_factor = np.random.uniform(0.8, 1.2) 
        couriers.append({
            'courier_id': f'c_{i:04d}',
            'city': city,
            'speed_factor': speed_factor,
            # Вероятность работать в день: 90-100%
            'work_prob': np.random.uniform(0.9, 1.0)
        })
    return pd.DataFrame(couriers)

def generate_orders(couriers_df, days_back):
    """Генерация исторических данных о доставках"""
    orders = []
    order_counter = 0
    base_date = datetime.now() - timedelta(days=days_back)
    
    for day in range(days_back):
        date = base_date + timedelta(days=day)
        
        for _, courier in couriers_df.iterrows():
            # Пропускаем курьера с вероятностью 1 - work_prob
            if np.random.random() > courier['work_prob']:
                continue
                
            # Генерация количества заказов в день (пуассоновское распределение)
            n_orders = np.random.poisson(ORDERS_PER_DAY_MEAN)
            
            for _ in range(n_orders):
                # Базовое время доставки для города
                base_time, std = CITY_PARAMS[courier['city']]
                
                # Реальное время доставки с учетом:
                # - индивидуального множителя скорости курьера
                # - случайных колебаний
                delivery_time = np.random.normal(
                    loc=base_time * courier['speed_factor'],
                    scale=std * (1 + 0.2 * np.random.random())  # Добавляем вариативность дисперсии
                )
                
                # Ограничим минимальное время доставки 10 минутами
                delivery_time = max(10, delivery_time)
                
                # Генерация временных меток
                start_time = date + timedelta(
                    hours=np.random.randint(8, 20),  # Рабочий день с 8 до 20
                    minutes=np.random.randint(0, 60)
                )
                
                end_time = start_time + timedelta(minutes=int(delivery_time))
                
                orders.append({
                    'order_id': f'ord_{order_counter:06d}',
                    'courier_id': courier['courier_id'],
                    'city': courier['city'],
                    'start_time': start_time,
                    'end_time': end_time,
                    'delivery_time': delivery_time
                })
                order_counter += 1
                
    return pd.DataFrame(orders)
