import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import math

# Константи
SCALE = 20  # Масштаб для Canvas
BALL_SIZE = 10  # Розмір об'єкта
dt = 0.01  # Крок часу
t_max = 10  # Максимальний час моделювання
TRAIL_OPACITY = 0.7  # Прозорість сліду від кульки
offset = 50  # Відступи від країв екрану

# Створюємо головне вікно
root = tk.Tk()
root.title("Рух тіла кинутого під кутом до горизонту")

input_frame = tk.Frame(root, padx=20, pady=20)
input_frame.pack(side="left", fill="y")

# Поля введення
tk.Label(input_frame, text="X0 (м):").grid(row=0, column=0, padx=10, pady=10)
entry_x0 = tk.Entry(input_frame)
entry_x0.grid(row=0, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Y0 (м):").grid(row=1, column=0, padx=10, pady=10)
entry_y0 = tk.Entry(input_frame)
entry_y0.grid(row=1, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Кут (градуси):").grid(row=2, column=0, padx=10, pady=10)
entry_angle = tk.Entry(input_frame)
entry_angle.grid(row=2, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Початкова швидкість (м/с):").grid(
    row=3, column=0, padx=10, pady=10
)
entry_v0 = tk.Entry(input_frame)
entry_v0.grid(row=3, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Сила тяжіння:").grid(row=4, column=0, padx=10, pady=10)
entry_g = tk.Entry(input_frame)
entry_g.grid(row=4, column=1, padx=10, pady=10)

# Полотно для відображення руху
canvas = tk.Canvas(root, width=700, height=400, bg="white")
canvas.pack(side="right", fill="both", expand=True)


def draw_axes():
    canvas.create_line(
        offset,
        canvas.winfo_height() - offset,
        canvas.winfo_width() - offset,
        canvas.winfo_height() - offset,
        fill="black",
    )
    canvas.create_line(offset, 0, offset, canvas.winfo_height(), fill="black")


def start_simulation():
    draw_axes()
    x0 = float(entry_x0.get())
    y0 = float(entry_y0.get())
    v0 = float(entry_v0.get())
    alpha = float(entry_angle.get())
    g = float(entry_g.get())

    theta = math.radians(alpha)

    root.update_idletasks()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    x = x0
    y = y0

    canvas_x = x * SCALE + offset
    canvas_y = canvas_height - (y * SCALE + offset)

    ball = canvas.create_oval(
        canvas_x, canvas_y, canvas_x + BALL_SIZE, canvas_y + BALL_SIZE, fill="red"
    )

    t_pol = 2 * v0 * math.sin(theta) / g
    t_pid = t_pol / 2

    L = v0**2 * math.sin(2 * theta) / g
    H = (v0**2) * (math.sin(theta) ** 2) / (2 * g)

    print_exact_result(t_pol, t_pid, L, H)

    t = 0

    trail = []

    def update_motion():
        nonlocal x, y, t

        t += dt

        v0x = v0 * math.cos(theta)
        v0y = v0 * math.sin(theta)

        x = x0 + v0x * t
        y = y0 + v0y * t - 0.5 * g * t**2

        canvas_x = x * SCALE + offset
        canvas_y = canvas_height - (y * SCALE + offset)

        canvas.coords(
            ball, canvas_x, canvas_y, canvas_x + BALL_SIZE, canvas_y + BALL_SIZE
        )

        # Додаємо нову точку в слід
        trail.append((canvas_x, canvas_y))

        for i, (trail_x, trail_y) in enumerate(trail):
            hex_opacity = int(TRAIL_OPACITY * 255)
            color = f"#{hex_opacity:02x}{hex_opacity:02x}{hex_opacity:02x}"

            canvas.create_oval(
                trail_x,
                trail_y,
                trail_x + BALL_SIZE / 2,
                trail_y + BALL_SIZE / 2,
                outline="",
                fill=color,
                tags="trail",
            )

        if y > 0 and t <= t_max:
            root.after(int(dt * 1000), update_motion)

    update_motion()


result_labels = {}


def print_exact_result(t_pol, t_pid, L, H):
    global result_labels

    results = {
        "Час польоту": t_pol,
        "Час підйому": t_pid,
        "Дальність польоту": L,
        "Висота підйому": H,
    }

    row = 9

    for key, value in results.items():
        if key in result_labels:
            # Якщо Label вже існує, оновлюємо його текст
            result_labels[key].config(text=f"{key}: {value:.2f}")
        else:
            # Якщо Label ще немає, створюємо його
            label = tk.Label(input_frame, text=f"{key}: {value:.2f}")
            label.grid(row=row, column=0, columnspan=2, padx=10, pady=5)
            result_labels[key] = label
        row += 1


graphs = []
last_params = []


def render_trajectory():
    plt.figure(figsize=(8, 5))

    colors = ["blue", "green", "red", "purple", "orange"]
    for i, (x_vals, y_vals) in enumerate(graphs):
        plt.plot(x_vals, y_vals, label=f"Графік {i+1}", color=colors[i % len(colors)])

    plt.xlabel("X (м)")
    plt.ylabel("Y (м)")
    plt.title("Графік руху тіла кинутого під кутом до горизонту")
    plt.legend()
    plt.grid()
    plt.show()


def plot_trajectory():
    global last_params
    x0 = float(entry_x0.get())
    y0 = float(entry_y0.get())
    v0 = float(entry_v0.get())
    alpha = float(entry_angle.get())
    g = float(entry_g.get())

    if last_params == [x0, y0, v0, alpha, g]:
        render_trajectory()
        return

    last_params = [x0, y0, v0, alpha, g]

    theta = math.radians(alpha)

    t = np.arange(0, t_max, dt)

    v0x = v0 * math.cos(theta)
    v0y = v0 * math.sin(theta)

    x = x0 + v0x * t
    y = y0 + v0y * t - 0.5 * g * t**2

    # Видаляємо точки, де y < 0
    valid_indices = y >= 0
    x = x[valid_indices]
    y = y[valid_indices]

    graphs.append((x, y))

    render_trajectory()


def clean_window():
    canvas.delete("all")
    graphs.clear()


# Кнопки для запуску симуляції та отримання графіка
tk.Button(input_frame, text="Очистити", command=clean_window).grid(
    row=5, column=0, columnspan=2, pady=10
)
tk.Button(input_frame, text="Запустити симуляцію", command=start_simulation).grid(
    row=6, column=0, columnspan=2, pady=10
)
tk.Button(input_frame, text="Отримати графік", command=plot_trajectory).grid(
    row=7, column=0, columnspan=2, pady=10
)

root.mainloop()
