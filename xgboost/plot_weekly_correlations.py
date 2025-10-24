"""
Script to plot weekly sales correlations from predictions_weekly.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

def plot_weekly_correlations():
    """
    Load weekly predictions and create correlation plots.
    """
    print("Loading weekly predictions...")
    
    # Load the weekly predictions data
    df = pd.read_csv('predictions_weekly.csv')
    
    print(f"Loaded {len(df)} weekly records")
    print(f"Columns: {list(df.columns)}")
    
    # Calculate correlation
    actual = df['actual_sales']
    predicted = df['predicted_sales']
    
    correlation, p_value = pearsonr(actual, predicted)
    r_squared = correlation ** 2
    
    print(f"Weekly Correlation: {correlation:.4f}")
    print(f"Weekly R²: {r_squared:.4f}")
    print(f"P-value: {p_value:.4f}")
    
    # Create plots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Scatter plot with correlation line
    axes[0, 0].scatter(actual, predicted, alpha=0.6, s=50)
    
    # Add correlation line
    z = np.polyfit(actual, predicted, 1)
    p = np.poly1d(z)
    axes[0, 0].plot(actual, p(actual), "r--", alpha=0.8, linewidth=2)
    
    axes[0, 0].set_xlabel('Actual Weekly Sales')
    axes[0, 0].set_ylabel('Predicted Weekly Sales')
    axes[0, 0].set_title(f'Weekly Sales Correlation\nr = {correlation:.4f}, R² = {r_squared:.4f}')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Residuals plot
    residuals = actual - predicted
    axes[0, 1].scatter(predicted, residuals, alpha=0.6, s=50)
    axes[0, 1].axhline(y=0, color='r', linestyle='--', alpha=0.8)
    axes[0, 1].set_xlabel('Predicted Weekly Sales')
    axes[0, 1].set_ylabel('Residuals (Actual - Predicted)')
    axes[0, 1].set_title('Weekly Residuals Plot')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Time series comparison
    axes[1, 0].plot(df['week'], actual, label='Actual', alpha=0.8, linewidth=2)
    axes[1, 0].plot(df['week'], predicted, label='Predicted', alpha=0.8, linewidth=2)
    axes[1, 0].set_xlabel('Week')
    axes[1, 0].set_ylabel('Weekly Sales')
    axes[1, 0].set_title('Weekly Sales: Actual vs Predicted Over Time')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Distribution comparison
    axes[1, 1].hist(actual, alpha=0.6, label='Actual', bins=30, density=True)
    axes[1, 1].hist(predicted, alpha=0.6, label='Predicted', bins=30, density=True)
    axes[1, 1].set_xlabel('Weekly Sales')
    axes[1, 1].set_ylabel('Density')
    axes[1, 1].set_title('Distribution of Weekly Sales')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('weekly_correlations_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print summary statistics
    print("\n" + "="*50)
    print("WEEKLY SALES CORRELATION ANALYSIS")
    print("="*50)
    print(f"Number of weeks: {len(df)}")
    print(f"Correlation coefficient: {correlation:.4f}")
    print(f"R-squared: {r_squared:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Mean actual sales: {actual.mean():.2f}")
    print(f"Mean predicted sales: {predicted.mean():.2f}")
    print(f"Std actual sales: {actual.std():.2f}")
    print(f"Std predicted sales: {predicted.std():.2f}")
    print(f"RMSE: {np.sqrt(np.mean((actual - predicted)**2)):.2f}")
    print(f"MAE: {np.mean(np.abs(actual - predicted)):.2f}")
    
    return correlation, r_squared

if __name__ == "__main__":
    plot_weekly_correlations()
