import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Load the data
input_file = "dns_timing_results.csv"
df = pd.read_csv(input_file)

custom_colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFB266', '#FF99FF', '#66FFCC']
flierprops = dict(marker='o', color='red', alpha=0.9, markersize=8)

def graph_duration(df, col, exclude_type="NetBios", max_threshold=0.05):
    scaler = MinMaxScaler()
    df[col] = scaler.fit_transform(df[[col]])

    df_filtered = df[(df[col] < max_threshold) & (df['encoding_type'] != exclude_type)]

    fig, ax = plt.subplots(figsize=(20, 12))
    df_filtered.boxplot(
        column=col, 
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
    col_title = col.replace('_', ' ').title()

    ax.set_title(f"Normalized {col_title} per Encoding Type (Filtered < {max_threshold})", fontsize=20, pad=15)
    ax.set_ylabel('Encoding Type', fontsize=16, fontweight='bold', labelpad=10)
    ax.set_xlabel(f"Normalized {col_title}", fontsize=16, fontweight='bold', labelpad=10)
    plt.suptitle("DNS Timing Analysis - Encoding Type Comparison", fontsize=24, fontweight='bold')

    plt.xticks(fontsize=14, fontweight='bold')
    plt.yticks(fontsize=14, fontweight='bold')
    plt.tight_layout()

    # Save the figure
    output_boxplot_image = f"dns_timing_horizontal_{col}.png"
    plt.savefig(output_boxplot_image, bbox_inches='tight')
    print(f"Boxplot saved to {output_boxplot_image}")
    plt.close(fig)

columns_to_graph = ["total_duration", "dns_resolution_duration", "encode_duration"]
for col in columns_to_graph:
    graph_duration(df, col)
