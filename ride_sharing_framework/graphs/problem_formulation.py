import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_scenario(ax, sec_positions, ev_positions, tp_positions, ev_movements, title):
    # Set limits and grid
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_xticks(range(4))
    ax.set_yticks(range(3))
    ax.grid(True)
    ax.set_title(title, fontsize=12)

    # Plot SECs
    for sec, (x, y) in sec_positions.items():
        ax.add_patch(patches.Circle((x, y), 0.1, color='blue'))
        ax.text(x, y, sec, color='white', ha='center', va='center')

    # Plot EV initial positions
    for ev, (x, y) in ev_positions.items():
        ax.add_patch(patches.Rectangle((x - 0.1, y - 0.1), 0.2, 0.2, color='green'))
        ax.text(x, y, ev, color='white', ha='center', va='center')

    # Plot TPs
    for tp, (px, py, dx, dy) in tp_positions.items():
        ax.add_patch(patches.Circle((px, py), 0.1, color='red'))
        ax.text(px, py, tp + '_P', color='white', ha='center', va='center')
        ax.add_patch(patches.Circle((dx, dy), 0.1, color='orange'))
        ax.text(dx, dy, tp + '_D', color='white', ha='center', va='center')

    # Plot EV movements
    for ev, movements in ev_movements.items():
        for (x1, y1), (x2, y2) in movements:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

    return ax


# Define positions and movements
sec_positions = {'SEC1': (1, 2), 'SEC2': (2, 3)}
ev_positions = {'EV1': (1, 2), 'EV2': (1, 2)}
tp_positions = {
    'TP1': (2, 3, 0, 0),
    'TP2': (2, 2, 1, 1),
    'TP3': (2, 3, 1, 3),
    'TP4': (1, 2, 2, 3)
}
ev_movements_with_incentives = {
    'EV1': [((1, 2), (2, 3)), ((2, 3), (2, 2)), ((2, 2), (1, 1)), ((1, 1), (0, 0)),
            ((0, 0), (1, 1)), ((1, 1), (2, 3)), ((2, 3), (1, 1))],
    'EV2': [((1, 2), (1, 2))]  # EV2 stays idle initially
}
ev_movements_without_incentives = {
    'EV1': [((1, 2), (2, 3)), ((2, 3), (2, 2)), ((2, 2), (1, 1)), ((1, 1), (0, 0)),
            ((0, 0), (1, 2)), ((1, 2), (2, 3)), ((2, 3), (1, 2))],
    'EV2': [((1, 2), (1, 2))]  # EV2 stays idle initially
}

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Plot scenarios
draw_scenario(axes[0], sec_positions, ev_positions, tp_positions, ev_movements_with_incentives,
              "Scenario with Incentives")
draw_scenario(axes[1], sec_positions, ev_positions, tp_positions, ev_movements_without_incentives,
              "Scenario without Incentives")

plt.tight_layout()
plt.show()
