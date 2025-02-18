from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd
import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="Observer",
    user="user",
    password=123,
    host="192.168.246.12",
    port=5432,
)

query = "SELECT created_at FROM messages"
df = pd.read_sql_query(query, conn)

# Преобразование данных в формат datetime
df["created_at"] = pd.to_datetime(df.created_at, format="%m/%d/%Y")

# Группировка данных по временным промежуткам (например, по часам)
df.set_index("created_at", inplace=True)
hourly_counts = df.groupby(pd.Grouper(freq="30min")).size()
# hourly_counts.index = hourly_counts.index.strftime("%m-%d %H:%M:%S")
hourly_counts.index = (hourly_counts.index + timedelta(hours=3)).strftime(
    "%m-%d %H:%M:%S"
)
print(hourly_counts.index)

# Построение графика
plt.style.use("dark_background")
plt.rcParams["axes.facecolor"] = "#353535"

fig = plt.figure(figsize=(12, 6))
plt.plot(hourly_counts.index, hourly_counts.values, marker="o", color="#ff99c8")
plt.title("Частота сообщений")
plt.xlabel("Время")
plt.ylabel("Кол-во сообщений")
plt.xticks(rotation=45)
plt.grid(True, color="#ABA19F")
plt.tight_layout()


# Отображение графика
plt.show()

# Закрытие соединения с базой данных
conn.close()
