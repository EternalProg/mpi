import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import math

# Константи
SCALE = 20  # Масштаб для Canvas
BALL_SIZE = 10  # Розмір об'єкта
dt = 0.01  # Крок часу
t_max = 10  # Максимальний час моделювання
TRAIL_OPACITY = 0.7 # Прозорість сліду від кульки
offset = 50 # Відступи від осей

# Створюємо головне вікно
root = tk.Tk()
root.title("Прямолінійний рух")

# Фрейм для введення даних
input_frame = tk.Frame(root, padx=20, pady=20)
input_frame.pack(side="left", fill="y")

# Поля введення
tk.Label(input_frame, text="X0 (м):").grid(row=0, column=0)
entry_x0 = tk.Entry(input_frame)
entry_x0.grid(row=0, column=1)

tk.Label(input_frame, text="Y0 (м):").grid(row=1, column=0)
entry_y0 = tk.Entry(input_frame)
entry_y0.grid(row=1, column=1)

tk.Label(input_frame, text="Кут (градуси):").grid(row=2, column=0)
entry_angle = tk.Entry(input_frame)
entry_angle.grid(row=2, column=1)

tk.Label(input_frame, text="Початкова швидкість (м/с):").grid(row=3, column=0)
entry_v0 = tk.Entry(input_frame)
entry_v0.grid(row=3, column=1)

tk.Label(input_frame, text="Прискорення (м/с²):").grid(row=4, column=0)
entry_a = tk.Entry(input_frame)
entry_a.grid(row=4, column=1)

# Кнопка очищення Canvas
canvas = tk.Canvas(root, width=700, height=400, bg="white")
canvas.pack(side="right", fill="both", expand=True)

def draw_axes():
    canvas.create_line(offset, canvas.winfo_height() - offset, canvas.winfo_width() - offset, canvas.winfo_height() - offset, fill="black")
    canvas.create_line(offset, 0, offset, canvas.winfo_height(), fill="black")

def start_simulation():
    draw_axes()
    x0 = float(entry_x0.get())
    y0 = float(entry_y0.get())
    v0 = float(entry_v0.get())
    alpha = float(entry_angle.get())
    a = float(entry_a.get())

    theta = math.radians(alpha)
    dirX = np.cos(theta)
    dirY = np.sin(theta)

    root.update_idletasks()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    x = x0
    y = y0

    canvas_x = x * SCALE + offset
    canvas_y = canvas_height - (y * SCALE + offset)

    ball = canvas.create_oval(canvas_x, canvas_y, canvas_x + BALL_SIZE, canvas_y + BALL_SIZE, fill="red")

    t = 0

    trail = []

    def update_motion():
        nonlocal x, y, t

        t += dt

        S = v0 * t + 0.5 * a * t ** 2

        x = x0 + dirX * S
        y = y0 + dirY * S

        canvas_x = x * SCALE + offset
        canvas_y = canvas_height - (y * SCALE + offset)

        canvas.coords(ball, canvas_x, canvas_y, canvas_x + BALL_SIZE, canvas_y + BALL_SIZE)

        # Додаємо нову точку в слід
        trail.append((canvas_x, canvas_y))

        for i, (trail_x, trail_y) in enumerate(trail):
            opacity = 1 - (i / len(trail)) * TRAIL_OPACITY
            hex_opacity = int(opacity * 255)
            color = f"#{hex_opacity:02x}{hex_opacity:02x}{hex_opacity:02x}"

            canvas.create_oval(
                trail_x - BALL_SIZE, trail_y - BALL_SIZE, trail_x + BALL_SIZE / 2, trail_y + BALL_SIZE / 2,
                outline="", fill=color, tags="trail"
        )

        if t <= t_max and 0 <= canvas_x <= canvas_width - BALL_SIZE and 0 <= canvas_y <= canvas_height - BALL_SIZE:
            root.after(int(dt * 1000), update_motion)
    update_motion()


graphs = []

def plot_trajectory():
    x0 = float(entry_x0.get())
    y0 = float(entry_y0.get())
    v = float(entry_v0.get())
    alpha = float(entry_angle.get())
    a = float(entry_a.get())

    theta = math.radians(alpha)

    t = np.arange(0, t_max, dt)

    dirX = np.cos(theta)
    dirY = np.sin(theta)

    S = v * t + 0.5 * a * t ** 2

    x = x0 + dirX * S
    y = y0 + dirY * S

    # Додаємо новий графік до списку
    graphs.append((x, y))

    # Оновлюємо графік, додаючи всі траєкторії
    plt.figure(figsize=(8, 5))
    
    colors = ["blue", "green", "red", "purple", "orange"]
    for i, (x_vals, y_vals) in enumerate(graphs):
        plt.plot(x_vals, y_vals, label=f"Графік {i+1}", color=colors[i % len(colors)])

    plt.xlabel("X (м)")
    plt.ylabel("Y (м)")
    plt.title("Графік прямолінійного руху")
    plt.legend()
    plt.grid()
    plt.show()

def clean_window():
    canvas.delete("all")
    graphs.clear()

# Кнопки для запуску симуляції та отримання графіка
tk.Button(input_frame, text="Очистити", command=clean_window).grid(row=5, column=0)
tk.Button(input_frame, text="Запустити симуляцію", command=start_simulation).grid(row=6, column=0)
tk.Button(input_frame, text="Отримати графік", command=plot_trajectory).grid(row=7, column=0)

root.mainloop()

