import tkinter as tk
import requests

API_URL = "http://localhost:8000/api/setStatus/"  # For local development

def update_status(value):
    try:
        # Convert boolean to string for the API
        if isinstance(value, bool):
            value = str(value)
        
        response = requests.get(f"{API_URL}?value={value}")
        response.raise_for_status()
        result_label.config(text=f"✅ Sent: {value}")
        print(f"✅ Status sent: {value}")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"❌ Error: {e}")
        print(f"❌ Error sending status: {e}")

def password_correct():
    update_status("True")

def password_incorrect():
    update_status("False")

def is_yleoba():
    update_status("yle")

def attempts():
    update_status("yle2")

def auth():
    update_status("yle3")

def create_gui():
    window = tk.Tk()
    window.title("Status Control App")
    window.geometry("400x400")

    # Status labels
    status_label = tk.Label(window, text="Send Status to Server", font=("Arial", 14, "bold"))
    status_label.pack(pady=20)

    # Buttons
    correct_button = tk.Button(window, text="✅ Password is Correct", command=password_correct, bg="#4CAF50", fg="white")
    correct_button.pack(pady=10, padx=20, fill="x")

    incorrect_button = tk.Button(window, text="❌ Password is Incorrect", command=password_incorrect, bg="#ff9800", fg="white")
    incorrect_button.pack(pady=10, padx=20, fill="x")

    yleoba = tk.Button(window, text="🚨 YLEOBA Detected", command=is_yleoba, bg="#f44336", fg="white")
    yleoba.pack(pady=10, padx=20, fill="x")

    attempts_btn = tk.Button(window, text="📊 Attempts Recorded", command=attempts, bg="#2196F3", fg="white")
    attempts_btn.pack(pady=10, padx=20, fill="x")

    auth_btn = tk.Button(window, text="🔐 Approval Triggered", command=auth, bg="#9C27B0", fg="white")
    auth_btn.pack(pady=10, padx=20, fill="x")

    # Result label
    global result_label
    result_label = tk.Label(window, text="Ready", font=("Arial", 10), wraplength=350)
    result_label.pack(pady=20)

    # Status indicator
    status_indicator = tk.Label(window, text="● Connected", font=("Arial", 10), fg="green")
    status_indicator.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()