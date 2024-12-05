import os
from tkinter import Tk, Label, Button, filedialog, messagebox, Scale, HORIZONTAL, Canvas, Entry
import pygame
from pydub import AudioSegment


class SimpleAudioEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Простой Аудиоплеер и Редактор")
        self.root.geometry("600x750")

        self.audio_file = None
        self.audio = None
        self.audio_length = 0
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0  # Текущее время воспроизведения (в секундах)
        self.history = []  # Стек состояний

        pygame.mixer.init()

        Label(root, text="Простой Аудиоплеер и Редактор", font=("Arial", 16)).pack(pady=10)

        Button(root, text="Открыть аудиофайл", command=self.load_audio).pack(pady=5)

        # Полоса прогресса
        Label(root, text="Плеер").pack(pady=5)
        self.canvas = Canvas(root, height=20, width=500, bg="gray")
        self.canvas.pack(pady=10)
        self.time_label = Label(root, text="00:00 / 00:00", font=("Arial", 12))
        self.time_label.pack(pady=5)
        Button(root, text="▶️ Воспроизвести", command=self.play_audio).pack(side="left", padx=10)
        Button(root, text="⏸️ Пауза", command=self.pause_audio).pack(side="left", padx=10)
        Button(root, text="⏹️ Остановить", command=self.stop_audio).pack(side="left", padx=10)

        # Обрезка
        Label(root, text="Обрезка аудиофайла").pack(pady=10)
        self.trim_start = Scale(root, from_=0, to=100, orient=HORIZONTAL, label="Начало (%)")
        self.trim_start.pack(pady=5)
        self.trim_end = Scale(root, from_=0, to=100, orient=HORIZONTAL, label="Конец (%)")
        self.trim_end.set(100)
        self.trim_end.pack(pady=5)
        Button(root, text="Применить обрезку", command=self.trim_audio).pack(pady=5)

        # Изменение громкости
        Label(root, text="Изменение громкости").pack(pady=10)
        Label(root, text="Введите значение в дБ (например, -5 или 10)").pack()
        self.volume_entry = Entry(root, width=10)
        self.volume_entry.pack(pady=5)
        Button(root, text="Применить громкость", command=self.adjust_volume).pack(pady=5)

        # Изменение скорости
        Label(root, text="Изменение скорости воспроизведения").pack(pady=10)
        self.speed_scale = Scale(root, from_=50, to=300, orient=HORIZONTAL, label="Скорость (%)", resolution=5)
        self.speed_scale.set(100)
        self.speed_scale.pack(pady=5)
        Button(root, text="Применить скорость", command=self.change_speed).pack(pady=5)

        # Управление состояниями
        Button(root, text="Отменить последнее действие", command=self.undo_last_change).pack(pady=5)

        # Сохранение
        Button(root, text="Сохранить аудиофайл", command=self.save_audio).pack(pady=10)

        # Удаление временных файлов при закрытии
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup_temp_files)

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.audio_file = file_path
            self.audio = AudioSegment.from_file(file_path)
            self.history.clear()
            self.add_to_history()
            self.audio = AudioSegment.from_file(file_path)
            self.audio_length = len(self.audio) / 1000  # Длина в секундах
            pygame.mixer.music.load(file_path)
            self.is_playing = False
            self.current_position = 0
            self.canvas.delete("progress")
            self.update_time_label(0, self.audio_length)
            messagebox.showinfo("Файл загружен", f"Файл {os.path.basename(file_path)} успешно загружен.")

    def play_audio(self):
        if self.audio_file:
            if not self.is_playing:
                pygame.mixer.music.play(start=self.current_position)
                self.is_playing = True
                self.is_paused = False
                self.update_progress()
            elif self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.update_progress()
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")

    def pause_audio(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.current_position += pygame.mixer.music.get_pos() / 1000  # Обновляем позицию

    def stop_audio(self):
        if self.is_playing or self.is_paused:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.current_position = 0
            self.canvas.delete("progress")
            self.update_time_label(0, self.audio_length)

    def update_progress(self):
        if self.is_playing and not self.is_paused:
            current_time = self.current_position + pygame.mixer.music.get_pos() / 1000
            width = self.canvas.winfo_width()
            progress_width = int((current_time / self.audio_length) * width)
            self.canvas.delete("progress")
            self.canvas.create_rectangle(0, 0, progress_width, 20, fill="green", tags="progress")
            self.update_time_label(current_time, self.audio_length)

            if current_time < self.audio_length:
                self.root.after(100, self.update_progress)  # Обновление каждые 100 мс
            else:
                self.stop_audio()

    def update_time_label(self, current_time, total_time):
        current_minutes = int(current_time // 60)
        current_seconds = int(current_time % 60)
        total_minutes = int(total_time // 60)
        total_seconds = int(total_time % 60)
        self.time_label.config(text=f"{current_minutes:02}:{current_seconds:02} / {total_minutes:02}:{total_seconds:02}")

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
            self.audio_length = len(self.audio) / 1000
            self.canvas.delete("progress")
            self.update_time_label(0, self.audio_length)
            self.update_audio_file()
            messagebox.showinfo("Обрезка завершена", f"Файл обрезан: {start_percent}% - {end_percent}%.")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")

    def adjust_volume(self):
        if self.audio:
            try:
                db_change = float(self.volume_entry.get())
                self.audio = self.audio + db_change
                self.update_audio_file()
                messagebox.showinfo("Громкость изменена", f"Громкость изменена на {db_change} дБ.")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное числовое значение громкости.")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")

    def change_speed(self):
        if self.audio:
            speed_percent = self.speed_scale.get()
            self.audio = self.audio.speedup(playback_speed=speed_percent / 100.0)
            self.audio_length = len(self.audio) / 1000
            self.update_audio_file()
            messagebox.showinfo("Скорость изменена", f"Скорость изменена на {speed_percent}%.")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")

    def update_audio_file(self):
        if self.is_playing or self.is_paused:
            self.stop_audio()
        temp_file = f"Temp/temp_audio_{len(self.history)}.wav"
        self.audio.export(temp_file, format="wav")
        self.add_to_history()
        pygame.mixer.music.load(temp_file)
        self.audio_file = temp_file

    def add_to_history(self):
        temp_file = f"Temp/temp_audio_{len(self.history)}.wav"
        pygame.mixer.music.unload()
        self.audio.export(temp_file, format="wav")
        self.history.append(temp_file)

    def undo_last_change(self):

        if len(self.history) > 1:
            if self.is_playing or self.is_paused:
                self.stop_audio()
            last_file = self.history.pop()
            pygame.mixer.music.unload()
            os.remove(last_file)  # Удаляем последний временный файл
            previous_file = self.history[-1]
            self.audio = AudioSegment.from_file(previous_file)
            pygame.mixer.music.load(previous_file)
            self.audio_file = previous_file
            self.audio_length = len(self.audio) / 1000
            self.canvas.delete("progress")
            self.update_time_label(0, self.audio_length)
            messagebox.showinfo("Откат изменений", "Последнее действие отменено.")
        else:
            messagebox.showinfo("Откат невозможен", "Нет предыдущих действий для отмены.")

    def save_audio(self):
        if self.audio:
            save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if save_path:
                self.audio.export(save_path, format="wav")
                messagebox.showinfo("Сохранено", f"Файл сохранён как {os.path.basename(save_path)}.")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")

    def cleanup_temp_files(self):
        pygame.mixer.music.unload()
        for temp_file in self.history:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = SimpleAudioEditor(root)
    root.mainloop()