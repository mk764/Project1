import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

class Logger:
    def __init__(self, filename):
        self.terminal = __import__('sys').stdout
        self.log = open(filename, "w")
    
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()
    
    def flush(self):
        pass
    
    def close(self):
        self.log.close()

def main():
    # Setup logging
    log_filename = os.path.join(os.path.dirname(__file__), "analysis_output.log")
    sys.stdout = Logger(log_filename)
    
    print("=" * 80)
    print("COFFEE SALES DATA ANALYSIS")
    print("=" * 80)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load data
    df = pd.DataFrame(pd.read_csv("https://raw.githubusercontent.com/KeithGalli/complete-pandas-tutorial/refs/heads/master/warmup-data/coffee.csv"))
    
    print("RAW DATA:")
    print("-" * 80)
    print(df)
    print()
    
    # 1. Number of Latte and Espresso sold on each day
    print("=" * 80)
    print("1. DAILY COFFEE TYPE BREAKDOWN")
    print("=" * 80)
    daily_coffee = df.pivot_table(index='Day', columns='Coffee Type', values='Units Sold', aggfunc='sum')
    print(daily_coffee)
    print()
    
    # 2. Total sales on each day
    print("=" * 80)
    print("2. TOTAL SALES ON EACH DAY")
    print("=" * 80)
    daily_total = df.groupby('Day')['Units Sold'].sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    print(daily_total)
    print()
    
    # 3. Highest and lowest sale day
    print("=" * 80)
    print("3. HIGHEST AND LOWEST SALES DAYS")
    print("=" * 80)
    highest_day = daily_total.idxmax()
    highest_sales = daily_total.max()
    lowest_day = daily_total.idxmin()
    lowest_sales = daily_total.min()
    
    print(f"Highest Sales Day: {highest_day} with {highest_sales} units sold")
    print(f"Lowest Sales Day: {lowest_day} with {lowest_sales} units sold")
    print()
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Coffee Sales Data Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Daily Coffee Type Breakdown
    daily_coffee.plot(kind='bar', ax=axes[0, 0], color=['#8B4513', '#D2691E'])
    axes[0, 0].set_title('Daily Coffee Type Breakdown', fontweight='bold')
    axes[0, 0].set_xlabel('Day')
    axes[0, 0].set_ylabel('Units Sold')
    axes[0, 0].legend(title='Coffee Type')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Plot 2: Total Sales per Day
    daily_total.plot(kind='bar', ax=axes[0, 1], color='#FF6347')
    axes[0, 1].set_title('Total Sales per Day', fontweight='bold')
    axes[0, 1].set_xlabel('Day')
    axes[0, 1].set_ylabel('Total Units Sold')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Plot 3: Line chart for daily trends
    daily_total.plot(kind='line', ax=axes[1, 0], marker='o', color='#4169E1', linewidth=2, markersize=8)
    axes[1, 0].set_title('Daily Sales Trend', fontweight='bold')
    axes[1, 0].set_xlabel('Day')
    axes[1, 0].set_ylabel('Total Units Sold')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Pie chart for coffee type distribution
    total_by_type = df.groupby('Coffee Type')['Units Sold'].sum()
    colors = ['#8B4513', '#D2691E']
    axes[1, 1].pie(total_by_type, labels=total_by_type.index, autopct='%1.1f%%', colors=colors, startangle=90)
    axes[1, 1].set_title('Total Sales by Coffee Type', fontweight='bold')
    
    plt.tight_layout()
    
    # Save the plot
    plot_filename = os.path.join(os.path.dirname(__file__), "coffee_sales_analysis.png")
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved to: {plot_filename}")
    print()
    
    # Summary statistics
    print("=" * 80)
    print("4. SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total Units Sold (All): {df['Units Sold'].sum()}")
    print(f"Average Daily Sales: {daily_total.mean():.2f} units")
    print(f"Standard Deviation: {daily_total.std():.2f} units")
    print(f"Total Espresso Sold: {df[df['Coffee Type'] == 'Espresso']['Units Sold'].sum()}")
    print(f"Total Latte Sold: {df[df['Coffee Type'] == 'Latte']['Units Sold'].sum()}")
    print()
    
    print("=" * 80)
    print(f"✓ Full analysis output saved to: {log_filename}")
    print("=" * 80)
    
    # Close logger
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    print(f"✓ Analysis complete! Log file and visualization saved to: {os.path.dirname(__file__)}")

if __name__ == "__main__":
    import sys
    main()
