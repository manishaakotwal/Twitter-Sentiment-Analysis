import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from textblob import TextBlob


def analyze_sentiment():
    text_to_analyze = entry.get()

    if not text_to_analyze:
        messagebox.showwarning("Warning", "Please enter a tweet for analysis.")
        return

    blob = TextBlob(text_to_analyze)
    sentiment = blob.sentiment.polarity

    if sentiment > 0:
        result = "Positive"
    elif sentiment < 0:
        result = "Negative"
    else:
        result = "Neutral"

    result_label.config(text=f"Sentiment: {result}")


def plot_sentiment_percentage():
    try:
        num_tweets = int(num_tweets_entry.get())
    except ValueError:
        messagebox.showwarning("Warning", "Please enter a valid number of tweets.")
        return

    with open(r'C:\Users\lenovo\Downloads\training.1600000.processed.noemoticon.csv',
              encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        text_data = [row[5] for row in reader if len(row) > 5][:num_tweets]

    # Perform sentiment analysis on each tweet
    sentiments = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    for text in text_data:
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            sentiments['Positive'] += 1
        elif sentiment < 0:
            sentiments['Negative'] += 1
        else:
            sentiments['Neutral'] += 1

    # Create a pie chart
    labels = sentiments.keys()
    sizes = sentiments.values()

    # Clear previous plot
    for widget in frame.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'red', 'gray'])
    ax.set_title('Sentiment Percentage Analysis')

    # Display the plot in the Tkinter window
    canvas_widget = FigureCanvasTkAgg(fig, master=window)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().grid(column=0, row=6, pady=10)


# GUI setup
window = tk.Tk()
window.title("Twitter Sentiment Analysis")

frame = ttk.Frame(window, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label = ttk.Label(frame, text="Enter Tweet:")
label.grid(column=0, row=0, columnspan=2, pady=10)

entry = ttk.Entry(frame, width=40)
entry.grid(column=0, row=1, columnspan=2, pady=10)

analyze_button = ttk.Button(frame, text="Analyze", command=analyze_sentiment)
analyze_button.grid(column=0, row=2, columnspan=2, pady=10)

result_label = ttk.Label(frame, text="Sentiment: ")
result_label.grid(column=0, row=3, columnspan=2, pady=10)

num_tweets_label = ttk.Label(frame, text="Number of Tweets:")
num_tweets_label.grid(column=0, row=4, pady=10)

num_tweets_entry = ttk.Entry(frame, width=10)
num_tweets_entry.grid(column=1, row=4, pady=10)

plot_button = ttk.Button(frame, text="Plot Sentiment Percentage", command=plot_sentiment_percentage)
plot_button.grid(column=0, row=5, columnspan=2, pady=10)

window.mainloop()