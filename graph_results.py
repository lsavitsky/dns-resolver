import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Load the data
input_file = "dns_timing_results.csv"
df = pd.read_csv(input_file)

custom_colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFB266', '#FF99FF', '#66FFCC']
flierprops = dict(marker='o', color='red', alpha=0.9, markersize=8)

scaler = MinMaxScaler()
df[['encodePacketStart_norm', 'total_duration_norm']] = scaler.fit_transform(
    df[['encodePacketStart', 'total_duration']]
)

df_filtered = df[df['total_duration_norm'] < 0.05]

fig, ax = plt.subplots(figsize=(20, 12))

df_filtered.boxplot(
    column='total_duration_norm', 
    by='encoding_type', 
    ax=ax, 
    patch_artist=True, 
    vert=False,  # Horizontal boxplot
    grid=False, 
    widths=0.75, 
    flierprops=flierprops
)

for patch, color in zip(ax.artists, custom_colors[:len(ax.artists)]):
    patch.set_facecolor(color)

ax.grid(axis='x', linestyle='--', alpha=0.7) 

ax.set_title('Normalized Total Duration per Encoding Type (Filtered < 0.05)', fontsize=20, pad=15)
ax.set_ylabel('Encoding Type', fontsize=16, fontweight='bold', labelpad=10)
ax.set_xlabel('Normalized Total Duration', fontsize=16, fontweight='bold', labelpad=10)


plt.suptitle("DNS Timing Analysis - Encoding Type Comparison", fontsize=24, fontweight='bold', y=1.02)


plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.tight_layout()
output_boxplot_image = "dns_timing_horizontal_boxplots_filtered.png"
plt.savefig(output_boxplot_image, bbox_inches='tight')
print(f"Boxplots saved to {output_boxplot_image}")
