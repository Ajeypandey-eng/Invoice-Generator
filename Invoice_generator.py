import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.lib.utils import ImageReader

# ==== Creating main class
class InvoiceGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Generator")
        self.root.geometry("800x850")

        # Creating frame in window
        self.frame = Frame(self.root, bg="white")
        self.frame.place(x=50, y=20, width=700, height=800)

        Label(self.frame, text="Enter Company Details", font=("times new roman", 20, "bold"), bg="white", fg="green").place(x=50, y=10)

        # Company Name
        Label(self.frame, text="Company Name", font=("times new roman", 12, "bold"), bg="white", fg="gray").place(x=50, y=50)
        self.company_name = Entry(self.frame, font=("times new roman", 12), bg="light grey")
        self.company_name.place(x=250, y=50, width=300, height=25)

        # Address
        Label(self.frame, text="Address", font=("times new roman", 12, "bold"), bg="white", fg="gray").place(x=50, y=90)
        self.address = Entry(self.frame, font=("times new roman", 12), bg="light grey")
        self.address.place(x=250, y=90, width=300, height=25)

        # City
        Label(self.frame, text="City", font=("times new roman", 12, "bold"), bg="white", fg="gray").place(x=50, y=130)
        self.city = Entry(self.frame, font=("times new roman", 12), bg="light grey")
        self.city.place(x=250, y=130, width=300, height=25)

        # GST Number
        Label(self.frame, text="GST Number", font=("times new roman", 12, "bold"), bg="white", fg="gray").place(x=50, y=170)
        self.gst = Entry(self.frame, font=("times new roman", 12), bg="light grey")
        self.gst.place(x=250, y=170, width=300, height=25)

        # Date
        Label(self.frame, text="Date", font=("times new roman", 12, "bold"), bg="white", fg="gray").place(x=50, y=210)
        self.date = Entry(self.frame, font=("times new roman", 12), bg="light grey")
        self.date.place(x=250, y=210, width=300, height=25)

        # Contact
        Label(self.frame, text="Contact", font=("times new roman", 12, "bold"), bg="white", fg="gray").place(x=50, y=250)
        self.contact = Entry(self.frame, font=("times new roman", 12), bg="light grey")
        self.contact.place(x=250, y=250, width=300, height=25)

        # Customer Name
        Label(self.frame, text="Customer Name", font=("times new roman", 12, "bold"), bg="white", fg="gray").place(x=50, y=290)
        self.c_name = Entry(self.frame, font=("times new roman", 12), bg="light grey")
        self.c_name.place(x=250, y=290, width=300, height=25)

        # Total Items Input
        Label(self.frame, text="Total Items", font=("times new roman", 12, "bold"), bg="white", fg="gray").place(x=50, y=330)
        self.total_items = Entry(self.frame, font=("times new roman", 12), bg="light grey")
        self.total_items.place(x=250, y=330, width=100, height=25)

        # Button to dynamically generate item fields
        Button(self.frame, text="Add Items", font=("times new roman", 12), command=self.generate_item_fields).place(x=370, y=330)

        # Frame for Items
        self.items_frame = Frame(self.frame, bg="white")
        self.items_frame.place(x=50, y=370, width=600, height=250)

        # Submit Button
        Button(self.frame, text="Generate Invoice", command=self.generate_invoice, font=("times new roman", 14), fg="white", bg="#B00857").place(x=250, y=640, width=180, height=40)

    # Function to dynamically generate item entry fields
    def generate_item_fields(self):
        try:
            total = int(self.total_items.get())
            self.item_entries = []

            # Clear previous fields
            for widget in self.items_frame.winfo_children():
                widget.destroy()

            Label(self.items_frame, text="S.No", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=0)
            Label(self.items_frame, text="Item Name", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=1)
            Label(self.items_frame, text="Quantity", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=2)
            Label(self.items_frame, text="Price", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=3)

            for i in range(total):
                Label(self.items_frame, text=str(i+1), bg="white").grid(row=i+1, column=0)
                item_name = Entry(self.items_frame, bg="light grey")
                item_name.grid(row=i+1, column=1)
                quantity = Entry(self.items_frame, bg="light grey")
                quantity.grid(row=i+1, column=2)
                price = Entry(self.items_frame, bg="light grey")
                price.grid(row=i+1, column=3)
                self.item_entries.append((item_name, quantity, price))
        
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of items.")

    # Function to generate invoice
    def generate_invoice(self):
        try:
            c = canvas.Canvas("Invoice.pdf", pagesize=letter)

            c.setFont("Helvetica-Bold", 20)
            c.drawString(250, 750, "INVOICE")

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 700, f"Company: {self.company_name.get()}")
            c.drawString(50, 680, f"Address: {self.address.get()}, {self.city.get()}")
            c.drawString(400, 700, f"Date: {self.date.get()}")
            c.drawString(400, 680, f"GST No: {self.gst.get()}")

            c.drawString(50, 650, f"Bill To: {self.c_name.get()}")
            c.drawString(50, 630, f"Contact: {self.contact.get()}")

            c.drawString(50, 600, "S.No")
            c.drawString(120, 600, "Item Name")
            c.drawString(280, 600, "Quantity")
            c.drawString(380, 600, "Price")
            c.drawString(480, 600, "Total")

            y = 580
            total_amount = 0
            for i, (item, quantity, price) in enumerate(self.item_entries, start=1):
                q = int(quantity.get())
                p = int(price.get())
                total = q * p
                total_amount += total

                c.drawString(50, y, str(i))
                c.drawString(120, y, item.get())
                c.drawString(280, y, str(q))
                c.drawString(380, y, f"₹{p}")
                c.drawString(480, y, f"₹{total}")
                y -= 20

            c.drawString(380, y-20, "Grand Total:")
            c.drawString(480, y-20, f"₹{total_amount}")
            c.save()

            messagebox.showinfo("Success", "Invoice generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Running the application
if __name__ == "__main__":
    root = Tk()
    obj = InvoiceGenerator(root)
    root.mainloop()
