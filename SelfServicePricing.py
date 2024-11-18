import tkinter as tk
from tkinter import messagebox, Canvas, OptionMenu, Toplevel, Entry, Button, Label, StringVar
import math
import openai
from openai import OpenAI
import psycopg2
from psycopg2 import sql





# Consultant Type Global Variables
W2_VALUE = 1.27
C2C_VALUE = 1.1

# VMS Fee Global Variables
NO_VMS_VALUE = 0
ARIBA_VALUE = 6.75
VENDORPASS_VALUE = 1.95
FIELDGLASS_VALUE = 2.65
ORACLE_VALUE = 1.0
VMS_VALUE = 0.0
BEELINE_VALUE = 2.5
HAYS_VALUE = 1.2
PRIORITY_VALUE = 1.55


class CircularSlider(Canvas):
    def __init__(self, parent, width=100, height=100, min_value=0, max_value=100, start_angle=180, extent=359.9, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.start_angle = start_angle
        self.extent = extent
        self.value = tk.DoubleVar()
        self.value.set((min_value + max_value) / 2)
        self.bind("<Button-1>", self.set_value)
        self.bind("<B1-Motion>", self.set_value)
        self.animation_id = None
        self.target_value = self.value.get()
        self.current_value = self.value.get()
        self.step = 0.5  # Animation step value
        self.draw_slider()

    def draw_slider(self):
        self.delete("slider")
        angle_extent = self.extent * (self.current_value - self.min_value) / (self.max_value - self.min_value)
        self.create_arc(10, 10, self.width - 10, self.height - 10, start=self.start_angle, extent=-angle_extent, style="arc", width=4, outline=self.get_color(), tags="slider")
        angle = self.start_angle + angle_extent
        x = self.width / 2 + (self.width / 2 - 9) * math.cos(math.radians(angle))
        y = self.height / 2 + (self.height / 2 - 9) * math.sin(math.radians(angle))
        self.create_oval(x + 5, y + 5, x - 5, y - 5, fill="#fff", outline="#fff", tags="slider")
        self.create_text(self.width / 2, self.height / 2, text=f"{self.current_value:.0f}%", font=("Arial", 12, "bold"), tags="slider")

    def get_color(self):
        if self.current_value < 20:
            return "red"
        else:
            return "white"

    def set_value(self, event):
        x, y = event.x - self.width / 2, event.y - self.height / 2
        angle = (math.degrees(math.atan2(y, x)) - self.start_angle) % 360
        if angle <= self.extent:
            value = self.min_value + (self.max_value - self.min_value) * angle / self.extent
            self.target_value = value
            self.animate_slider()
    def get_value(self):
        return self.target_value
    def update_value(self, new_value):
        if self.min_value <= new_value <= self.max_value:
            self.target_value = new_value
            self.animate_slider()

    def animate_slider(self):
        if self.animation_id:
            self.after_cancel(self.animation_id)
        if abs(self.current_value - self.target_value) > self.step:
            if self.current_value < self.target_value:
                self.current_value += self.step
            else:
                self.current_value -= self.step
            self.draw_slider()
            self.animation_id = self.after(10, self.animate_slider)
        else:
            self.current_value = self.target_value
            self.draw_slider()

def show_margin_calculator():
    margin_frame.pack(fill='both', expand=True)
    other_frame.pack_forget()

def show_other_calculator():
    other_frame.pack(fill='both', expand=True)
    margin_frame.pack_forget()

def show_admin_panel():
    password_prompt = Toplevel(root)
    password_prompt.title("Admin Login")
    password_prompt.geometry("300x150")

    def check_password():
        if password_entry.get() == "admin_password":
            password_prompt.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Error", "Incorrect password")

    Label(password_prompt, text="Enter Admin Password:", font=label_font).pack(pady=10)
    password_entry = Entry(password_prompt, show="*", font=entry_font)
    password_entry.pack(pady=5)
    Button(password_prompt, text="Submit", command=check_password, font=button_font).pack(pady=10)

def open_admin_panel():
    admin_panel = Toplevel(root)
    admin_panel.title("Admin Panel")
    admin_panel.geometry("600x900")

    def update_values():
        global W2_VALUE, C2C_VALUE, ARIBA_VALUE, VENDORPASS_VALUE, FIELDGLASS_VALUE, ORACLE_VALUE, VMS_VALUE, BEELINE_VALUE, HAYS_VALUE, PRIORITY_VALUE
        try:
            W2_VALUE = float(w2_entry.get())
            C2C_VALUE = float(c2c_entry.get())
            ARIBA_VALUE = float(ariba_entry.get())
            VENDORPASS_VALUE = float(vendorpass_entry.get())
            FIELDGLASS_VALUE = float(fieldglass_entry.get())
            ORACLE_VALUE = float(oracle_entry.get())
            VMS_VALUE = float(vms_entry.get())
            BEELINE_VALUE = float(beeline_entry.get())
            HAYS_VALUE = float(hays_entry.get())
            PRIORITY_VALUE = float(priority_entry.get())
            messagebox.showinfo("Success", "Values updated successfully!")
            admin_panel.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    Label(admin_panel, text="W2 Value:", font=label_font).pack(pady=5)
    w2_entry = Entry(admin_panel, font=entry_font)
    w2_entry.pack(pady=5)
    w2_entry.insert(0, str(W2_VALUE))

    Label(admin_panel, text="C2C Value:", font=label_font).pack(pady=5)
    c2c_entry = Entry(admin_panel, font=entry_font)
    c2c_entry.pack(pady=5)
    c2c_entry.insert(0, str(C2C_VALUE))

    Label(admin_panel, text="Aetna Value:", font=label_font).pack(pady=5)
    ariba_entry = Entry(admin_panel, font=entry_font)
    ariba_entry.pack(pady=5)
    ariba_entry.insert(0, str(ARIBA_VALUE))

    Label(admin_panel, text="Accenture Value:", font=label_font).pack(pady=5)
    vendorpass_entry = Entry(admin_panel, font=entry_font)
    vendorpass_entry.pack(pady=5)
    vendorpass_entry.insert(0, str(VENDORPASS_VALUE))

    Label(admin_panel, text="BCBSNC Value:", font=label_font).pack(pady=5)
    fieldglass_entry = Entry(admin_panel, font=entry_font)
    fieldglass_entry.pack(pady=5)
    fieldglass_entry.insert(0, str(FIELDGLASS_VALUE))

    Label(admin_panel, text="BCBS MI Value:", font=label_font).pack(pady=5)
    oracle_entry = Entry(admin_panel, font=entry_font)
    oracle_entry.pack(pady=5) 
    oracle_entry.insert(0, str(ORACLE_VALUE))

    Label(admin_panel, text="BCI Value:", font=label_font).pack(pady=5)
    vms_entry = Entry(admin_panel, font=entry_font)
    vms_entry.pack(pady=5)
    vms_entry.insert(0, str(VMS_VALUE))

    Label(admin_panel, text="Centene Value:", font=label_font).pack(pady=5)
    beeline_entry = Entry(admin_panel, font=entry_font)
    beeline_entry.pack(pady=5)
    beeline_entry.insert(0, str(BEELINE_VALUE))

    Label(admin_panel, text="Cognizant Value:", font=label_font).pack(pady=5)
    hays_entry = Entry(admin_panel, font=entry_font)
    hays_entry.pack(pady=5)
    hays_entry.insert(0, str(HAYS_VALUE))

    Label(admin_panel, text="Spectrum Value:", font=label_font).pack(pady=5)
    priority_entry = Entry(admin_panel, font=entry_font)
    priority_entry.pack(pady=5)
    priority_entry.insert(0, str(PRIORITY_VALUE))

    Button(admin_panel, text="Update Values", command=update_values, font=button_font).pack(pady=20)

def calculate_desired_margin():
    try:
        vms_fee_value = vms_fee_var.get()
        pay_rate = pay_rate_entry2.get()
        bill_rate = bill_rate_entry2.get()
        referral = float(referral_entry2.get())
        desired_margin = round(float(CircularSlider.get_value(desired_margin_slider)))
        consultant_type = consultant_type_var.get()

        vms_fee_map = {
            "No VMS Fee": 0,
            "Aetna": ARIBA_VALUE,
            "Accenture": VENDORPASS_VALUE,
            "BCBSNC": FIELDGLASS_VALUE,
            "BCBS MI": ORACLE_VALUE,
            "BCI": VMS_VALUE,
            "Centene": BEELINE_VALUE,
            "Cognizant": HAYS_VALUE,
            "Spectrum": PRIORITY_VALUE
        }
        vms_fee = vms_fee_map[vms_fee_value]

        if desired_margin >= 100:
            messagebox.showerror("Error", "Desired margin must be less than 100%.")
            return

        if not pay_rate and not bill_rate:
            messagebox.showerror("Error", "Please enter either Pay Rate or Bill Rate.")
            return

        if pay_rate and not bill_rate:
            pay_rate = float(pay_rate)
        if bill_rate and not pay_rate:
            bill_rate = float(bill_rate)

        if consultant_type == "W2":
            total_cost = lambda pay: float(pay) * W2_VALUE + referral
        elif consultant_type == "C2C":
            total_cost = lambda pay: float(pay) * C2C_VALUE + referral
        else:
            messagebox.showerror("Error", "Please select a valid consultant type.")
            return

        if pay_rate and not bill_rate:
            revised_bill = (total_cost(pay_rate)) / (1-((desired_margin)/100))
            print(vms_fee)
            print(desired_margin)
            bill_rate_entry2.delete(0, tk.END)  
            bill_rate_entry2.insert(0, f"${revised_bill:.2f}")  # Display required bill rate
            hourly_spread = revised_bill - total_cost(pay_rate)
            vms_perc = revised_bill*(vms_fee/100)
            revised_margin_value = revised_bill - float(total_cost(pay_rate)) - float(vms_perc)
            margin_inclusive_vms_value = (revised_margin_value/revised_bill) *100
            revised_bill_v2 = revised_bill - ((revised_bill*vms_fee)/100)
            revised_bill_label2.config(text=f"Revised Bill Rate: ${revised_bill_v2:.2f}")
            total_cost_label2.config(text=f"Total Cost: ${total_cost(pay_rate):.2f}")
            hourly_spread_label2.config(text=f"Hourly Spread: ${hourly_spread:.2f}")
            vms_fee_perc.config(text=f"VMS Fee: {vms_perc:.2f}%")
            revised_margin.config(text=f"Revised Margin: ${revised_margin_value:.2f}")
            margin_inclusive_vms.config(text=f"Margin inclusive of VMS %: {margin_inclusive_vms_value:.2f}%")
        elif bill_rate and not pay_rate:
            revised_bill = bill_rate * (1 - vms_fee/ 100)
            print(vms_fee)
            #bill rate= (payrate+ (pay_rate * (W2_VALUE if consultant_type == 'W2' else C2C_VALUE))/margin
            # pay_rate = (revised_bill * (1-((desired_margin/100)))) / ((W2_VALUE if consultant_type == 'W2' else C2C_VALUE))
            pay_rate = ((bill_rate * (1 - desired_margin/ 100))- referral)/ ((W2_VALUE if consultant_type == 'W2' else C2C_VALUE))
            # print(W2_VALUE)
            # print(desired_margin)
            # print(bill_rate)
            # print(referral)

            # (revised_bill - referral) / (W2_VALUE if consultant_type == 'W2' else C2C_VALUE)}
            pay_rate_entry2.delete(0, tk.END)  # Clear previous pay rate value
            pay_rate_entry2.insert(0, f"${pay_rate:.2f}")
            hourly_spread = bill_rate    - pay_rate
            vms_perc = bill_rate*(vms_fee/100)
            revised_margin_value = bill_rate - float(total_cost(pay_rate)) - float(vms_perc)
            margin_inclusive_vms_value = (revised_margin_value/bill_rate) *100
            revised_bill_label2.config(text=f"Revised Bill Rate: ${revised_bill:.2f}")
            total_cost_label2.config(text=f"Total Cost: ${total_cost(pay_rate):.2f}")
            hourly_spread_label2.config(text=f"Hourly Spread: ${revised_margin_value:.2f}")
            vms_fee_perc.config(text=f"VMS Fee: {vms_perc:.2f}%")
            revised_margin.config(text=f"Revised Margin: ${revised_margin_value:.2f}")
            margin_inclusive_vms.config(text=f"Margin inclusive of VMS %: {margin_inclusive_vms_value:.2f}%")
        elif pay_rate and bill_rate:
            revised_bill = float(bill_rate) - (float(bill_rate) * (vms_fee / 100))
            hourly_spread = float(bill_rate) - total_cost(float(pay_rate))
            margin = (hourly_spread / float(bill_rate)) * 100
            desired_margin_slider.update_value(margin)
            vms_perc = float(bill_rate)*(vms_fee/100)
            revised_margin_value = float(bill_rate) - float(total_cost(pay_rate)) - float(vms_perc)
            margin_inclusive_vms_value = (revised_margin_value/(float(bill_rate))) *100
            revised_bill_label2.config(text=f"Revised Bill Rate: ${revised_bill:.2f}")
            total_cost_label2.config(text=f"Total Cost: ${total_cost(pay_rate):.2f}")
            hourly_spread_label2.config(text=f"Hourly Spread: ${revised_margin_value:.2f}")
            vms_fee_perc.config(text=f"VMS Fee: {vms_perc:.2f}%")
            revised_margin.config(text=f"Revised Margin: ${revised_margin_value:.2f}")
            margin_inclusive_vms.config(text=f"Margin inclusive of VMS %: {margin_inclusive_vms_value:.2f}%")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def reset_fields():
    pay_rate_entry2.delete(0, tk.END)
    bill_rate_entry2.delete(0, tk.END)
    referral_entry2.delete(0, tk.END)
    desired_margin_slider.update_value(50)  # Reset to middle value
    revised_bill_label2.config(text="Revised Bill Rate: N/A")
    total_cost_label2.config(text="Total Cost: N/A")
    hourly_spread_label2.config(text="Hourly Spread: N/A")
    vms_fee_perc.config(text="VMS Fee %: N/A")
    revised_margin.config(text="Revised Margin $: N/A")
    margin_inclusive_vms.config(text="Margin inclusive of VMS %: N/A")

def send_message_to_openai(message):
    response = openai.Completion.create(
        engine="asst_o3ALvz7hpk1acenc5W6XaMnc",
        prompt=message,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def handle_chat(event=None):
    user_message = user_input.get()
    if user_message:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"You: {user_message}\n")
        user_input.delete(0, tk.END)
        response = send_message_to_openai(user_message)
        chat_log.insert(tk.END, f"Bot: {response}\n")
        chat_log.config(state=tk.DISABLED)
        chat_log.yview(tk.END)

root = tk.Tk()
root.title("Margin Calculator")
root.geometry("600x800")
# root.configure(background="white")

label_font = ("Arial", 12)
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")
result_font = ("Arial", 12, "bold")

top_frame = tk.Frame(root)
top_frame.pack(pady=10)
# top_frame.configure(background="white")


other_button = tk.Button(top_frame, text="Margin Calculator", command=show_other_calculator, font=button_font)
other_button.grid(row=0, column=1, padx=10)

admin_button = tk.Button(top_frame, text="Admin Panel", command=show_admin_panel, font=button_font)
admin_button.grid(row=0, column=2, padx=10)

margin_frame = tk.Frame(root)

input_frame = tk.Frame(margin_frame)
input_frame.pack(pady=20)

# Chatbot Frame
chatbot_frame = tk.Frame(margin_frame)
chatbot_frame.pack(pady=20)

chat_log = tk.Text(chatbot_frame, state=tk.DISABLED, width=60, height=15, wrap=tk.WORD)
chat_log.pack(padx=10, pady=5)

user_input = tk.Entry(chatbot_frame, font=entry_font, width=50)
user_input.pack(padx=10, pady=5, side=tk.LEFT)
user_input.bind("<Return>", handle_chat)

send_button = tk.Button(chatbot_frame, text="Send", command=handle_chat, font=button_font)
send_button.pack(padx=10, pady=5, side=tk.LEFT)

other_frame = tk.Frame(root)

input_frame2 = tk.Frame(other_frame)
input_frame2.pack(pady=20)

tk.Label(input_frame2, text="Consultant Type", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky="e")
consultant_type_var = tk.StringVar()
consultant_type_menu = tk.OptionMenu(input_frame2, consultant_type_var, "W2", "C2C")
consultant_type_menu.config(font=entry_font)
consultant_type_menu.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame2, text="Pay Rate ($):", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky="e")
pay_rate_entry2 = tk.Entry(input_frame2, font=entry_font)
pay_rate_entry2.grid(row=1, column=1, padx=10, pady=5)

tk.Label(input_frame2, text="Bill Rate ($):", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky="e")
bill_rate_entry2 = tk.Entry(input_frame2, font=entry_font)
bill_rate_entry2.grid(row=2, column=1, padx=10, pady=5)

tk.Label(input_frame2, text="Referral ($):", font=label_font).grid(row=3, column=0, padx=10, pady=5, sticky="e")
referral_entry2 = tk.Entry(input_frame2, font=entry_font)
referral_entry2.grid(row=3, column=1, padx=10, pady=5)

tk.Label(input_frame2, text="VMS Fee (%):", font=label_font).grid(row=4, column=0, padx=10, pady=5, sticky="e")
vms_fee_var = tk.StringVar()
vms_fee_options = ["No VMS Fee","Aetna", "Accenture", "BCBSNC", "BCBS MI", "BCI", "Centene", "Cognizant", "Spectrum"]
vms_fee_menu = tk.OptionMenu(input_frame2, vms_fee_var, *vms_fee_options)
vms_fee_menu.config(font=entry_font)
vms_fee_menu.grid(row=4, column=1, padx=10, pady=5)

tk.Label(input_frame2, text="Desired Margin (%):", font=label_font).grid(row=5, column=0, padx=10, pady=5, sticky="e")
desired_margin_slider = CircularSlider(input_frame2, width=100, height=100)
desired_margin_slider.grid(row=5, column=1, padx=10, pady=5)

revised_bill_label2 = tk.Label(input_frame2, text="Revised Bill Rate: N/A", font=result_font)
revised_bill_label2.grid(row=6, column=1, padx=10, pady=5)

total_cost_label2 = tk.Label(input_frame2, text="Total Cost: N/A", font=result_font)
total_cost_label2.grid(row=7, column=1, padx=10, pady=5)

hourly_spread_label2 = tk.Label(input_frame2, text="Hourly Spread: N/A", font=result_font)
hourly_spread_label2.grid(row=8, column=1, padx=10, pady=5)

vms_fee_perc = tk.Label(input_frame2, text="VMS Fee %: N/A", font=result_font)
vms_fee_perc.grid(row=9, column=1, padx=10, pady=5)

revised_margin = tk.Label(input_frame2, text="Revised Margin $: N/A", font=result_font)
revised_margin.grid(row=10, column=1, padx=10, pady=5)

margin_inclusive_vms = tk.Label(input_frame2, text="Margin inclusive of VMS %: N/A", font=result_font)
margin_inclusive_vms.grid(row=11, column=1, padx=10, pady=5)

calculate_desired_button = tk.Button(other_frame, text="Calculate", command=calculate_desired_margin, font=button_font)
calculate_desired_button.pack(pady=3)

reset_button = tk.Button(other_frame, text="Reset", command=reset_fields, font=button_font)
reset_button.pack(pady=8)
result_frame2 = tk.Frame(other_frame)
result_frame2.pack(padx=5)

# Admin Frame
admin_frame = tk.Frame(root)
admin_password_frame = tk.Frame(root)
admin_password_var = tk.StringVar()

def show_admin_panel():
    admin_password_frame.pack(fill='both', expand=True)
    margin_frame.pack_forget()
    other_frame.pack_forget()

def check_password():
    password = admin_password_var.get()
    if password == "admin123":  # Change this to your desired admin password
        admin_password_frame.pack_forget()
        admin_frame.pack(fill='both', expand=True)
    else:
        messagebox.showerror("Error", "Incorrect Password")

tk.Label(admin_password_frame, text="Enter Admin Password:", font=label_font).pack(pady=20)
tk.Entry(admin_password_frame, textvariable=admin_password_var, show="*", font=entry_font).pack(pady=5)
tk.Button(admin_password_frame, text="Submit", command=check_password, font=button_font).pack(pady=5)

def update_values():
    global W2_VALUE, C2C_VALUE, ARIBA_VALUE, VENDORPASS_VALUE, FIELDGLASS_VALUE, ORACLE_VALUE, VMS_VALUE, BEELINE_VALUE, HAYS_VALUE, PRIORITY_VALUE
    try:
        W2_VALUE = float(w2_value_entry.get())
        C2C_VALUE = float(c2c_value_entry.get())
        ARIBA_VALUE = float(ariba_value_entry.get())
        VENDORPASS_VALUE = float(vendorpass_value_entry.get())
        FIELDGLASS_VALUE = float(fieldglass_value_entry.get())
        ORACLE_VALUE = float(oracle_value_entry.get())
        VMS_VALUE = float(vms_value_entry.get())
        BEELINE_VALUE = float(beeline_value_entry.get())
        HAYS_VALUE = float(hays_value_entry.get())
        PRIORITY_VALUE = float(priority_value_entry.get())
        messagebox.showinfo("Success", "Values updated successfully")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

tk.Label(admin_frame, text="Update Values", font=("Arial", 16)).pack(pady=20)

value_frame = tk.Frame(admin_frame)
value_frame.pack(pady=10)

tk.Label(value_frame, text="W2 Value:", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky="e")
w2_value_entry = tk.Entry(value_frame, font=entry_font)
w2_value_entry.grid(row=0, column=1, padx=10, pady=5)
w2_value_entry.insert(0, W2_VALUE)

tk.Label(value_frame, text="C2C Value:", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky="e")
c2c_value_entry = tk.Entry(value_frame, font=entry_font)
c2c_value_entry.grid(row=1, column=1, padx=10, pady=5)
c2c_value_entry.insert(0, C2C_VALUE)

tk.Label(value_frame, text="Aetna Value:", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky="e")
ariba_value_entry = tk.Entry(value_frame, font=entry_font)
ariba_value_entry.grid(row=2, column=1, padx=10, pady=5)
ariba_value_entry.insert(0, ARIBA_VALUE)

tk.Label(value_frame, text="Accenture Value:", font=label_font).grid(row=3, column=0, padx=10, pady=5, sticky="e")
vendorpass_value_entry = tk.Entry(value_frame, font=entry_font)
vendorpass_value_entry.grid(row=3, column=1, padx=10, pady=5)
vendorpass_value_entry.insert(0, VENDORPASS_VALUE)

tk.Label(value_frame, text="BCBSNC Value:", font=label_font).grid(row=4, column=0, padx=10, pady=5, sticky="e")
fieldglass_value_entry = tk.Entry(value_frame, font=entry_font)
fieldglass_value_entry.grid(row=4, column=1, padx=10, pady=5)
fieldglass_value_entry.insert(0, FIELDGLASS_VALUE)

tk.Label(value_frame, text="BCBS MI Value:", font=label_font).grid(row=5, column=0, padx=10, pady=5, sticky="e")
oracle_value_entry = tk.Entry(value_frame, font=entry_font)
oracle_value_entry.grid(row=5, column=1, padx=10, pady=5)
oracle_value_entry.insert(0, ORACLE_VALUE)

tk.Label(value_frame, text="BCI Value:", font=label_font).grid(row=6, column=0, padx=10, pady=5, sticky="e")
vms_value_entry = tk.Entry(value_frame, font=entry_font)
vms_value_entry.grid(row=6, column=1, padx=10, pady=5)
vms_value_entry.insert(0, VMS_VALUE)

tk.Label(value_frame, text="Centene Value:", font=label_font).grid(row=7, column=0, padx=10, pady=5, sticky="e")
beeline_value_entry = tk.Entry(value_frame, font=entry_font)
beeline_value_entry.grid(row=7, column=1, padx=10, pady=5)
beeline_value_entry.insert(0, BEELINE_VALUE)

tk.Label(value_frame, text="Cognizant Value:", font=label_font).grid(row=8, column=0, padx=10, pady=5, sticky="e")
hays_value_entry = tk.Entry(value_frame, font=entry_font)
hays_value_entry.grid(row=8, column=1, padx=10, pady=5)
hays_value_entry.insert(0, HAYS_VALUE)

tk.Label(value_frame, text="Spectrum Value:", font=label_font).grid(row=9, column=0, padx=10, pady=5, sticky="e")
priority_value_entry = tk.Entry(value_frame, font=entry_font)
priority_value_entry.grid(row=9, column=1, padx=10, pady=5)
priority_value_entry.insert(0, PRIORITY_VALUE)

tk.Button(admin_frame, text="Update Values", command=update_values, font=button_font).pack(pady=10)

show_other_calculator()

root.mainloop()





