import plotext as plt
from datetime import datetime, timedelta

def test_graph():
    # Simulate data: 2 points, same price, different dates
    date1 = datetime(2025, 12, 1, 10, 0)
    date2 = datetime(2025, 12, 2, 10, 0)
    
    dates = [date1.strftime("%Y-%m-%d %H:%M"), date2.strftime("%Y-%m-%d %H:%M")]
    values = [100.0, 100.0]
    
    print(f"Dates: {dates}")
    print(f"Values: {values}")
    
    plt.clear_data()
    plt.date_form("Y-m-d H:M")
    plt.plot(dates, values)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Test Graph - Constant Price")
    plt.show()
    
    # Also test with slightly different prices to see if it works normally
    print("\nTest with different prices:")
    values_diff = [100.0, 110.0]
    plt.clear_data()
    plt.date_form("Y-m-d H:M")
    plt.plot(dates, values_diff)
    plt.title("Test Graph - Rising Price")
    plt.build()

if __name__ == "__main__":
    test_graph()
