import os
import customtkinter as ctk
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from utils.utils import Utils 

class App:
    def __init__(self):
        # load_dotenv()
        
        # self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        # if not self.api_key:
        #     raise ValueError("API_KEY not found in environment variables!")
        
        # ts = TimeSeries(key=self.api_key, output_format='pandas')
        # self.data, self.meta_data = ts.get_weekly('AAPL')

        # self.data.columns = [
        #     col.split(". ")[1] if ". " in col else col for col in self.data.columns
        # ]
        
        # self.data.index = pd.to_datetime(self.data.index)
        # self.data["year"] = self.data.index.year
        
        # self.selected_data_type = "open"
        # self.selected_year = self.data["year"].iloc[0]
        # self.overlay_mode = False  

        # self.utils = Utils(self)
        
        csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'stock_data.csv')
        if not os.path.exists(csv_file_path):
            raise ValueError(f"CSV file not found at {csv_file_path}")

        # Read the stock data from the CSV file
        self.data = pd.read_csv(csv_file_path, parse_dates=['date'], index_col='date')
        
        # Make sure the data has the correct column names and structure
        self.data.columns = [col.strip().lower() for col in self.data.columns]  # Normalize column names to lowercase
        self.data["year"] = self.data.index.year

        self.selected_data_type = "open"
        self.selected_year = self.data["year"].iloc[0]
        self.overlay_mode = False

        self.utils = Utils(self)
    def run(self):
        self.setup_gui()
    
    def setup_gui(self):
        self.root = ctk.CTk()
        self.root.title("Stock Data Graph")
        self.root.geometry("700x600")
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        
        unique_years = sorted(self.data['year'].unique())
        self.year_var = ctk.StringVar(value=str(self.selected_year))
        self.year_dropdown = ctk.CTkComboBox(
            self.root, variable=self.year_var, values=[str(year) for year in unique_years],
            command=self.update_year_selection
        )
        self.year_dropdown.pack(pady=10)
        
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)
        
        for data_type in ["open", "high", "low", "close", "volume"]:
            button = ctk.CTkButton(
                button_frame, text=data_type.capitalize(),
                command=lambda dt=data_type: self.update_data_type(dt)
            )
            button.pack(side=ctk.LEFT, padx=5)
        
        overlay_button = ctk.CTkButton(self.root, text="Overlay All", command=self.toggle_overlay_mode)
        overlay_button.pack(pady=5)

        self.update_plot()
        self.root.mainloop()

    def update_year_selection(self, selected_year):
        """Update selected year and refresh the plot."""
        self.selected_year = int(selected_year)
        self.update_plot()

    def update_data_type(self, data_type):
        """Update selected data type and refresh the plot."""
        self.selected_data_type = data_type
        self.overlay_mode = False
        self.update_plot()

    def toggle_overlay_mode(self):
        """Toggle overlay mode to plot all data types."""
        self.overlay_mode = not self.overlay_mode
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        
        year_data = self.data[self.data["year"] == self.selected_year]

        if self.overlay_mode:
            self.overlay_plot(year_data)
        else:
            self.ax.plot(year_data.index, year_data[self.selected_data_type], label=self.selected_data_type.capitalize(), color="blue")
            self.ax.set_ylabel(self.selected_data_type.capitalize())
            self.ax.set_title(f"{self.selected_data_type.capitalize()} over Time in {self.selected_year}")

        self.ax.set_xlabel("Time")
        self.ax.legend()
        self.canvas.draw()

    def overlay_plot(self, year_data):
        """Plot all data types (open, high, low, close, volume) with different colors."""
        colors = ["blue", "green", "red", "orange", "purple"]
        data_types = ["open", "high", "low", "close"]
        
        for color, data_type in zip(colors, data_types):
            self.ax.plot(year_data.index, year_data[data_type], label=data_type.capitalize(), color=color)
        
        self.ax.set_ylabel("Values")
        self.ax.set_title(f"Overlay of All Data Types over Time in {self.selected_year}")

    def save_data_to_csv(self):
        output_dir = os.path.join(os.path.dirname(__file__), '../output')
        os.makedirs(output_dir, exist_ok=True)

        csv_file_path = os.path.join(output_dir, 'stock_data.csv')
        self.data.to_csv(csv_file_path)
        print(f"Data has been saved to {csv_file_path}")
        
if __name__ == "__main__":
    app = App()
    app.run()
