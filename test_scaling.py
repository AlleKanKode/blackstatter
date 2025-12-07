import plotext as plt
from datetime import datetime

def test_scaling():
    dates = ["2025-12-01 10:00", "2025-12-02 10:00"]
    values = [6990.0, 6999.0]
    
    print("--- Default Scaling ---")
    plt.clear_data()
    plt.date_form("Y-m-d H:M")
    plt.plot(dates, values)
    plt.title("Default Scaling (6990 vs 6999)")
    plt.show()
    
    print("\n--- Fixed Scaling (Start from 0) ---")
    plt.clear_data()
    plt.date_form("Y-m-d H:M")
    plt.plot(dates, values)
    plt.ylim(0, max(values) * 1.1)
    plt.title("Fixed Scaling (0 to Max)")
    plt.show()

if __name__ == "__main__":
    test_scaling()
