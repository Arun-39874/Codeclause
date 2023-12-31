import tkinter as tk
import random
import time
from faker import Faker

class SpeedTypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Typing Test")
        self.root.configure(bg="#F5F5F5")  # Background color

        self.faker = Faker()
        self.stories = self.generate_stories()
        self.current_story = tk.StringVar()
        self.custom_timer_minutes = tk.StringVar(value="1")  # Default timer duration is 1 minute

        self.is_test_running = False
        self.timer_seconds = 0

        self.setup_ui()

    def generate_stories(self, num_stories=20):
        stories = []
        for _ in range(num_stories):
            story = self.faker.paragraph(nb_sentences=10)  # Adjust the number of sentences as needed
            stories.append(story)
        return stories

    def start_test(self):
        self.is_test_running = True
        random.shuffle(self.stories)
        self.next_story()
        self.start_time = time.time()
        self.timer_seconds = int(self.custom_timer_minutes.get()) * 60  # Convert minutes to seconds
        self.update_timer()

    def end_test(self):
        if self.is_test_running:
            self.is_test_running = False
            self.show_results()

    def reset_test(self):
        self.is_test_running = False
        self.stories = self.generate_stories()
        self.current_story.set("")
        self.timer_seconds = 0
        self.timer_label.config(text="Time remaining: 00:00")
        self.story_label.config(text="")
        self.text_area.delete("1.0", tk.END)

        # Clear the result label if it exists
        try:
            self.result_label.destroy()
        except AttributeError:
            pass

    def next_story(self):
        if self.stories:
            self.current_story.set(self.stories.pop(0))
            self.story_label.config(text=self.current_story.get())

    def show_results(self):
        end_time = time.time()
        total_time = end_time - self.start_time
        stories_per_minute = int(len(self.stories) / total_time * 60)
        accuracy = self.calculate_accuracy()

        result_text = "Typing test complete!\nTotal time: {:.2f} seconds\nWords per minute: {}\nAccuracy: {:.2f}%".format(
            total_time, stories_per_minute, accuracy
        )

        self.result_label = tk.Label(self.root, text=result_text, font=("Helvetica", 14), bg="#F5F5F5")  # Background color
        self.result_label.grid(row=2, column=0, columnspan=3, pady=20)

    def calculate_accuracy(self):
        typed_text = self.text_area.get("1.0", tk.END).strip().lower()
        target_text = self.current_story.get().lower()

        # Split the text into words
        typed_words = typed_text.split()
        target_words = target_text.split()

        # Calculate the number of correct words and total words
        correct_words = sum(tw == tt for tw, tt in zip(typed_words, target_words))
        total_words = len(target_words)

        # Calculate accuracy based on correct words and total words
        accuracy = (correct_words / total_words) * 100 if total_words > 0 else 100

        return accuracy

    def update_timer(self):
        if self.is_test_running and self.timer_seconds > 0:
            self.timer_seconds -= 1
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.timer_label.config(text=f"Time remaining: {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)  # Schedule the function to run after 1000 milliseconds (1 second)
        elif self.is_test_running:
            self.end_test()  # Automatically end the test when the timer reaches 0

    def on_enter_press(self, event):
        # Move the cursor to the next line in the Text widget
        self.text_area.insert(tk.END, '\n')
        return 'break'  # Prevents the default behavior of adding a newline in the Text widget

    def setup_ui(self):
        title_label = tk.Label(self.root, text="Typing Test", font=("Helvetica", 16), bg="#4CAF50", fg="white")
        title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

        timer_label = tk.Label(self.root, text="Set Timer (minutes):", font=("Helvetica", 12), bg="#F5F5F5")  # Background color
        timer_label.grid(row=1, column=0, columnspan=3, pady=5)

        timer_entry = tk.Entry(self.root, textvariable=self.custom_timer_minutes, font=("Helvetica", 12), width=5)
        timer_entry.grid(row=2, column=0, columnspan=3, pady=5)

        start_button = tk.Button(self.root, text="Start Test", command=self.start_test, bg="#4CAF50", fg="white")
        start_button.grid(row=3, column=2, pady=5, padx=(0, int(self.root.winfo_screenwidth() * 0.25)), sticky="e")

        end_button = tk.Button(self.root, text="End Test", command=self.end_test, bg="#FF5733", fg="white")
        end_button.grid(row=4, column=2, pady=5, padx=(0, int(self.root.winfo_screenwidth() * 0.25)), sticky="e")

        self.timer_label = tk.Label(self.root, text="Time remaining: 00:00", font=("Helvetica", 12), bg="#F5F5F5")  # Background color
        self.timer_label.grid(row=5, column=0, columnspan=3, pady=5)

        self.story_label = tk.Label(self.root, textvariable=self.current_story, font=("Helvetica", 14), wraplength=800, bg="#F5F5F5")  # Background color
        self.story_label.grid(row=6, column=0, columnspan=3, pady=20)

        self.text_area = tk.Text(self.root, wrap="word", font=("Helvetica", 12), height=10, width=80)
        self.text_area.grid(row=7, column=0, columnspan=3, pady=20)

        entry_frame = tk.Frame(self.root, bg="#F5F5F5")  # Background color
        entry_frame.grid(row=8, column=0, columnspan=3)

        # Remove the Check button and add Reset button
        reset_button = tk.Button(entry_frame, text="Reset", command=self.reset_test, bg="#3498DB", fg="white")
        reset_button.grid(row=0, column=0, pady=10)

        # Configure row and column weights to make the Text area expandable
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTypingTest(root)
    root.mainloop()
