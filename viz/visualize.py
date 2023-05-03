import matplotlib.pyplot as plt

colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'yellow', 'black', 'white']

def draw_poly(polymino, ax, color='blue'):
    for x, y in polymino:
        ax.add_patch(plt.Rectangle((x, y), 1, 1, facecolor=color))
    min_x = min(p[0] for p in polymino)
    max_x = max(p[0] for p in polymino)
    min_y = min(p[1] for p in polymino)
    max_y = max(p[1] for p in polymino)
    ax.set_xlim(min_x - 1, max_x + 2)
    ax.set_ylim(min_y - 1, max_y + 2)
    ax.set_aspect('equal')
    ax.axis('off')

def draw_edges(polymino, ax, x_offset=0, y_offset=0, color='black'):
    for x, y in polymino:
        x += x_offset
        y += y_offset
        ax.plot([x, x + 1], [y, y], color=color, linewidth=2)
        ax.plot([x + 1, x + 1], [y, y + 1], color=color, linewidth=2)
        ax.plot([x + 1, x], [y + 1, y + 1], color=color, linewidth=2)
        ax.plot([x, x], [y + 1, y], color=color, linewidth=2)
    ax.set_aspect('equal')
    ax.axis('off')

def draw_polymino_set(polyminoes, colors=None):
    '''
    Draw a set of 
    '''
    
    fig, axes = plt.subplots(1, len(polyminoes), figsize=(len(polyminoes) * 2, 2))
    
    i = 0
    for ax, polymino in zip(axes, polyminoes):
        draw_poly(polymino, ax, color=colors[i % len(colors)] if colors else 'blue')
        draw_edges(polymino, ax)
        i += 1

    plt.show()

def draw_packing(polyminoes, locations, board_width, board_height):
    
    def draw_polymino(polymino, ax, x_offset=0, y_offset=0, color='blue'):
        for x, y in polymino:
            ax.add_patch(plt.Rectangle((x + x_offset, y + y_offset), 1, 1, facecolor=color))
        ax.set_aspect('equal')
        ax.axis('off')

    fig, ax = plt.subplots(figsize=(board_width, board_height))
    ax.set_xlim(0, board_width)
    ax.set_ylim(0, board_height)

    i = 0
    for polymino, (x_offset, y_offset) in zip(polyminoes, locations):
        c = colors[i % len(colors)]
        draw_edges(polymino, ax, x_offset, y_offset, color='black')
        draw_polymino(polymino, ax, x_offset, y_offset, color=c)
        i += 1
    plt.show()
