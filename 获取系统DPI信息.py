# Python获取DPI信息的示例
import ctypes
import tkinter as tk


def get_dpi_info():
    # Windows API获取DPI
    user32 = ctypes.windll.user32
    hdc = user32.GetDC(0)
    dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
    dpi_y = ctypes.windll.gdi32.GetDeviceCaps(hdc, 90)  # LOGPIXELSY
    user32.ReleaseDC(0, hdc)

    print(f"系统DPI: {dpi_x} x {dpi_y}")
    print(f"缩放比例: {dpi_x / 96:.1%}")

    # Tkinter方法
    root = tk.Tk()
    dpi = root.winfo_fpixels('1i')  # 每英寸像素数
    print(f"Tkinter DPI: {dpi}")
    root.destroy()


if __name__ == "__main__":
    get_dpi_info()
