import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols

def perform_eda(df):
    # 1. Базовая статистика по городам
    city_stats = df.groupby('city')['delivery_time'].agg(['mean', 'std', 'count', 'min', 'max'])
    print("📊 Описательная статистика по городам:")
    print(city_stats)
    
    # 2. Визуализация распределений
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='city', y='delivery_time', hue='city', data=df, palette='viridis', legend=False)
    plt.title('Распределение времени доставки по городам')
    plt.ylabel('Минуты')
    plt.grid(True)
    plt.show()
    
    # 3. Расчет доли объясняемой дисперсии
    model = ols('delivery_time ~ C(city)', data=df).fit()
    r_squared = model.rsquared
    print(f"\n📌 Доля дисперсии, объясняемая городом (R²): {r_squared:.2%}")
