from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def data_file():
    names = ["TRAIN2.xlsx", "train.xlsx"]
    places = [Path(__file__).with_name(name) for name in names]
    places += [Path.home() / "Downloads" / name for name in names]
    for place in places:
        if place.exists():
            return place
    raise FileNotFoundError("Không tìm thấy file Excel trong thư mục code hoặc Downloads.")


def read_scores():
    try:
        df = pd.read_excel(data_file())
    except ImportError as exc:
        raise RuntimeError("Thiếu openpyxl. Cài bằng lệnh: python -m pip install openpyxl") from exc

    df.columns = df.columns.astype(str).str.strip().str.lower()
    if not {"midterm", "final"}.issubset(df.columns):
        raise ValueError("File Excel phải có 2 cột: midterm và final.")

    scores = df[["midterm", "final"]].apply(pd.to_numeric, errors="coerce").dropna()
    scores = scores[scores["midterm"].between(0, 10) & scores["final"].between(0, 10)]
    if len(scores) < 2:
        raise ValueError("Dữ liệu hợp lệ quá ít để train mô hình.")
    return scores


def train_model(scores):
    x = scores["midterm"].to_numpy(float)
    y = scores["final"].to_numpy(float)
    a, b = np.polyfit(x, y, 1)
    y_hat = a * x + b
    mae = np.mean(np.abs(y - y_hat))
    r2 = 1 - np.sum((y - y_hat) ** 2) / np.sum((y - y.mean()) ** 2)
    return x, y, a, b, mae, r2


def start_app():
    scores = read_scores()
    x, y, a, b, mae, r2 = train_model(scores)

    def estimate(midterm):
        return float(np.clip(a * midterm + b, 0, 10))

    def formula():
        mark = "+" if b >= 0 else "-"
        return f"final = {a:.4f} * midterm {mark} {abs(b):.4f}"

    def draw(point=None):
        ax.clear()
        line_x = np.linspace(0, 10, 200)
        line_y = a * line_x + b

        ax.scatter(x, y, s=34, alpha=0.65, color="#1976d2", label="Dữ liệu thực tế")
        ax.plot(line_x, line_y, color="#d32f2f", linewidth=2.2, label="Đường dự báo")

        if point:
            px, py = point
            ax.scatter([px], [py], s=120, marker="X", color="#2e7d32", label="Điểm vừa nhập")
            ax.annotate(f"{py:.2f}", xy=(px, py), xytext=(8, 8), textcoords="offset points")

        ax.set_title("Dự báo điểm cuối kỳ từ điểm giữa kỳ")
        ax.set_xlabel("Điểm giữa kỳ")
        ax.set_ylabel("Điểm cuối kỳ")
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.grid(True, linestyle="--", alpha=0.35)
        ax.legend()
        chart.draw_idle()

    def predict():
        try:
            midterm = float(entry.get().strip().replace(",", "."))
        except ValueError:
            messagebox.showerror("Lỗi", "Hãy nhập điểm bằng số.")
            return

        if not 0 <= midterm <= 10:
            messagebox.showwarning("Cảnh báo", "Điểm phải từ 0 đến 10.")
            return

        final = estimate(midterm)
        result.set(f"Điểm cuối kỳ dự đoán: {final:.2f}")
        draw((midterm, final))

    root = tk.Tk()
    root.title("Dự đoán điểm cuối kỳ")
    root.geometry("1050x600")

    ttk.Style().theme_use("clam")
    left = ttk.Frame(root, padding=18)
    left.pack(side=tk.LEFT, fill=tk.Y)
    right = ttk.Frame(root, padding=(0, 18, 18, 18))
    right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    ttk.Label(left, text="Mô hình hồi quy", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 14))
    ttk.Label(
        left,
        text=f"{formula()}\n\nSố mẫu: {len(scores)}\nMAE: {mae:.3f}\nR2: {r2:.3f}",
        font=("Segoe UI", 11),
        justify=tk.LEFT,
    ).pack(anchor="w", pady=(0, 22))

    ttk.Label(left, text="Nhập điểm giữa kỳ:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
    entry = ttk.Entry(left, width=18, font=("Segoe UI", 12))
    entry.pack(anchor="w", pady=8)

    ttk.Button(left, text="Dự đoán", command=predict).pack(anchor="w", pady=(0, 16))
    result = tk.StringVar(value="Điểm cuối kỳ dự đoán: --")
    ttk.Label(left, textvariable=result, font=("Segoe UI", 14, "bold"), foreground="#c62828").pack(anchor="w")

    fig = Figure(figsize=(7, 4.8), dpi=100)
    ax = fig.add_subplot(111)
    chart = FigureCanvasTkAgg(fig, master=right)
    chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    draw()
    root.mainloop()


if __name__ == "__main__":
    try:
        start_app()
    except Exception as error:
        messagebox.showerror("Lỗi chương trình", str(error))
