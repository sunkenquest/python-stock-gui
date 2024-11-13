import os
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv

class App:
    def __init__(self):
        load_dotenv()
        
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables!")
                
    def run(self):
        ts = TimeSeries(key=self.api_key, output_format='pandas')
        data, meta_data = ts.get_intraday('AAPL', interval='1min')
        self.save_data_to_csv(data)
        
    def save_data_to_csv(self, data):
        output_dir = os.path.join(os.path.dirname(__file__), '../output')
        os.makedirs(output_dir, exist_ok=True)

        csv_file_path = os.path.join(output_dir, 'stock_data.csv')
        data.to_csv(csv_file_path)
        print(f"Data has been saved to {csv_file_path}")