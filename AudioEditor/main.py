import os
from tkinter import Tk, Label, Button, filedialog, messagebox, Scale, HORIZONTAL, Entry, Canvas
from pydub import AudioSegment
from pydub.utils import which
from pydub.playback import play
from threading import Thread
import time

class SimpleAudioEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Простой Аудиоредактор")
        self.root.geometry("600x500")

        self.audio_file = None
        self.audio = None
        self.audio_length = 0
        self.is_playing = False
        self.play_thread = None

        Label(root, text="Простой Аудиоредактор", font=("Arial", 16)).pack(pady=10)

        Button(root, text="Открыть аудиофайл", command=self.load_audio).pack(pady=5)

        # Добавляем плеер
        Label(root, text="Плеер").pack(pady=5)
        self.canvas = Canvas(root, height=20, width=500, bg="gray")
        self.canvas.pack(pady=5)
        Button(root, text="▶️ Воспроизвести", command=self.start_playing).pack(side="left", padx=10)
        Button(root, text="⏸️ Пауза", command=self.pause_audio).pack(side="left", padx=10)

        Label(root, text="Обрезка файла").pack(pady=10)
        self.trim_start = Scale(root, from_=0, to=100, orient=HORIZONTAL, label="Начало (%)")
        self.trim_start.pack(pady=5)
        self.trim_end = Scale(root, from_=0, to=100, orient=HORIZONTAL, label="Конец (%)")
        self.trim_end.set(100)
        self.trim_end.pack(pady=5)
        Button(root, text="Применить обрезку", command=self.trim_audio).pack(pady=5)

        Label(root, text="Изменение громкости").pack(pady=10)
        Label(root, text="Введите значение в дБ (например, -5 или 10)").pack()
        self.volume_entry = Entry(root, width=10)
        self.volume_entry.pack(pady=5)
        Button(root, text="Применить громкость", command=self.adjust_volume).pack(pady=5)

        Button(root, text="Сохранить файл", command=self.save_audio).pack(pady=10)

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])

        if file_path:
            self.audio_file = file_path
            self.audio = AudioSegment.from_file(file_path)
            self.audio_length = len(self.audio)
            self.is_playing = False
            messagebox.showinfo("Файл загружен", f"Файл {os.path.basename(file_path)} успешно загружен.")

    def play_audio(self):
        """Функция для воспроизведения аудио с визуализацией."""

        self.is_playing = True
        step = self.canvas.winfo_width() / self.audio_length  # Шаг полосы прогресса
        position = 0
        while self.is_playing and position < self.audio_length:
            time.sleep(0.1)  # Каждые 100 мс обновляем
            position += 100
            self.update_progress(position, step)
        self.is_playing = False

    def update_progress(self, position, step):
        """Обновление полосы прогресса."""
        self.canvas.delete("progress")
        self.canvas.create_rectangle(0, 0, step * position, 20, fill="green", tags="progress")

    def start_playing(self):
        if self.audio:
            if self.play_thread is None or not self.play_thread.is_alive():
                self.play_thread = Thread(target=lambda: (play(self.audio), self.play_audio()))
                self.play_thread.start()
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")

    def pause_audio(self):
        self.is_playing = False

    def trim_audio(self):
        if self.audio:
            start_percent = self.trim_start.get()
            end_percent = self.trim_end.get()
            if start_percent >= end_percent:
                messagebox.showerror("Ошибка", "Начало должно быть меньше конца.")
                return
            start_ms = len(self.audio) * (start_percent / 100)
            end_ms = len(self.audio) * (end_percent / 100)
            self.audio = self.audio[int(start_ms):int(end_ms)]
            self.audio_length = len(self.audio)
            self.canvas.delete("progress")
            messagebox.showinfo("Обрезка завершена", f"Файл обрезан: {start_percent}% - {end_percent}%.")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")

    def adjust_volume(self):
        if self.audio:
            try:
                db_change = float(self.volume_entry.get())
                self.audio = self.audio + db_change
                messagebox.showinfo("Громкость изменена", f"Громкость изменена на {db_change} дБ.")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное числовое значение громкости.")
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