import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageEnhance
import shutil
from textToImage_Model import create_pipeline, text2img

class TextToImageApp:
    def __init__(self, master):
        self.master = master
        master.title("Text to Image App")

        self.label = tk.Label(master, text="Nhập văn bản để tạo ảnh:", font=("Arial", 14))
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.text_entry = tk.Text(master, font=("Arial", 12), wrap=tk.WORD, height=4, width=50)
        self.text_entry.grid(row=1, column=0, padx=10, pady=10)

        self.generate_button = tk.Button(master, text="Tạo ảnh", command=self.generate_image, font=("Arial", 12))
        self.generate_button.grid(row=2, column=0, padx=10, pady=10)

        self.image_label = tk.Label(master)
        self.image_label.grid(row=3, column=0, padx=10, pady=10)

        self.save_button = tk.Button(master, text="Lưu ảnh", command=self.save_image, state=tk.DISABLED, font=("Arial", 12))
        self.save_button.grid(row=4, column=0, padx=10, pady=10)

        self.adjust_brightness_button = tk.Button(master, text="", command=self.adjust_brightness_popup, font=("Arial", 12))
        self.adjust_brightness_button.grid(row=3, column=1, padx=10, pady=10)

        # Thêm icon mặt trời vào nút điều chỉnh độ sáng
        self.sun_icon = tk.PhotoImage(file="./icons/sun_icon.png")
        self.adjust_brightness_button.config(image=self.sun_icon, compound=tk.LEFT)

        self.image_path = None

    def generate_image(self):
        user_input = self.text_entry.get("1.0", tk.END).strip()

        # Khởi tạo pipeline
        pipeline = create_pipeline()

        try:
            # Sinh ảnh từ văn bản
            im = text2img(user_input, pipeline)

            # Lưu ảnh tạm thời
            self.save_temp_image(im)

            # Hiển thị ảnh trong giao diện
            self.display_image(im)

            # Kích hoạt nút lưu ảnh
            self.save_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi trong quá trình tạo ảnh:\n{}".format(str(e)))

    def display_image(self, image):
        # Chuyển đổi ảnh sang định dạng ImageTk
        self.image_tk = ImageTk.PhotoImage(image)

        # Hiển thị ảnh trong giao diện
        self.image_label.configure(image=self.image_tk)

    def save_temp_image(self, image):
        # Tạo tên tệp tạm thời
        temp_image_path = "./product_images/product_temp_image.jpg"

        # Lưu ảnh vào tệp tạm thời
        image.save(temp_image_path)

        # Lưu đường dẫn của ảnh tạm thời
        self.image_path = temp_image_path

    def save_image(self):
        if self.image_path:
            try:
                # Chọn nơi lưu ảnh
                file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
                if file_path:
                    # Sao chép ảnh từ tệp tạm thời vào nơi lưu được chọn
                    shutil.copyfile(self.image_path, file_path)
                    messagebox.showinfo("Thông báo", "Đã lưu ảnh thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", "Đã xảy ra lỗi trong quá trình lưu ảnh:\n{}".format(str(e)))
        else:
            messagebox.showerror("Lỗi", "Không có ảnh để lưu!")

    def adjust_brightness_popup(self):
        # Tạo cửa sổ pop-up để người dùng điều chỉnh độ sáng
        brightness_popup = tk.Toplevel()
        brightness_popup.title("Điều chỉnh độ sáng")

        # Tạo thanh trượt để điều chỉnh độ sáng
        brightness_scale = tk.Scale(brightness_popup, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Độ sáng", font=("Arial", 12))
        brightness_scale.pack(padx=10, pady=10)

        # Nút xác nhận
        confirm_button = tk.Button(brightness_popup, text="Xác nhận", command=lambda: self.adjust_brightness(brightness_scale.get()), font=("Arial", 12))
        confirm_button.pack(padx=10, pady=10)

    def adjust_brightness(self, factor):
        if self.image_path:
            try:
                # Mở ảnh từ đường dẫn tạm thời
                image = Image.open(self.image_path)
                # Tạo một đối tượng ImageEnhance để điều chỉnh độ sáng
                enhancer = ImageEnhance.Brightness(image)
                # Điều chỉnh độ sáng dựa trên yếu tố được chọn
                modified_image = enhancer.enhance(factor)
                # Hiển thị ảnh đã điều chỉnh trong giao diện
                self.display_image(modified_image)
            except Exception as e:
                messagebox.showerror("Lỗi", "Đã xảy ra lỗi trong quá trình điều chỉnh độ sáng:\n{}".format(str(e)))
        else:
            messagebox.showerror("Lỗi", "Không có ảnh để điều chỉnh độ sáng!")

def main():
    root = tk.Tk()
    app = TextToImageApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
