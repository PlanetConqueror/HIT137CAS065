#https://github.com/PlanetConqueror/HIT137CAS065

import tkinter as tk
from tkinter import messagebox

# Dummy AI model for sentiment analysis (for demonstration)
def sentiment_analysis(comment):
    # Normally this would be an AI model predicting sentiment
    # Here, we simulate a positive/negative comment based on length.
    return "Positive" if len(comment) % 2 == 0 else "Negative"

# Decorator to log button clicks (example of a decorator in Python)
def button_click_logger(func):
    def wrapper(*args, **kwargs):
        print(f"Button clicked: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Base class for the YouTube interface
class YouTubeInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Like Interface")
        self.geometry("400x300")

        # Encapsulation of the 'likes' and 'subscribers' attributes
        self._likes = 0  # Protected attribute (encapsulated)
        self._subscribers = 0

        self.create_widgets()

    def create_widgets(self):
        self.like_button = tk.Button(self, text="Like", command=self.like_video)
        self.like_button.pack(pady=10)

        self.subscribe_button = tk.Button(self, text="Subscribe", command=self.subscribe)
        self.subscribe_button.pack(pady=10)

        self.comment_label = tk.Label(self, text="Leave a comment:")
        self.comment_label.pack(pady=10)

        self.comment_entry = tk.Entry(self)
        self.comment_entry.pack(pady=5)

        self.submit_button = tk.Button(self, text="Submit Comment", command=self.submit_comment)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self, text="")
        self.result_label.pack(pady=10)

    @button_click_logger  # Applying decorator
    def like_video(self):
        self._likes += 1  # Encapsulation: Direct access is avoided
        messagebox.showinfo("Likes", f"Video Liked! Total Likes: {self._likes}")

    @button_click_logger
    def subscribe(self):
        self._subscribers += 1  # Encapsulation: Direct access is avoided
        messagebox.showinfo("Subscribers", f"Subscribed! Total Subscribers: {self._subscribers}")

    # Method overriding to implement different behavior in a derived class
    def submit_comment(self):
        comment = self.comment_entry.get()
        sentiment = sentiment_analysis(comment)
        self.result_label.config(text=f"Sentiment: {sentiment}")

# Another class that inherits from YouTubeInterface and adds extra functionality
class YouTubePremiumInterface(YouTubeInterface):
    def __init__(self):
        super().__init__()
        self.title("YouTube Premium Like Interface")

    # Method overriding to change behavior for Premium users
    @button_click_logger
    def subscribe(self):
        self._subscribers += 1
        messagebox.showinfo("Subscribers", f"Premium Subscription Added! Total Subscribers: {self._subscribers}")

    # Polymorphism example: Although the method has the same name as the base class,
    # the functionality can be different.
    def submit_comment(self):
        comment = self.comment_entry.get()
        sentiment = sentiment_analysis(comment)
        if sentiment == "Positive":
            self.result_label.config(text="Thank you for the positive comment! Sentiment: Positive")
        else:
            self.result_label.config(text="We appreciate your feedback. Sentiment: Negative")

# Multiple inheritance example with a class adding additional features
class NotificationFeature:
    def show_notification(self, message):
        print(f"Notification: {message}")
        messagebox.showinfo("Notification", message)

class YouTubeWithNotification(YouTubePremiumInterface, NotificationFeature):
    # We are inheriting from both YouTubePremiumInterface and NotificationFeature
    # This showcases multiple inheritance
    def __init__(self):
        super().__init__()

    def like_video(self):
        super().like_video()  # Calling parent method (polymorphism)
        self.show_notification("Thank you for the like! Here's a cookie for you!")

    def subscribe(self):
        super().subscribe()  # Calling parent method (polymorphism)
        self.show_notification("Thank you for subscribing our channel!")

if __name__ == "__main__":
    # Instantiate the main application class
    app = YouTubeWithNotification()
    app.mainloop()
