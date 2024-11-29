import os
from tkinter import Tk, Label, Button, filedialog, messagebox
from pydub import AudioSegment


class SimpleAudioEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Простой Аудиоредактор")
        self.root.geometry("400x200")

        self.audio_file = None
        self.audio = None

        Label(root, text="Простой Аудиоредактор", font=("Arial", 16)).pack(pady=10)

        Button(root, text="Открыть аудиофайл", command=self.load_audio).pack(pady=5)
        Button(root, text="Обрезать (0-10 сек)", command=self.trim_audio).pack(pady=5)
        Button(root, text="Изменить громкость (+5 дБ)", command=self.increase_volume).pack(pady=5)
        Button(root, text="Сохранить файл", command=self.save_audio).pack(pady=5)

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.audio_file = file_path
            self.audio = AudioSegment.from_file(file_path)
            messagebox.showinfo("Файл загружен", f"Файл {os.path.basename(file_path)} успешно загружен.")

    def trim_audio(self):
        if self.audio:
            self.audio = self.audio[:10000]  # Обрезаем первые 10 секунд
            messagebox.showinfo("Обрезка завершена", "Аудиофайл обрезан до первых 10 секунд.")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")

    def increase_volume(self):
        if self.audio:
            self.audio = self.audio + 5  # Увеличиваем громкость на 5 дБ
            messagebox.showinfo("Громкость изменена", "Громкость увеличена на 5 дБ.")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")

    def save_audio(self):
        if self.audio:
            save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
            if save_path:
                self.audio.export(save_path, format="mp3")
                messagebox.showinfo("Файл сохранен", f"Файл успешно сохранен: {save_path}")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите и обработайте аудиофайл.")


if __name__ == "__main__":
    root = Tk()
    app = SimpleAudioEditor(root)
    root.mainloop()