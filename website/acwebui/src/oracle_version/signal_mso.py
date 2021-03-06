from .data_computing import get_data, get_descriptors
from .similarity_functions import true_mat, dissimilarity
import numpy as np
import cv2
import time
# import plot
from acwebui.src.parameters import BASIC_FRAME, BACKGROUND, SEG_ERROR, CLASS_ERROR, SEGMENTATION,\
    CORRECTION_BIT_COLOR, WRITE_RESULTS, NB_SILENCE, SUFFIX_METHOD, NOTE_MIN, SYNTHESIS, HOP_LENGTH, INIT, NB_VALUES, \
    verbose, SEGMENTATION_BIT
from .mso import *
from .synthesis_mso import synthesis
from .formal_diagram_mso import print_formal_diagram_update, letter_diff
from .oracle_mso import create_oracle
from .algo_segmentation_mso import fun_segmentation
from .similarity_rules import char_next_level_similarity


# import compute_dynamics as cd

# In this file are implemented functions for the cognitive algorithm  with the oracle as the main structure

# TODO : intégrer le timbre dans la représentation

# note : matrices are created in HSV
fmin = NOTE_MIN
hop_length = HOP_LENGTH
init = INIT
nb_values = NB_VALUES

# ======================================== ORACLE INITIALISATION AND CORRECTION ========================================
def modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data):
    """ Modify the oracle 'oracle_t' according to the last corrected frame of mat 'j_mat' at instant 'i_hop'."""
    obs = input_data[i_hop]
    if prev_mat == oracle_t.data[-1]:
        if len(oracle_t.latent[prev_mat]) > 1:
            good_sfx = oracle_t.latent[prev_mat][-2]
        else:
            good_sfx = 0
    else:
        good_sfx = oracle_t.latent[prev_mat][-1]
    oracle_t.data[i_hop + 1] = prev_mat
    oracle_t.rsfx[oracle_t.sfx[i_hop + 1]].pop()
    oracle_t.rsfx[good_sfx].append(i_hop + 1)
    (oracle_t.rsfx[good_sfx]).sort()

    oracle_t.rep[prev_mat][0] = (oracle_t.rep[prev_mat][0] * oracle_t.rep[prev_mat][1] + obs) / \
                                (oracle_t.rep[prev_mat][1] + 1)
    oracle_t.rep[prev_mat][1] = oracle_t.rep[prev_mat][1] + 1
    oracle_t.sfx[i_hop + 1] = good_sfx
    oracle_t.latent[j_mat].pop()
    oracle_t.latent[prev_mat].append(i_hop + 1)
    (oracle_t.latent[prev_mat]).sort()

    if (oracle_t.rep[j_mat][0] * oracle_t.rep[j_mat][1] - obs).all() == 0 and oracle_t.rep[j_mat][1] - 1 == 0:
        oracle_t.rep.pop(j_mat)
        oracle_t.latent.pop(j_mat)
        oracle_t.vec.pop(j_mat - 1)
        for ind in range(j_mat - 1, len(oracle_t.vec)):
            oracle_t.vec[ind].pop(prev_mat - 1)
        for j in range(len(oracle_t.data) - 2, len(oracle_t.data)):
            if oracle_t.data[j] and oracle_t.data[j] > j_mat:
                oracle_t.data[j] = oracle_t.data[j] - 1
    else:
        oracle_t.rep[j_mat][0] = (oracle_t.rep[j_mat][0] * oracle_t.rep[j_mat][1] - obs) / \
                                 (oracle_t.rep[j_mat][1] - 1)
        oracle_t.rep[j_mat][1] = oracle_t.rep[j_mat][1] - 1


def modify2_oracle(oracle_t, prev2_mat, prev_mat, j_mat, i_hop, input_data):
    """ Modify the oracle 'oracle_t' according to the two last corrected frames of mat 'j_mat' and 'prev_mat' at instant
    'i_hop' and i_hop - 1."""
    obs_1 = input_data[i_hop]
    obs_2 = input_data[i_hop - 1]

    if prev2_mat == oracle_t.data[-1]:
        if len(oracle_t.latent[prev2_mat]) > 1:
            good_sfx = oracle_t.latent[prev2_mat][-2]
        else:
            good_sfx = 0
    else:
        good_sfx = oracle_t.latent[prev2_mat][-1]

    oracle_t.data[i_hop + 1] = prev2_mat
    oracle_t.data[i_hop] = prev2_mat

    oracle_t.rsfx[oracle_t.sfx[i_hop + 1]].pop()
    oracle_t.rsfx[oracle_t.sfx[i_hop]].pop()
    oracle_t.rsfx[good_sfx - 1].append(i_hop)
    oracle_t.rsfx[good_sfx].append(i_hop + 1)
    (oracle_t.rsfx[good_sfx - 1]).sort()
    (oracle_t.rsfx[good_sfx]).sort()

    oracle_t.rep[prev2_mat][0] = (oracle_t.rep[prev2_mat][0] * oracle_t.rep[prev2_mat][1] + obs_2) / \
                                 (oracle_t.rep[prev2_mat][1] + 1)
    oracle_t.rep[prev2_mat][1] = oracle_t.rep[prev2_mat][1] + 1
    oracle_t.rep[prev2_mat][0] = (oracle_t.rep[prev2_mat][0] * oracle_t.rep[prev2_mat][1] + obs_1) / \
                                 (oracle_t.rep[prev2_mat][1] + 1)
    oracle_t.rep[prev2_mat][1] = oracle_t.rep[prev2_mat][1] + 1

    oracle_t.sfx[i_hop] = good_sfx - 1
    oracle_t.sfx[i_hop + 1] = good_sfx

    oracle_t.latent[j_mat].pop()
    oracle_t.latent[prev_mat].pop()
    oracle_t.latent[prev2_mat].append(i_hop)
    oracle_t.latent[prev2_mat].append(i_hop + 1)
    (oracle_t.latent[prev2_mat]).sort()
    if prev_mat != j_mat and (oracle_t.rep[j_mat][0] * oracle_t.rep[j_mat][1] - obs_1).all() == 0:
        oracle_t.rep.pop(j_mat)
        oracle_t.latent.pop(j_mat)
        oracle_t.vec.pop(j_mat - 1)
        for ind in range(j_mat - 1, len(oracle_t.vec)):
            oracle_t.vec[ind].pop(prev_mat - 1)
        if prev_mat > j_mat:
            prev_mat = prev_mat - 1
        for j in range(len(oracle_t.data) - 3, len(oracle_t.data)):
            if oracle_t.data[j] and oracle_t.data[j] > j_mat:
                oracle_t.data[j] = oracle_t.data[j] - 1
    else:
        oracle_t.rep[j_mat][0] = (oracle_t.rep[j_mat][0] * oracle_t.rep[j_mat][1] - obs_1) / \
                                 (oracle_t.rep[j_mat][1] - 1)
        oracle_t.rep[j_mat][1] = oracle_t.rep[j_mat][1] - 1
    if (oracle_t.rep[prev_mat][0] * oracle_t.rep[prev_mat][1] - obs_2).all() == 0:
        oracle_t.rep.pop(prev_mat)
        oracle_t.latent.pop(prev_mat)
        oracle_t.vec.pop(prev_mat - 1)
        for ind in range(prev_mat - 1, len(oracle_t.vec)):
            oracle_t.vec[ind].pop(prev_mat - 1)
        for j in range(len(oracle_t.data) - 3, len(oracle_t.data)):
            if oracle_t.data[j] and oracle_t.data[j] > prev_mat:
                oracle_t.data[j] = oracle_t.data[j] - 1
    else:
        oracle_t.rep[prev_mat][0] = (oracle_t.rep[prev_mat][0] * oracle_t.rep[prev_mat][1] - obs_2) / \
                                    (oracle_t.rep[prev_mat][1] - 1)
        oracle_t.rep[prev_mat][1] = oracle_t.rep[prev_mat][1] - 1


def build_oracle(flag, TETA, nb_values, nb_hop, s_tab, v_tab, params):
    """Initialize an oracle with the given parameters."""
    volume_data = v_tab
    suffix_method = SUFFIX_METHOD

    if params.MFCC_BIT == 1:
        dim = nb_values - 1
        input_data = s_tab.transpose()
    elif params.FFT_BIT == 1:
        dim = len(s_tab[0])
        input_data = np.array(s_tab)
    else:
        dim = nb_values
        input_data = s_tab.transpose()

    if type(input_data) != np.ndarray or type(input_data[0]) != np.ndarray:
        input_data = np.array(input_data)
    if input_data.ndim != 2:
        input_data = np.expand_dims(input_data, axis=1)

    oracle_t = create_oracle(flag, threshold=TETA, dfunc='cosine', dfunc_handle=None, dim=dim)

    return volume_data, suffix_method, input_data, oracle_t


# ================================================ MATRIX CORRECTION ===================================================
def modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, lim_ind):
    """ Modify the similarity matrix according the the corrected frames."""
    # TODO: regarder les ajouts et suppression dans oracle_t.vec
    blank_ind = 0
    while mtx[prev_mat][blank_ind][0] == BACKGROUND[0] and mtx[prev_mat][blank_ind][1] == BACKGROUND[1] \
            and mtx[prev_mat][blank_ind][2] == BACKGROUND[2]:
        blank_ind += 1

    if blank_ind == lim_ind and prev_mat == actual_max:
        matrix[0] = matrix[0][:-1]
        matrix[1].pop()
        for i in range(len(matrix[1])):
            matrix[1][i].pop()
        actual_max = actual_max - 1
        temp_max = temp_max - 1
        mtx = np.delete(mtx, - 1, 0)
        return 1, matrix, actual_max, temp_max, mtx
    return 0, matrix, actual_max, temp_max, mtx


# ============================================ COGNITIVE ALGORITHM =====================================================
def prep_data(audio_path):
    """ Prepare the signal from continue to discrete values and add silence at the beginning."""
    here_time = time.time()
    data, rate, data_size, data_length = get_data(audio_path)
    temps_data = time.time() - here_time
    if verbose == 1:
        print("Temps data : %s secondes ---" % temps_data)

    nb_points = NB_SILENCE
    a = np.zeros(nb_points)
    data = np.concatenate((a, data))
    return data, rate, data_size, data_length, nb_points


def matrix_init(rate, data_size, data_length, nb_points):
    """ Initialize the structure corresponding to the formal diagram of level 0."""
    # initialise matrix of each hop coordinates
    nb_sil_frames = nb_points / hop_length
    nb_hop = int(data_size / hop_length + nb_sil_frames) + 1
    data_length = data_length + nb_points / rate
    if data_size % hop_length < init:
        nb_hop = int(data_size / hop_length)
    if verbose == 1:
        print("[RESULT] audio length = ", nb_hop)

    new_mat = np.ones((1, nb_hop, 3), np.uint8)
    for i in range(nb_hop):
        new_mat[0][i] = BACKGROUND
    mtx = new_mat.copy()
    return mtx, nb_hop, data_length


def algo_cog(audio_path, oracles, params, end_mk=0):
    """ Compute the formal diagram of the audio at audio_path with threshold teta and size of frame hop_length."""
    print("[INFO] Computing the cognitive algorithm of the audio extract...")
    TETA = params.TETA
    MFCC_BIT = params.MFCC_BIT
    CQT_BIT = params.CQT_BIT
    FFT_BIT = params.FFT_BIT
    min_matrix = params.min_matrix

    data, rate, data_size, data_length, nb_points = prep_data(audio_path)
    mtx, nb_hop, data_length = matrix_init(rate, data_size, data_length, nb_points)

    if verbose == 1:
        print("[INFO] Computing frequencies and volume...")
    v_tab, s_tab = get_descriptors(data, rate, hop_length, nb_hop, nb_values, init, params, fmin)

    value = 255 - v_tab[0] * 255
    color = (BASIC_FRAME[0], BASIC_FRAME[1], value)
    mtx[0][0] = color

    seg_error = 0
    class_error = 0

    if verbose == 1:
        print("[INFO] Structures initialisation...")

    # ------- CREATE AND BUILD VMO -------
    flag = 'a'
    volume_data, suffix_method, input_data, oracle_t = build_oracle(flag, TETA, nb_values, nb_hop, s_tab, v_tab, params)

    # ------- INITIALISATION OF OTHER STRUCTURES -------
    level = 0
    f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix_next = \
        structure_init(flag, level)
    vec = [1]
    matrix = [chr(letter_diff + 1), [vec]]
    oracles[1].append([f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix_next, matrix])
    oracles[0] = level
    oracles[2] = data

    # ------- ALGORITHM -------
    prev_mat = prev2_mat = prev3_mat = 0
    actual_max = temp_max = 0
    color = color2 = (BASIC_FRAME[0], BASIC_FRAME[1], v_tab[0])
    diff_mk = 0

    if verbose == 1:
        print("[INFO] Computing formal diagram...")

    start_time = time.time()

    # vsd, vdd, vkl, fsd, fdd = cd.compute_dynamics()

    for i_hop in range(nb_hop):  # while
        if verbose == 1:
            print("[INFO] Process in level 0...")
        obs = input_data[i_hop]
        oracle_t.add_state(obs, input_data, volume_data, params, suffix_method)

        j_mat = oracle_t.data[i_hop + 1]
        value = 255 - v_tab[i_hop] * 255

        color3 = color2
        color2 = color
        color = (BASIC_FRAME[0], BASIC_FRAME[1], value)

        if i_hop > 2:
            prev_mat = oracle_t.data[i_hop]
            prev2_mat = oracle_t.data[i_hop - 1]
            prev3_mat = oracle_t.data[i_hop - 2]

        if i_hop == nb_hop - 1 and j_mat != prev_mat:
            modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data)
            j_mat = prev_mat

        diff = dissimilarity(i_hop, s_tab, v_tab, params)
        if diff and len(concat_obj) > 3:
            if diff_mk != 1:
                if SEGMENTATION_BIT:
                    color = SEGMENTATION

                if i_hop == nb_hop - 1:
                    end_mk = 1
                    concat_obj = concat_obj + chr(letter_diff + oracle_t.data[i_hop + 1] + 1)
                # link update
                if len(oracles[1]) > level + 1:
                    # node = len(oracles[1][level + 1][0].data)
                    node = max(oracles[1][level][1]) + 1
                else:
                    node = 1
                for ind in range(len(concat_obj)):
                    link.append(node)
                # history_next update
                new_char = char_next_level_similarity(oracles, level, params)
                # concat_obj update
                concat_obj = ""
                diff_mk = 1
                fun_segmentation(oracles, new_char, nb_hop, params, level=level + 1, end_mk=end_mk)
                if verbose == 1:
                    print("[INFO] Process in level 0...")
        else:
            diff_mk = 0
            if i_hop == nb_hop - 1:
                end_mk = 1
                concat_obj = concat_obj + chr(letter_diff + oracle_t.data[i_hop + 1] + 1)
                # link update
                if len(oracles[1]) > level + 1:
                    node = max(oracles[1][level][1]) + 1
                else:
                    node = 1
                for ind in range(len(concat_obj)):
                    link.append(node)
                # history_next update
                new_char = char_next_level_similarity(oracles, level, params)
                # concat_obj update
                concat_obj = ""
                diff_mk = 1
                fun_segmentation(oracles, new_char, nb_hop, params, level=level + 1, end_mk=end_mk)
                if verbose == 1:
                    print("[INFO] Process in level 0...")

        if j_mat > actual_max:

            if i_hop > 2 and prev_mat != prev2_mat and params.CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                seg_error = seg_error + 1
                good_mat = true_mat(i_hop - 1, i_hop, i_hop - 2, j_mat, prev2_mat, s_tab, params)
                if good_mat == j_mat:
                    modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data)
                    j_mat = oracle_t.data[i_hop]

                else:
                    modify_oracle(oracle_t, prev2_mat, prev_mat, i_hop - 1, input_data)
                    digit, matrix, actual_max, temp_max, mtx = \
                        modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, i_hop - 1)
                    if digit == 1:
                        j_mat -= 1

            elif i_hop > 2 and prev_mat != prev3_mat and params.CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                good_mat = true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab, params)
                if good_mat == j_mat:
                    modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data)
                    j_mat = oracle_t.data[i_hop]
                    temp_max = j_mat
                else:
                    modify2_oracle(oracle_t, prev3_mat, prev2_mat, prev_mat, i_hop - 1, input_data)
                    digit, matrix, actual_max, temp_max, mtx = \
                        modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, i_hop - 1)
                    if digit == 1:
                        j_mat -= 1
                    digit, matrix, actual_max, temp_max, mtx = \
                        modify_matrix(mtx, prev2_mat, matrix, actual_max, temp_max, i_hop - 2)
                    if digit == 1:
                        j_mat -= 1
                    seg_error = seg_error + 2

        if j_mat > actual_max:
            temp_max = j_mat
            vec = oracle_t.vec[len(matrix[0]) - 1].copy()
            vec.append(1)
            matrix[0] += (chr(len(matrix[0]) + letter_diff + 1))
            matrix[1].append(vec)
            for i in range(len(matrix[1]) - 1):
                matrix[1][i].append(matrix[1][len(matrix[1]) - 1][i])
            new_mat_l = np.ones((1, nb_hop, 3), np.uint8)
            for i in range(nb_hop):
                new_mat_l[0][i] = BACKGROUND
            mtx = np.concatenate((mtx, new_mat_l))

        else:

            if i_hop > 2 and prev_mat != prev2_mat and j_mat != prev_mat and params.CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 1
                good_mat = true_mat(i_hop - 1, i_hop, i_hop - 2, j_mat, prev2_mat, s_tab, params)

                # By default the best element is the previous one because FO cannot point on future objects
                modify_oracle(oracle_t, good_mat, prev_mat, i_hop - 1, input_data)
                digit, matrix, actual_max, temp_max, mtx = \
                    modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, i_hop - 1)

            if i_hop > 2 and prev_mat == prev2_mat and prev_mat != prev3_mat and j_mat != prev_mat and \
                    params.CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 2
                good_mat = true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab, params)
                modify2_oracle(oracle_t, good_mat, prev2_mat, prev_mat, i_hop - 1, input_data)
                digit, matrix, actual_max, temp_max, mtx = \
                    modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, i_hop - 1)
                digit, matrix, actual_max, temp_max, mtx = \
                    modify_matrix(mtx, prev2_mat, matrix, actual_max, temp_max, i_hop - 2)

        if i_hop > 3:
            for j in range(len(oracle_t.data) - 3, len(oracle_t.data)):
                for k in range(len(mtx)):
                    mtx[k][j - 1] = BACKGROUND
            mtx[oracle_t.data[i_hop - 1]][i_hop - 2] = color3
            mtx[oracle_t.data[i_hop]][i_hop - 1] = color2
            mtx[oracle_t.data[i_hop + 1]][i_hop] = color
            for mat in range(1, oracle_t.data[i_hop - 1]):
                value = min((1 - matrix[1][oracle_t.data[i_hop - 1]][mat])/(1 - min_matrix) * 255,255)
                mtx[mat][i_hop - 2] = (BASIC_FRAME[0], BASIC_FRAME[1], value)
            for mat in range(1, oracle_t.data[i_hop]):
                value = min((1 - matrix[1][oracle_t.data[i_hop]][mat])/(1 - min_matrix) * 255,255)
                mtx[mat][i_hop - 1] = (BASIC_FRAME[0], BASIC_FRAME[1], value)
        for mat in range(1, oracle_t.data[i_hop + 1]):
            value = min((1 - matrix[1][oracle_t.data[i_hop + 1]][mat])/(1 - min_matrix) * 255, 255)
            mtx[mat][i_hop] = (BASIC_FRAME[0], BASIC_FRAME[1], value)

        if len(concat_obj) == 1:
            if len(history_next) > 0:
                new_history_next_element = history_next[-1][1]
                if ord(history_next[-1][1][-2]) - letter_diff > len(matrix[0]):
                    tmp_char = history_next[-1][1][-1]
                    new_history_next_element = new_history_next_element[:-2]
                    new_history_next_element += chr(oracle_t.data[i_hop - 1] + letter_diff + 1)
                    new_history_next_element += tmp_char
                if ord(history_next[-1][1][-1]) - letter_diff > len(matrix[0]):
                    new_history_next_element = new_history_next_element[:-1]
                    new_history_next_element += chr(oracle_t.data[i_hop - 1] + letter_diff + 1)
                history_next[-1] = (history_next[-1][0], new_history_next_element, history_next[-1][2])
            concat_obj = chr(letter_diff + oracle_t.data[i_hop] + 1)

        if len(concat_obj) == 2:
            if len(history_next) > 0:
                new_history_next_element = history_next[-1][1]
                if ord(history_next[-1][1][-1]) - letter_diff > len(matrix[0]):
                    new_history_next_element = new_history_next_element[:-1]
                    new_history_next_element += chr(oracle_t.data[i_hop - 1] + letter_diff + 1)
                history_next[-1] = (history_next[-1][0], new_history_next_element,  history_next[-1][2])
            concat_obj = chr(letter_diff + oracle_t.data[i_hop - 1] + 1) \
                         + chr(letter_diff + oracle_t.data[i_hop] + 1)
            # TODO: corriger la valeur dans la matrice

        if len(concat_obj) >= 3:
            concat_obj = concat_obj[:len(concat_obj) - 2] + chr(letter_diff + oracle_t.data[i_hop - 1] + 1) \
                         + chr(letter_diff + oracle_t.data[i_hop] + 1)
        concat_obj = concat_obj + chr(letter_diff + oracle_t.data[i_hop + 1] + 1)

        if temp_max > actual_max:
            actual_max = temp_max
        formal_diagram = cv2.cvtColor(mtx, cv2.COLOR_HSV2BGR)
        print_formal_diagram_update(formal_diagram_graph, level, formal_diagram, nb_hop)

        g_oracle = create_oracle('f')
        for ind in range(i_hop + 1):
            g_oracle.add_state(oracle_t.data[ind + 1] + 1)
        f_oracle = g_oracle
        oracles[1][level][0] = f_oracle
        oracles[1][level][1] = link
        oracles[1][level][2] = history_next
        oracles[1][level][3] = concat_obj
        oracles[1][level][4] = formal_diagram
        oracles[1][level][5] = formal_diagram_graph

    if flag != 'f' and flag != 'v':
        oracle_t.f_array.finalize()

    mtx = cv2.cvtColor(mtx, cv2.COLOR_HSV2BGR)
    distance = (seg_error + class_error) / nb_hop

    algocog_time = time.time() - start_time
    print("Temps de calcul l'algorithme : %s secondes ---" % algocog_time)

    if WRITE_RESULTS:
        f_ac = open("../../results/algocog_computing.txt", "a")
        f_ac.write(str(algocog_time) + "\n")
        f_ac.close()
        name = audio_path.split('/')[-1]
        file = open("../results/error.txt", "a")
        file.write("\nERROR file " + name + ", " + str(hop_length) + ", " + str(nb_values) + ", " + str(TETA) +
                   ", " + str(init) + "\nseg_error = " + str(seg_error) + "\nclass_error = " + str(class_error) +
                   "\ndistance = " + str(distance) + "\n")
        file.close()

    if SYNTHESIS == 1:
        name = audio_path.split('/')[-1][:-4] + '_synthesis.wav'
        print("name : ", name)
        synthesis(oracle_t, nb_hop, data, hop_length, rate, name)

    '''if PLOT_ORACLE == 1:
        im = plot.start_draw(oracle_t, size=(900 * 4, 400 * 4))
        im.show()'''

    return mtx, data_length, data_size, distance, algocog_time
