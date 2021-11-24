import numpy as np
from Bio import pairwise2
from Bio.Align import substitution_matrices
from .similarity_functions import frequency_static_similarity_fft
from acwebui.src.parameters import TRANSPOSITION, QUOTIENT, LETTER_DIFF, GAP_VALUE, EXT_GAP_VALUE, GAP, \
    CORREC_VALUE, SR, NB_VALUES, NB_NOTES, NOTES_PER_OCTAVE, NOTE_MIN
import librosa

# In this file are computed the alignment between strings to compute similarity at a symbolic scale

transpo = TRANSPOSITION
quotient = QUOTIENT

letter_diff = LETTER_DIFF


# ================================================= ALIGNMENT ==========================================================
# penalty values
gap_value = GAP_VALUE
extend_gap_value = EXT_GAP_VALUE
gap = GAP
correc_value = CORREC_VALUE


def compute_alignment(string_compared, actual_string, mat, params):
    # initalisation
    alignment = -pow(10, 10)
    if len(actual_string) == 0:
        return 0, 0
    min_len = min(len(string_compared), len(actual_string))

    # creation of the similarity matrix
    if not mat[1]:
        mat[1] = np.empty((0, 0))
    np_mat = np.array(mat[1]) * quotient
    matrix = substitution_matrices.Array(alphabet=mat[0], dims=2, data=np_mat)

    # conversion of the string if necessary
    sx = string_compared
    for j in range(transpo):
        sy = ''
        for i in actual_string:
            sy += chr(ord(i) - j)

        # Needleman-Wunsch alignment
        nw_align = pairwise2.align.globalds(sx, sy, matrix, gap_value, extend_gap_value, gap_char=gap)
        if len(nw_align) == 0:
            return 0, 0
        nw_alignment = nw_align[0][2]
        if nw_alignment > alignment:
            alignment = nw_alignment

    similarity = (alignment - correc_value) / min_len
    if similarity >= params.TETA * quotient:
        # print(nw_align[0][0], nw_align[0][1])
        # print("tabTransfo", lambda_tabTransfo(nw_align[0][0], nw_align[0][1], [], gap))
        return 1, similarity
    return 0, similarity


# ==================================================== SIGNAL ==========================================================
rate = SR
nb_value = NB_VALUES

nb_notes = NB_NOTES
NPO = NOTES_PER_OCTAVE
fmin = NOTE_MIN


def compute_window_audio(oracles, level, actual_object):
    # descriptor corresponds to the descriptor that is computed from the actual_object
    descriptor = []
    # TODO: when object structure will be modified,
    #  k_init = actual_object.init,
    #  k_end = k_init + len(actual_object.label) - 1
    k_init = len(oracles[1][level][1]) + 1
    k_end = k_init + len(actual_object) - 1
    if level > 0:
        lv = level - 1
        while lv >= 0:
            link = oracles[1][lv][1]
            link_r = link.copy()
            link_r.reverse()
            k_init = link.index(k_init)
            k_end = len(link) - link_r.index(k_end) - 1

    window = oracles[2][k_init:k_end + 1]
    return window


def compute_descriptor(window):
    hop_length = len(window)
    #if MFCC_BIT:
    descriptor = librosa.feature.mfcc(y=window, sr=rate, hop_length=hop_length, n_mfcc=20)[1:]
    '''elif FFT_BIT:
        descriptor = data_computing.get_frequency_windows(window, rate, 0, hop_length)
    else:
        descriptor = np.abs(librosa.cqt(window, sr=rate, hop_length=hop_length, fmin=librosa.note_to_hz(fmin),
                     n_bins=nb_notes, bins_per_octave=NPO, window='blackmanharris', sparsity=0.01, norm=1))
        descriptor = librosa.amplitude_to_db(descriptor, ref=np.max)'''
    return descriptor


def compute_signal_similarity(s_tab, compared_object_ind, params):
    # freq_static_sim_fft is ok because s_tab is in the according shape
    similarity = frequency_static_similarity_fft(s_tab, compared_object_ind, len(s_tab) - 1)
    if similarity >= params.TETA:
        return 1, similarity
    return 0, similarity
