import tkinter as tk
import serial

# --- SERIAL SETUP ---
# Replace with your Bluetooth serial port (e.g., '/dev/tty.HC-05-DevB')
SERIAL_PORT = '/dev/tty.HC-05-DevB'
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    ser = None
    print(f"Could not open serial port: {e}")

# --- GUI SETUP ---

root = tk.Tk()
root.title("Robot Controls")
root.geometry("800x600")

status_var = tk.StringVar()
status_var.set("Ready" if ser else "Serial not connected!")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(root, text="Robot Control Interface", font=("Helvetica", 16))
label.pack(pady=10)


def send_command(cmd):
    if ser:
        try:
            ser.write(cmd.encode())
            status_var.set(f"Sent: {cmd}")
        except Exception as e:
            status_var.set(f"Error: {e}")
    else:
        status_var.set("Serial not connected!")

# --- BUTTONS WITH ACTIVE STATE ---
btn_forward = tk.Button(frame, text="Forward", width=12, height=2, highlightbackground='SystemButtonFace')
btn_backward = tk.Button(frame, text="Backward", width=12, height=2, highlightbackground='SystemButtonFace')
btn_left = tk.Button(frame, text="Left", width=12, height=2, highlightbackground='SystemButtonFace')
btn_right = tk.Button(frame, text="Right", width=12, height=2, highlightbackground='SystemButtonFace')
btn_grab = tk.Button(frame, text="Grab", width=12, height=2, highlightbackground='SystemButtonFace')
btn_raise = tk.Button(frame, text="Raise", width=12, height=2, highlightbackground='SystemButtonFace')
btn_lower = tk.Button(frame, text="Lower", width=12, height=2, highlightbackground='SystemButtonFace')

# Map commands to buttons for easy access
command_to_button = {
    'F': btn_forward,
    'B': btn_backward,
    'L': btn_left,
    'R': btn_right,
    'G': btn_grab,
    'U': btn_raise,
    'D': btn_lower
}

def button_press(cmd):
    btn = command_to_button[cmd]
    btn.config(highlightbackground='red')
    btn.update_idletasks()  # Force visual update
    send_command(cmd)

def button_release(cmd):
    btn = command_to_button[cmd]
    btn.config(highlightbackground='SystemButtonFace')
    btn.update_idletasks()  # Force visual update

btn_forward.config(command=lambda: button_press('F'))
btn_backward.config(command=lambda: button_press('B'))
btn_left.config(command=lambda: button_press('L'))
btn_right.config(command=lambda: button_press('R'))
btn_grab.config(command=lambda: button_press('G'))
btn_raise.config(command=lambda: button_press('U'))
btn_lower.config(command=lambda: button_press('D'))

# Bind mouse button release to reset color
btn_forward.bind('<ButtonRelease-1>', lambda e: button_release('F'))
btn_backward.bind('<ButtonRelease-1>', lambda e: button_release('B'))
btn_left.bind('<ButtonRelease-1>', lambda e: button_release('L'))
btn_right.bind('<ButtonRelease-1>', lambda e: button_release('R'))
btn_grab.bind('<ButtonRelease-1>', lambda e: button_release('G'))
btn_raise.bind('<ButtonRelease-1>', lambda e: button_release('U'))
btn_lower.bind('<ButtonRelease-1>', lambda e: button_release('D'))

# Layout
btn_forward.grid(row=0, column=1, padx=5, pady=5)
btn_left.grid(row=1, column=0, padx=5, pady=5)
btn_grab.grid(row=1, column=1, padx=5, pady=5)
btn_right.grid(row=1, column=2, padx=5, pady=5)
btn_backward.grid(row=2, column=1, padx=5, pady=5)
btn_raise.grid(row=3, column=0, padx=5, pady=5)
btn_lower.grid(row=3, column=2, padx=5, pady=5)

# --- STATUS LABEL ---
status_label = tk.Label(root, textvariable=status_var, fg="blue")
status_label.pack(pady=10)

# --- KEYBOARD BINDINGS WITH VISUAL FEEDBACK ---
key_to_cmd = {
    'w': 'F',
    's': 'B',
    'a': 'L',
    'd': 'R',
    'up': 'U',
    'down': 'D',
    'space': 'G'
}

pressed_keys = set()

def on_key_press(event):
    key = event.keysym.lower()
    if key in key_to_cmd and key not in pressed_keys:
        label.config(text=f"Key Pressed: {key}")
        cmd = key_to_cmd[key]
        button_press(cmd)
        pressed_keys.add(key)

def on_key_release(event):
    key = event.keysym.lower()
    if key in key_to_cmd and key in pressed_keys:
        cmd = key_to_cmd[key]
        button_release(cmd)
        pressed_keys.remove(key)

root.bind('<KeyPress>', on_key_press)
root.bind('<KeyRelease>', on_key_release)

def on_closing():
    if ser:
        ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

