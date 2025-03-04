import tkinter as tk
import math

root = tk.Tk()

root.title("Рух тіла підкинутого під кутом")
root.geometry("1000x600")

input_frame = tk.Frame(root, padx=20, pady=20)
input_frame.pack(side="left")

tk.Label(input_frame, text="Початкова швидкість (м/с):").pack()
entry_v0 = tk.Entry(input_frame)
entry_v0.pack()

tk.Label(input_frame, text="Кут в градусах:").pack()
entry_angle = tk.Entry(input_frame)
entry_angle.pack()

tk.Label(input_frame, text="Маса тіла (кг):").pack()
entry_m = tk.Entry(input_frame)
entry_m.pack()

tk.Label(input_frame, text="Опір повітря (кг/с):").pack()
entry_air_resistance = tk.Entry(input_frame)
entry_air_resistance.pack()

tk.Label(input_frame, text="Прискорення вільного падіння (м/с^2):").pack()
entry_g = tk.Entry(input_frame)
entry_g.pack()

canvas = tk.Canvas(root, width=700, height=600, bg="white")
canvas.pack(side="right", fill="both", expand=True)

SCALE = 20  # Масштаб для зручності відображення
GROUND_Y = 500  # Лінія "землі" на Canvas
BALL_SIZE = 10  # Розмір тіла

def start_simulation():
    v0 = float(entry_v0.get())
    alpha = float(entry_angle.get())
    m = float(entry_m.get())
    k = float(entry_air_resistance.get())
    g = float(entry_g.get())

    dt = 0.03  # 20 мс -> 0.02 секунд
    theta = math.radians(alpha)

    Vx = v0 * math.cos(theta)
    Vy = -v0 * math.sin(theta)  # Негативне, бо y зменшується вгору в Canvas

    x, y = 50, GROUND_Y - BALL_SIZE

    # Лінія старту
    canvas.create_line(x, GROUND_Y, x, GROUND_Y - 50, fill="black", width=2)
    
    ball = canvas.create_oval(x, y, x + BALL_SIZE, y + BALL_SIZE, fill="red")

    def update_motion():
        nonlocal x, y, Vx, Vy

        # Прискорення з урахуванням опору повітря
        ax = -k * (Vx / m)
        ay = g - (k * Vy / m)  # g позитивне, бо в Canvas вниз = зростання y

        # Оновлюємо швидкості
        Vx += ax * dt
        Vy += ay * dt

        # Оновлюємо координати
        x += Vx * dt * SCALE
        y += Vy * dt * SCALE

        print(f"Vx: {Vx:.2f}, Vy: {Vy:.2f}, x: {x:.2f}, y: {y:.2f}")

        canvas.coords(ball, x, y, x + BALL_SIZE, y + BALL_SIZE)

        # Якщо не торкнулося землі - продовжуємо рух
        if y < GROUND_Y - BALL_SIZE:
            root.after(int(dt * 1000), update_motion)  # dt у мс
        else:
            canvas.coords(ball, x, GROUND_Y - BALL_SIZE, x + BALL_SIZE, GROUND_Y)
            
            canvas.create_line(x + BALL_SIZE, GROUND_Y, x + BALL_SIZE, GROUND_Y - 50, fill="black", width=2)
            canvas.create_text(x, GROUND_Y + 10, text=f"Відстань: {x-50:.2f} м", fill="black", font=('Arial', 10))

    update_motion()

tk.Button(input_frame, text="Запустити", command=start_simulation).pack()

root.mainloop()
