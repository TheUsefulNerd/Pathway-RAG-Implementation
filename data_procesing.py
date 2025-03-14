import time
import os
import pathway as pw
from config import DATA_PATH, OUTPUT_PATH

class FinanceSchema(pw.Schema):
    timestamp: str
    Open: float
    High: float
    Low: float
    Close: float
    Volume: int

def wait_for_file(filepath, timeout=60):
    """Wait until the CSV file is available."""
    start_time = time.time()
    while not os.path.exists(filepath) or os.stat(filepath).st_size == 0:
        if time.time() - start_time > timeout:
            print(f"❌ Timeout: CSV file {filepath} not found.")
            return False
        time.sleep(2)
    print(f"✅ File detected: {filepath}")
    return True

def process_streaming_data():
    """Read and process stock data using Pathway."""
    print("🚀 Starting Pathway data processing...")

    try:
        print(f"🔍 Reading data from: {DATA_PATH}")
        finance_data = pw.io.csv.read(DATA_PATH, mode="static", schema=FinanceSchema)

        # Aggregating stock data
        aggregated_data = finance_data.reduce(
            avg_close=pw.reducers.avg(finance_data.Close),
            highest_price=pw.reducers.max(finance_data.High),
            lowest_price=pw.reducers.min(finance_data.Low),
            total_volume=pw.reducers.sum(finance_data.Volume)
        )

        # DEBUG: Print results before writing
        print("✅ Aggregated Data Preview:")
        pw.debug.compute_and_print(aggregated_data)  # This will print in terminal

        # Save to CSV
        df = pw.debug.table_to_pandas(aggregated_data)
        df.to_csv(OUTPUT_PATH, index=False)


        # Run Pathway engine
        pw.run()
        print(f"✅ Processed data saved to {OUTPUT_PATH}")

    except Exception as e:
        print(f"❌ Error during Pathway processing: {e}")

def run_streaming():
    """Run stock data processing after ensuring file exists."""
    print("🔄 Checking if stock data is available...")

    if not wait_for_file(DATA_PATH, timeout=60):
        return

    print("✅ Stock data confirmed. Starting processing...")
    process_streaming_data()