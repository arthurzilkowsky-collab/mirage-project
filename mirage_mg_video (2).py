# mirage_mg_video.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def mirror_group(sequence):
    """Parses sequence into repeat-bounded mirror groups."""
    if not sequence:
        return []
    groups = []
    current = sequence[0]
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            groups.append(current)
            current = sequence[i]
        else:
            current += sequence[i]
    if current:
        groups.append(current)
    return groups

def generate_mg_video(sequence, filename="mirage_mg_animation.mp4", fps=2):
    groups = mirror_group(sequence)
    
    fig, ax = plt.subplots(figsize=(10, 3))
    fig.patch.set_facecolor('#0b0f19')
    ax.set_facecolor('#0b0f19')
    
    max_len = max(len(g) for g in groups) if groups else 1
    ax.set_xlim(-1, len(groups))
    ax.set_ylim(-1, max_len + 2)
    ax.axis('off')
    
    # Color mapping for bases / characters
    color_map = {
        'A': '#ff5555', # Red/Coral
        'T': '#55ffff', # Cyan
        'G': '#55ff55', # Green
        'C': '#ff55ff'  # Purple/Orchid
    }
    
    title = ax.text(0.5, 0.9, "", transform=ax.transAxes, color="white", 
                    fontsize=14, ha="center", fontfamily="monospace", weight="bold")
    
    rects = []
    texts = []

    def init():
        title.set_text(f"MIRAGE Sequence: {sequence}")
        return [title]

    def animate(frame):
        ax.clear()
        ax.set_facecolor('#0b0f19')
        ax.set_xlim(-1, len(groups))
        ax.set_ylim(-1, max_len + 3)
        ax.axis('off')
        
        ax.text(0.5, 0.92, f"MIRAGE Visualizer | Frame {frame+1}/{len(groups)}", 
                transform=ax.transAxes, color="#00ffff", fontsize=12, ha="center", fontfamily="monospace")
        
        # Draw all groups up to the current frame with a glowing highlight on the active group
        for idx, g in enumerate(groups):
            box_color = '#1f2937' if idx != frame else '#3b82f6'
            edge_color = '#4b5563' if idx != frame else '#60a5fa'
            
            # Draw group container box
            rect = plt.Rectangle((idx - 0.4, 0), 0.8, len(g) + 0.5, facecolor=box_color, edgecolor=edge_color, linewidth=2, alpha=0.9, borderRadius=0.1)
            ax.add_patch(rect)
            
            # Draw group label
            ax.text(idx, -0.6, f"G{idx+1}", color='#9ca3af', fontsize=9, ha='center', fontfamily='monospace')

            # Draw individual characters in the stack
            for char_idx, char in enumerate(g):
                c = color_map.get(char.upper(), '#ffffff')
                ax.text(idx, char_idx + 0.25, char, color=c, fontsize=14, fontweight='bold', 
                        ha='center', va='center', fontfamily='monospace')

        return []

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(groups), interval=1000, blit=False)
    
    # Save as MP4 or GIF
    if filename.endswith('.gif'):
        ani.save(filename, writer='pillow', fps=fps)
    else:
        # Requires ffmpeg installed for MP4
        ani.save(filename, writer='ffmpeg', fps=fps)
        
    print(f"✅ MG Video successfully rendered and saved as: {filename}")
    plt.close()

if __name__ == "__main__":
    sample_dna = "AGGCTTACCGGTAAGGTT"
    generate_mg_video(sample_dna, filename="mirage_mg_animation.gif", fps=1)