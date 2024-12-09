import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Load the data
input_file = "dns_timing_results.csv"
df = pd.read_csv(input_file)

# Normalize encodePacketStart and total_duration
scaler = MinMaxScaler()
df[['encodePacketStart_norm', 'total_duration_norm']] = scaler.fit_transform(
    df[['encodePacketStart', 'total_duration']]
)

# Plotting setup
plt.figure(figsize=(14, 8))

# Grouping and plotting
for encoding_type, group in df.groupby('encoding_type'):
    plt.plot(
        group['encodePacketStart_norm'], 
        group['total_duration_norm'], 
        marker='o', 
        label=encoding_type
    )
    break

# Plot configurations
plt.title('Normalized Total Duration vs Encode Packet Start (Split by Encode Type)')
plt.xlabel('Normalized Encode Packet Start')
plt.ylabel('Normalized Total Duration')
plt.legend(title='Encode Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='both', linestyle='--', alpha=0.7)

# Save and display the plot
output_image = "dns_timing_normalized_plot.png"
plt.savefig(output_image, bbox_inches='tight')
print(f"Plot saved to {output_image}")
plt.show()
