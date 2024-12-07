import os
from tkinter import Tk, Label, Button, filedialog, messagebox, Scale, HORIZONTAL, Canvas, Entry, PhotoImage
import pygame
from pydub import AudioSegment


class SimpleAudioEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("AudioEditorMini")
        self.root.geometry("984x520")
        self.root.configure(bg="#FFFFFF")

        self.audio_file = None
        self.audio = None
        self.audio_length = 0
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0  # Текущее время воспроизведения (в секундах)
        self.history = []  # Стек состояний
        self.images = []
        pygame.mixer.init()

        canvas = Canvas(
            root,
            bg="#FFFFFF",
            height=520,
            width=984,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Изображения
        image_image_1 = PhotoImage(file="Assets/image_1.png")
        self.images.append(image_image_1)
        canvas.create_image(55.0, 53.0, image=image_image_1)

        image_image_2 = PhotoImage(file="Assets/image_2.png")
        self.images.append(image_image_2)
        canvas.create_image(491.0, 332.0, image=image_image_2)

        image_image_3 = PhotoImage(file="Assets/image_3.png")
        self.images.append(image_image_3)
        canvas.create_image(190.0, 327.0, image=image_image_3)

        image_image_4 = PhotoImage(file="Assets/image_4.png")
        self.images.append(image_image_4)
        canvas.create_image(505.0, 327.0, image=image_image_4)

        image_image_5 = PhotoImage(file="Assets/image_5.png")
        self.images.append(image_image_5)
        canvas.create_image(807.0, 327.0, image=image_image_5)

        # Кнопки управления
        button_image_1 = PhotoImage(file="Assets/import.png")
        self.images.append(button_image_1)
        import_button = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_audio,
            relief="flat"
        )
        import_button.place(x=39.0, y=444.0, width=173.0, height=40.0)

        button_image_2 = PhotoImage(file="Assets/revert_button.png")
        self.images.append(button_image_2)
        revert_button = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.undo_last_change,
            relief="flat"
        )
        revert_button.place(x=772.0, y=444.0, width=173.0, height=40.0)

        button_image_3 = PhotoImage(file="Assets/export_button.png")
        self.images.append(button_image_3)
        export_button = Button(
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_audio,
            relief="flat"
        )
        export_button.place(x=239.0, y=444.0, width=173.0, height=40.0)

        # Кнопки воспроизведения
        button_image_4 = PhotoImage(file="Assets/play_button.png")
        self.images.append(button_image_4)
        play_button = Button(
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.play_audio,
            relief="flat"
        )
        play_button.place(x=445.0, y=170.0, width=32.0, height=32.0)

        button_image_5 = PhotoImage(file="Assets/pause_button.png")
        self.images.append(button_image_5)
        pause_button = Button(
            image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.pause_audio,
            relief="flat"
        )
        pause_button.place(x=484.0, y=170.0, width=32.0, height=32.0)

        button_image_6 = PhotoImage(file="Assets/stop_button.png")
        self.images.append(button_image_6)
        stop_button = Button(
            image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop_audio,
            relief="flat"
        )
        stop_button.place(x=523.0, y=170.0, width=32.0, height=32.0)

        # Полоса прогресса
        self.canvas_progress = Canvas(root, height=20, width=500, bg="#f5f5f5")
        self.canvas_progress.place(x=250.0, y=135.0)
        self.time_label = Label(canvas, text="00:00 | 00:00", font=("Arial", 12), bg="white")
        self.time_label.place(x=451.5, y=100.0)

        # Ввод границ обрезки
        short_entry_image = PhotoImage(file="Assets/short_entry.png")
        self.images.append(short_entry_image)
        canvas.create_image(110.0, 327.0, image=short_entry_image)
        canvas.create_image(155.0, 327.0, image=short_entry_image)
        canvas.create_image(226.0, 327.0, image=short_entry_image)
        canvas.create_image(271.0, 327.0, image=short_entry_image)

        self.start_minute_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.start_minute_entry.place(x=103.4, y=317.0, width=18.0, height=20.0)

        self.start_second_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.start_second_entry.place(x=148.4, y=317.0, width=18.0, height=20.0)

        self.end_minute_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.end_minute_entry.place(x=219.4, y=317.0, width=18.0, height=20.0)

        self.end_second_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.end_second_entry.place(x=264.4, y=317.0, width=18.0, height=20.0)

        # Изменение громкости
        entry_image_5 = PhotoImage(file="Assets/volume_entry.png")
        self.images.append(entry_image_5)
        canvas.create_image(790.0, 327.0, image=short_entry_image)
        self.volume_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.volume_entry.place(x=780.0, y=317.0, width=21.0, height=20.0)

        # Изменение скорости

        self.speed_scale = Scale(root, from_=10, to=200, orient=HORIZONTAL, resolution=1, bg="#FFFFFF")
        self.speed_scale.set(100)
        self.speed_scale.place(x=375.0, y=300.0, width = 260.0, height = 50.0)

        # GUI
        canvas.create_text(367.5, 275.0, anchor="nw", text="Изменить скорость воспроизведения", fill="#000000",font=("Inter", 16 * -1))
        canvas.create_text(730.0, 274.0, anchor="nw", text="Изменить громкость", fill="#000000",font=("Inter", 16 * -1))
        canvas.create_text(151.0, 273.0, anchor="nw", text="Обрезать", fill="#000000", font=("Inter", 16 * -1))
        canvas.create_text(810.0, 315.0, anchor="nw", text="Дб", fill="#000000", font=("Inter", 20 * -1))

        canvas.create_rectangle(131.0, 312.0, 132.0, 340.0, fill="#000000", outline="")
        canvas.create_rectangle(247.0, 312.0, 248.0, 340.0, fill="#000000", outline="")
        canvas.create_rectangle(176.0, 326.0, 204.0, 327.0, fill="#000000", outline="")

        # Кнопки "Применить"
        apply_image = PhotoImage(file="Assets/apply.png")
        self.images.append(apply_image)
        speed_apply_button = Button(
            image=apply_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.change_speed,
            relief="flat"
        )
        speed_apply_button.place(x=448.0, y=363.0, width=113.0, height=27.0)

        trim_apply_button = Button(
            image=apply_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.trim_audio,
            relief="flat"
        )
        trim_apply_button.place(x=132.0, y=363.0, width=113.0, height=27.0)

        volume_apply_button = Button(
            image=apply_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.adjust_volume,
            relief="flat"
        )
        volume_apply_button.place(x=751.0, y=363.0, width=113.0, height=27.0)

        root.resizable(False, False)
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
            self.canvas_progress.delete("progress")
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
            self.current_position += pygame.mixer.music.get_pos() / 10000  # Обновляем позицию

    def stop_audio(self):
        if self.is_playing or self.is_paused:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.current_position = 0
            self.canvas_progress.delete("progress")
            self.update_time_label(0, self.audio_length)

    def update_progress(self):
        if self.is_playing and not self.is_paused:
            current_time = self.current_position + pygame.mixer.music.get_pos() / 1000
            width = self.canvas_progress.winfo_width()
            progress_width = int((current_time / self.audio_length) * width)
            self.canvas_progress.delete("progress")
            self.canvas_progress.create_rectangle(0, 0, progress_width, 20, fill="black", tags="progress")
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
        self.time_label.config(text=f"{current_minutes:02}:{current_seconds:02} | {total_minutes:02}:{total_seconds:02}")

    def trim_audio(self):
        if self.audio:
            try:
                # Получаем минуты и секунды для начала и конца обрезки
                start_minute = int(self.start_minute_entry.get())
                start_second = int(self.start_second_entry.get())
                end_minute = int(self.end_minute_entry.get())
                end_second = int(self.end_second_entry.get())

                # Проверяем, чтобы секунды были в пределах 0-59
                if start_second < 0 or start_second >= 60 or end_second < 0 or end_second >= 60:
                    messagebox.showerror("Ошибка", "Секунды должны быть от 0 до 59.")
                    return

                # Переводим время в миллисекунды
                start_ms = (start_minute * 60 + start_second) * 1000
                end_ms = (end_minute * 60 + end_second) * 1000

                # Проверяем, чтобы начало было меньше конца
                if start_ms >= end_ms or end_ms > len(self.audio):
                    messagebox.showerror("Ошибка", "Неверно указан интервал обрезки.")
                    return

                # Применяем обрезку
                self.audio = self.audio[start_ms:end_ms]
                self.audio_length = len(self.audio) / 1000  # Обновляем длину аудио
                self.canvas_progress.delete("progress")
                self.update_time_label(0, self.audio_length)
                self.update_audio_file()

                messagebox.showinfo("Обрезка завершена", f"Аудиофайл обрезан: {start_minute}:{start_second} - {end_minute}:{end_second}.")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные числовые значения для минут и секунд.")
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
            self.canvas_progress.delete("progress")
            self.update_time_label(0, self.audio_length)
            messagebox.showinfo("Откат изменений", "Последнее действие отменено.")
        else:
            messagebox.showinfo("Откат невозможен", "Нет предыдущих действий для отмены.")

    def save_audio(self):
        if self.audio:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")]
            )
            if save_path:
                try:
                    if save_path.endswith(".mp3"):
                        self.audio.export(save_path, format="mp3")
                    else:
                        self.audio.export(save_path, format="wav")
                    messagebox.showinfo("Сохранено", f"Файл сохранён как {os.path.basename(save_path)}.")
                except Exception as e:
                    messagebox.showerror("Ошибка сохранения", f"Произошла ошибка при сохранении файла: {str(e)}")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите аудиофайл.")
    def cleanup_temp_files(self):
        pygame.mixer.music.unload()
        temp_dir = os.path.join("Temp")
        if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
            try:
                for filename in os.listdir(temp_dir):
                    if filename.startswith("temp_audio_"):
                        file_path = os.path.join(temp_dir, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось очистить файлы в папке Temp: {str(e)}")
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = SimpleAudioEditor(root)
    root.mainloop()