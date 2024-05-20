import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog, messagebox
import backend
import sys
import os




def create_fullscreen_app():
    root = tk.Tk()
    root.title("CSV Chat Agent")
    root.state("zoomed")

    # Define custom fonts
    bold_font = tkfont.Font(size=12, weight="bold")
    normal_font = tkfont.Font(size=10, weight="normal")

    # Instructions Text widget
    instructions_text = tk.Text(
        root,
        height=4,
        wrap="word",
        borderwidth=0,
        background=root.cget("background"),
        relief="flat",
    )
    instructions_text.pack(fill="x", padx=10, pady=5)
    instructions_text.tag_configure("bold", font=bold_font)
    instructions_text.tag_configure("normal", font=normal_font)

    instructions_text.insert("end", "Instructions: ", "bold")
    instructions_text.insert(
        "end",
        'Click "Upload From Computer" and select a valid .csv file to upload.\n'
        "Submit prompts in the chatbar beneath the window.\n"
        'To reset and upload a new .csv file, click the bottom "Reset" button.',
        "normal",
    )
    instructions_text.configure(state="disabled")

    # Upload file section
    top_frame = tk.Frame(root, height=50, pady=5)
    top_frame.pack(fill="x", padx=10, pady=10)
    upload_label = tk.Label(
        top_frame, font=normal_font, text="Upload File (Must Be csv)", anchor="w"
    )
    upload_label.pack(side="left", padx=(10, 5))

    def upload_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSVfiles", "*.csv")])
        chatbox.configure(state="normal")
        chatbox.insert("end", "Computer: ", "bold")
        chatbox.insert("end", "File processing. Please wait... \n", "normal")
        chatbox.yview("end")
        chatbox.configure(state="disabled")
        chatbox.yview("end")
        root.update()

        if file_path:
            success, message = backend.load_csv_agent(file_path)
            chatbox.configure(state="normal")
            if success:
                upload_label.config(text=f"Loaded: {file_path}")
                chatbox.insert("end", "Computer: ", "bold")
                chatbox.insert(
                    "end",
                    "File processed successfully! Please enter a prompt below. \n",
                    "normal",
                )
                user_input.config(state="normal")
                send_button.config(state="normal")
            else:
                messagebox.showerror("Error", message)
                chatbox.insert(
                    "end", f"Computer: Error processing file - {message}\n", "bold"
                )
            chatbox.configure(state="disabled")
            chatbox.yview("end")
        else:
            upload_label.config(text="Upload File (Must Be csv)")
        root.update()

    upload_button = tk.Button(
        top_frame, text="Upload from Computer", command=upload_file
    )
    upload_button.pack(side="left", padx=(5, 10))

    # Chat Frame
    chat_frame = tk.Frame(root)
    chat_frame.pack(fill="x", padx=10, pady=5)

    # Chatbox
    chatbox = tk.Text(chat_frame, height=20, state="disabled", bg="white")
    chatbox.pack(fill="x", padx=10, pady=5)
    chatbox.tag_configure("bold", font=bold_font)  # Configure a bold tag
    chatbox.tag_configure("normal", font=normal_font)  # Configure a normal tag

    # initiate default chatbox
    chatbox.insert("end", "Computer: ", "bold")
    chatbox.insert("end", "Please upload a valid csv file. \n", "normal")
    chatbox.yview("end")

    # Input Frame
    input_frame = tk.Frame(root, height=50)
    input_frame.pack(fill="x", padx=10, pady=5)

    # Layout elements inside the input frame
    input_label = tk.Label(
        input_frame, font=normal_font, text="Enter Your Prompt Here:"
    )
    input_label.pack(side="left", padx=(10, 5))

    user_input = tk.Entry(input_frame, state="disabled")
    user_input.pack(side="left", fill="x", expand=True, padx=(10, 5))

    # Function to handle sending messages
    def send_prompt(event=None):
        prompt = user_input.get()
        if prompt:
            chatbox.configure(state="normal")
            chatbox.insert("end", "User: ", "bold")
            chatbox.insert("end", prompt + "\n", "normal")
            user_input.delete(0, "end")  # Clear the input field
            user_input.configure(state="disabled")
            root.update()
            # Process the message with the backend function
            response = backend.process_prompt(prompt)
            chatbox.insert("end", "Computer: ", "bold")
            chatbox.insert("end", response + "\n", "normal")
            chatbox.configure(state="disabled")
            chatbox.yview("end")  # Auto-scrolls to the bottom
            user_input.configure(state="normal")

    send_button = tk.Button(
        input_frame, text="Send", state="disabled", command=send_prompt
    )
    send_button.pack(side="right", padx=(5, 10))

    # Bind the Enter key to send_message function
    user_input.bind("<Return>", send_prompt)

    def restart_program():
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # reset frame
    reset_frame = tk.Frame(root, height=50)
    reset_frame.pack(fill="x", padx=10, pady=5)

    reset_label = tk.Label(
        reset_frame, font=normal_font, text="Reset Session", anchor="w"
    )
    reset_label.pack(side="left", padx=(10, 5))
    reset_button = tk.Button(reset_frame, text="Reset", command=restart_program)
    reset_button.pack(side="left", padx=(5, 10))

    root.mainloop()


if __name__ == "__main__":
    create_fullscreen_app()
