import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

input_file = "dns_timing_results.csv"
df = pd.read_csv(input_file)

scaler = MinMaxScaler()
df[['encodePacketStart_norm', 'total_duration_norm']] = scaler.fit_transform(
    df[['encodePacketStart', 'total_duration']]
)

df_filtered = df[df['total_duration_norm'] < 0.06]

fig, ax = plt.subplots(figsize=(16, 8))

df_filtered.boxplot(
    column='total_duration_norm', 
    by='encoding_type', 
    ax=ax, 
    patch_artist=True, 
    grid=False
)


ax.set_title('Boxplot of Normalized Total Duration by Encoding Type (Filtered < 0.15)')
ax.set_xlabel('Encoding Type')
ax.set_ylabel('Normalized Total Duration')
plt.suptitle("Boxplots by Encoding Type")

output_boxplot_image = "dns_timing_boxplots_filtered.png"
plt.savefig(output_boxplot_image, bbox_inches='tight')
print(f"Boxplots saved to {output_boxplot_image}")
