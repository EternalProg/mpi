import tkinter as tk
import math

# Constants
SCALE = 10  # Масштаб для зручності відображення
GROUND_Y = 500  # Лінія "землі" на Canvas
BALL_SIZE = 10  # Розмір тіла
dt = 0.03

root = tk.Tk()

def Task1():
    clear_window(root)
    root.title("Рух тіла підкинутого під кутом")

    input_frame = tk.Frame(root, padx=20, pady=20)
    input_frame.pack(side="left", fill="y")

    tk.Label(input_frame, text="Початкова швидкість (м/с):").pack(pady=5)
    entry_v0 = tk.Entry(input_frame)
    entry_v0.pack(pady=5)

    tk.Label(input_frame, text="Кут в градусах:").pack(pady=5)
    entry_angle = tk.Entry(input_frame)
    entry_angle.pack(pady=5)

    tk.Label(input_frame, text="Прискорення вільного падіння (м/с^2):").pack(pady=5)
    entry_g = tk.Entry(input_frame)
    entry_g.pack(pady=5)

    tk.Button(input_frame, text="Очистити", command=lambda: canvas.delete("all")).pack(pady=10)

    canvas = tk.Canvas(root, width=700, height=600, bg="white")
    canvas.pack(side="right", fill="both", expand=True)
    
    result_labels = []

    def start_simulation():
        for label in result_labels:
            label.destroy()
        result_labels.clear()
        
        v0 = float(entry_v0.get())
        alpha = float(entry_angle.get())
        g = float(entry_g.get())
        
        dt = 0.02
        theta = math.radians(alpha)

        Vx = v0 * math.cos(theta)
        Vy = -v0 * math.sin(theta)  # Негативне, бо y зменшується вгору в Canvas

        x, y = 50, GROUND_Y - BALL_SIZE
        
        # t польоту, t підйому
        t_pol = 2*v0*math.sin(theta)/g
        t_pid = t_pol/2
        # Довжина + Висота
        L = v0**2 * math.sin(theta)**2 / g
        H = v0**2 * math.sin(theta)**2 / 2
        
        result_labels.append(tk.Label(input_frame, text=f"Час польоту: {t_pol:.2f} с"))
        result_labels.append(tk.Label(input_frame, text=f"Час підйому: {t_pid:.2f} с"))
        result_labels.append(tk.Label(input_frame, text=f"Довжина польоту: {L:.2f} м"))
        result_labels.append(tk.Label(input_frame, text=f"Максимальна висота: {H:.2f} м"))

        for label in result_labels:
            label.pack(pady=5)

        # Лінія старту
        canvas.create_line(x, GROUND_Y, x, GROUND_Y - 50, fill="black", width=2)
        
        ball = canvas.create_oval(x, y, x + BALL_SIZE, y + BALL_SIZE, fill="red")

        def update_motion():
            nonlocal x, y, Vx, Vy

            Vy += g * dt

            # Оновлюємо координати
            x += Vx * dt * SCALE
            y += (Vy * dt - g*(dt**2)/2) * SCALE

            print(f"Vx: {Vx:.2f}, Vy: {Vy:.2f}, x: {x:.2f}, y: {y:.2f}")

            canvas.coords(ball, x, y, x + BALL_SIZE, y + BALL_SIZE)

            # Якщо не торкнулося землі - продовжуємо рух
            if y < GROUND_Y - BALL_SIZE:
                root.after(int(dt * 1000), update_motion)  # dt у мс
            else:
                canvas.coords(ball, x, GROUND_Y - BALL_SIZE, x + BALL_SIZE, GROUND_Y)
                
                canvas.create_line(x + BALL_SIZE, GROUND_Y, x + BALL_SIZE, GROUND_Y - 50, fill="black", width=2)

        update_motion()

    tk.Button(input_frame, text="Запустити", command=start_simulation).pack()

def Task2():
    clear_window(root)
    root.title("Рух тіла підкинутого під кутом")

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


    def start_simulation():
        v0 = float(entry_v0.get())
        alpha = float(entry_angle.get())
        m = float(entry_m.get())
        k = float(entry_air_resistance.get())
        g = float(entry_g.get())

        theta = math.radians(alpha)

        t = 0
        
        Vx = v0 * math.cos(theta)
        Vy = -v0 * math.sin(theta)  # Негативне, бо y зменшується вгору в Canvas

        x, y = 50, GROUND_Y - BALL_SIZE

        # Лінія старту
        canvas.create_line(x, GROUND_Y, x, GROUND_Y - 50, fill="black", width=2)
        
        ball = canvas.create_oval(x, y, x + BALL_SIZE, y + BALL_SIZE, fill="red")

        def update_motion():
            nonlocal x, y, Vx, Vy, t

            t += dt

            # Оновлюємо швидкості
            Vx *= math.e ** ((-k/m) * t)
            Vy = m/k * (Vy + m * g / k)*(1 - math.e ** ((-k/m) * t)) - m*g*t/k

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
    
def Task3():
    clear_window(root)
    root.title("Рух тіла підкинутого під кутом")

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


    def start_simulation():
        v0 = float(entry_v0.get())
        alpha = float(entry_angle.get())
        m = float(entry_m.get())
        k = float(entry_air_resistance.get())
        g = float(entry_g.get())

        theta = math.radians(alpha)

        t = 0
        
        Vx = v0 * math.cos(theta)
        Vy = -v0 * math.sin(theta)  # Негативне, бо y зменшується вгору в Canvas

        x, y = 50, GROUND_Y - BALL_SIZE

        # Лінія старту
        canvas.create_line(x, GROUND_Y, x, GROUND_Y - 50, fill="black", width=2)
        
        ball = canvas.create_oval(x, y, x + BALL_SIZE, y + BALL_SIZE, fill="red")

        def update_motion():
            nonlocal x, y, Vx, Vy, t

            t += dt

            # Оновлюємо швидкості
            Vx *= math.e ** ((-k/m) * t)
            Vy = m/k * (Vy + m * g / k)*(1 - math.e ** ((-k/m) * t)) - m*g*t/k

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

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

def show_main_window():
    root.title("Лабораторна №1")
    
    tk.Button(root, text="Задача 1 (Рух тіла кинутого до горизонту)", command=Task1).pack()
    tk.Button(root, text="Задача 2 (Рух тіла кинутого до горизонту + gk", command=Task2).pack()
    tk.Button(root, text="Задача 3 (Попасти в ціль)", command=Task3).pack()
    
    root.geometry("1000x600")



show_main_window()

root.mainloop()
