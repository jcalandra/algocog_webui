import matplotlib.pyplot as plt
from acwebui.src.parameters import SR, HOP_LENGTH, TO_SAVE_PYP, EVOL_PRINT, LETTER_DIFF, processing, PATH_RESULT, \
    superpose_threshold
import numpy as np
from website.settings import BASE_DIR
import os

# In this file are implemented all the fonctions for the initialization and the update of the formal diagram and
# the functions to display the formal diagrams.
path_results = PATH_RESULT
letter_diff = LETTER_DIFF

f_number = 0


# ============================================ FORMAL DIAGRAM 2D =======================================================
# Implementation for an evolutive formal diagram
def print_formal_diagram_init(level):
    """ Print the formal diagram at level 'level' at its initialization."""
    # print("PRINT formal diagram init")
    fig = plt.figure(figsize=(36, 24))
    plt.title("Formal diagram of level " + str(level))
    plt.xlabel("time in seconds (formal memory)")
    plt.ylabel("material (material memory)")
    plt.gray()
    return fig.number


def print_formal_diagram_update(fig_number, level, formal_diagram, data_length):
    """ Print the updated formal diagram  'formal_diagram' at level 'level' in the window 'fig_number'."""
    # print("PRINT formal diagram update")
    fig = plt.figure(fig_number)
    plt.clf()
    global f_number
    f_number += 1
    file_name_pyplot = "FD_level" + str(level)
    plt.title("Formal diagram of level " + str(level))
    if processing == 'symbols':
        plt.xlabel("time in number of states (formal memory)")
    elif processing == 'signal':
        plt.xlabel("time in seconds (formal memory)")
    plt.ylabel("material (material memory)")
    string = ""
    for i in range(len(formal_diagram)):
        string += chr(i + letter_diff + 1)
    # plt.yticks([i for i in range(len(string))], string)
    if processing == 'symbols':
        plt.imshow(formal_diagram, extent=[0, int(data_length), len(formal_diagram), 0])
    elif processing == 'signal':
        plt.imshow(formal_diagram, extent=[0, int(data_length / SR * HOP_LENGTH), len(formal_diagram), 0])
    if TO_SAVE_PYP:
        plt.savefig(path_results + file_name_pyplot)
    if EVOL_PRINT == 1:
        plt.pause(0.1)
        name = os.path.join(BASE_DIR, 'uploads/photos_tmp/') + str(level) + ".png"
        plt.savefig(name)
    return fig.number


def formal_diagram_init(formal_diagram, data_length, oracles, level):
    """Initialize the formal diagram 'formal_diagram' at level 'level'."""
    # print("formal diagram init")
    new_mat = [1 for i in range(data_length)]
    formal_diagram.append(new_mat)
    if level == 0:
        n = 1
    else:
        k_end = 1
        lv = level - 1
        while lv >= 0:
            link = oracles[1][lv][1]
            link_r = link.copy()
            link_r.reverse()
            k_end = len(link_r) - link_r.index(k_end) - 1
            lv = lv - 1
        n = k_end
    for i in range(n):
        formal_diagram[0][i] = 1.1/4
    return 1


def formal_diagram_update(formal_diagram, data_length, actual_char, actual_char_ind, oracles, level, params):
    """Update the formal diagram 'formal_diagram' at level 'level' at instant 'actual_char_ind' with material
    'actual_char'."""
    # print("formal diagram update")
    k_init = actual_char_ind
    if processing == 'symbols':
        actual_char = actual_char - oracles[1][level][0].data[1] + 1
    if level == 0:
        n = 1
    else:
        k_end = k_init
        lv = level - 1
        while lv >= 0:
            link = oracles[1][lv][1]
            link_r = link.copy()
            link_r.reverse()
            k_init = link.index(k_init)
            true_len = len(link) - link_r.index(len(oracles[1][lv + 1][0].data) - 1)
            sub_link_r = link.copy()
            sub_link_r = sub_link_r[:true_len]
            sub_link_r.reverse()
            k_end = true_len - sub_link_r.index(k_end) - 1
            lv = lv - 1
        n = k_end - k_init + 1
    color = (actual_char_ind % 4 + 0.1)/4
    if actual_char > len(formal_diagram):
        new_mat = [1 for i in range(data_length)]
        formal_diagram.append(new_mat)
    side_materials(oracles, level, formal_diagram, actual_char, n, k_init, params)
    for i in range(n):
        formal_diagram[actual_char - 1][k_init + i - 1] = color
    return 0


def side_materials(oracles, level, formal_diagram, actual_char, n, k_init, params):
    if level == 0:
        matrix_values = oracles[1][0][7][1]
    else:
        matrix_values = oracles[1][level - 1][6][1]
    for i in range(1, actual_char - 1):
        for j in range(n):
            formal_diagram[i][k_init + j - 1] = min((1 - matrix_values[actual_char - 1][i])/(1 - params.min_matrix), 1)


def side_materials2(oracles, level, formal_diagram, actual_char, n, k_init, color):
    if level == 0:
        matrix_values = oracles[1][0][7][1]
    else:
        matrix_values = oracles[1][level - 1][6][1]
    for i in range(1, actual_char - 1):
        if matrix_values[actual_char - 1][i] > superpose_threshold:
            for j in range(n):
                formal_diagram[i][k_init + j - 1] = color + 0.1


# ======================================== FORMAL DIAGRAM 3D (TESTS) ===================================================
def diagram3D(oracles):
    """ 3D representation proposition of the formal diagrams once they are all created."""
    z_len = len(oracles[1])
    y_len = len(oracles[1][0][4][0])

    x_len = len(oracles[1][0][4])
    for i in range(1, z_len):
        if len(oracles[1][0][4]) > x_len:
            nb_mat_max = len(oracles[1][0][4])

    colors = ['red', 'blue', 'green', 'cyan', 'magenta', 'purple', 'grey']
    colors_maxi_mat = []
    colors_mat = []

    maxi_mat = []
    mat = []
    j = 0
    while j < len(oracles[1][0][4]):
        mat_len = []
        colors_len = []
        for k in range(y_len):
            if oracles[1][0][4][j][k][0] == 255 and oracles[1][0][4][j][k][1] == 255 \
                    and oracles[1][0][4][j][k][2] == 255:
                mat_len.append(False)
                colors_len.append(None)
            else:
                mat_len.append(True)
                colors_len.append(colors[0])
        mat.append(mat_len)
        colors_mat.append(colors_len)
        j += 1
    while j < x_len:
        mat_len = [False for i in range(y_len)]
        colors_len = [None for i in range(y_len)]
        mat.append(mat_len)
        colors_mat.append(colors_len)
        j += 1
    maxi_mat.append(mat)
    colors_maxi_mat.append(colors_mat)

    for i in range(1, z_len):
        mat = []
        colors_mat = []
        j = 0
        while j < len(oracles[1][i][4]):
            mat_len = []
            colors_len = []
            for k in range(y_len):
                if (oracles[1][i][4])[j][k] == 1:
                    mat_len.append(False)
                    colors_len.append(None)
                else:
                    mat_len.append(True)
                    colors_len.append(colors[i])
            mat.append(mat_len)
            colors_mat.append(colors_len)
            j += 1
        while j < x_len:
            mat_len = [False for i in range(y_len)]
            colors_len = [None for i in range(y_len)]
            mat.append(mat_len)
            colors_mat.append(colors_len)
            j += 1
        maxi_mat.append(mat)
        colors_maxi_mat.append(colors_mat)
    maxi_mat_np = np.array(maxi_mat)
    maxi_colors_np = np.array(colors_maxi_mat)

    fig = plt.figure(figsize=(50, 50))
    ax = fig.gca(projection='3d')
    ax.voxels(maxi_mat_np, facecolors=maxi_colors_np)