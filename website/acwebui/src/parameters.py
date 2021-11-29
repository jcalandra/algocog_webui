import website.wsgi
import os
from website.settings import BASE_DIR
from acwebui.models import parameter

# ================================================= PARAMETERS =========================================================
# This is the parametrisation file of the system
# Any variable tha can be modified by the users of the system are here.
# In the interface, numbers might be changed by virtual potentiometers, colors...

# ------------- MAIN -----------------
# Main informations about the signal to
# process

'''NAME, FORMAT = os.path.splitext(parameter.objects.last().file.name.split('/')[-1])

print("NAME=", NAME, "EXT=", FORMAT)

PATH_OBJ_BASIS = os.path.join(BASE_DIR, 'uploads/audio/')
PATH_OBJ = PATH_OBJ_BASIS + ""
PATH_RESULT = os.path.join(BASE_DIR, 'uploads/photos/')

teta = parameter.objects.last().sim_threshold # 0.976
superpose_threshold = 0.95
min_matrix = parameter.objects.last().sim_materials
d_threshold = parameter.objects.last().seg_threshold
# processing must be str 'symbols' or 'signal'
processing = 'signal'
verbose = 0

# === SIMILARITY AND SEGMENTATION RULES ===
# -------- SIGNAL SIMILARITY RULES --------
DIFF_CONCORDANCE = parameter.objects.last().diff_concordance
EUCLID_DISTANCE = parameter.objects.last().euclid_distance

# ------ SIGNAL SEGMENTATION RULES --------
DIFF_FOURIER = parameter.objects.last().diff_fourier
DIFF_DYNAMIC = parameter.objects.last().diff_dynamic

# ------- SYMBOLS SIMILARITY RULES --------
STRICT_EQUALITY = parameter.objects.last().strict_equality
ALIGNMENT = parameter.objects.last().alignment

# -------SYMBOLS SEGMENTATION RULES -------
# Rules that are activated or not and their
# parameters

RULE_1 = parameter.objects.last().rule_1
RULE_2 = parameter.objects.last().rule_2
RULE_3 = parameter.objects.last().rule_3
RULE_4 = parameter.objects.last().rule_4
RULE_5 = parameter.objects.last().rule_5

ALIGNEMENT_rule3 = 0
ALIGNEMENT_rule4 = 0

# ------------- ALIGNEMENT ----------------
# Alignement parameters to reajust similarity
# matrix values and to define the compared
# symbols

QUOTIENT = 100
TRANSPOSITION = 1
LETTER_DIFF = 1

GAP_VALUE = -5
EXT_GAP_VALUE = -1
GAP = chr(0)
CORREC_VALUE = GAP_VALUE/2

# -------- SIGNAL SIM FUNCTIONS -----------
# parameters for signal similarity computation

# fft : 0.91; mfcc : 0.019 pour 50; cqt : 0.97
# at precision 2, 0.927 at precision 1
TETA = teta
AUDIBLE_THRESHOLD = 0.00001
# fft : 35; mfcc : 60 # cqt : 140
D_THRESHOLD = d_threshold
GRAPH_COMPARISON = 0

# ----------- DATA PROCESSING --------------
# parameters for data processing

SR = 22050
HOP_LENGTH = 1024

PRECISION = 4
NB_NOTES = 48*PRECISION
NB_MFCC = 50
INIT = 0

MFCC_BIT = parameter.objects.last().mfcc
CQT_BIT = parameter.objects.last().cqt
FFT_BIT = parameter.objects.last().fft

if CQT_BIT:
    NB_VALUES = NB_NOTES
elif MFCC_BIT:
    NB_VALUES = NB_MFCC
else:
    NB_VALUES = 0

# cqt
NOTES_PER_OCTAVE = 12*PRECISION
NOTE_MIN = 'C3'

# fft
# 0.5 for quarter_tone, 1 for
# half-tone, 2 for tone
TONE_PRECISION = 0.125
DIV = 20

TIME_STATS = 0
MFCC_NORMALISATION = 0
CLEAN_SPECTRUM = 0

# ------------- MIDI ------------------
# parameters for obtention of formal
# diagram from MIDI file

TEMPO = 120

# ------------ DISPLAY ----------------

# note : matrices are created in HSV
# H between 0 and 179
# S between 0 and 255
# V between 0 and 255

BASIC_FRAME = (0, 0, 0)  # black
BACKGROUND = (0, 0, 255)  # white
SEGMENTATION = (0, 255, 255)  # red
SEG_ERROR = (60, 255, 255)  # light green
CLASS_ERROR = (60, 255, 150)  # dark green
SILENT_FRAME = BACKGROUND



# --------- INTERFACE ---------------
# parameters to save or to show in .bmp
# or from pyplot
TO_SAVE_BMP = 0
TO_SHOW_BMP = 0
TO_SAVE_PYP = 0
TO_SHOW_PYP = 1

# to show or not the oracle at level 0
PLOT_ORACLE = 0
# to show the evolution of the formal
# diagrams
EVOL_PRINT = 1

# ------------ ALGOCOG ----------------

CORRECTION_BIT = not parameter.objects.last().transitory_frame
CORRECTION_BIT_COLOR = 0
SEGMENTATION_BIT = 0
WRITE_RESULTS = 0

NB_SILENCE = 1024*16

ALGO_VMO = 1
ALGO_REP = 0
ALGO_USUAL = 0

# ------------ VMO ---------------

PARCOURS = 1
INCERTITUDE = 3
SUFFIX_METHOD = 'complete'  # 'inc' ou 'complete'

SYNTHESIS = 0'''

# ================================================= PARAMETERS =========================================================
# This is the parametrisation file of the system
# Any variable tha can be modified by the users of the system are here.
# In the interface, numbers might be changed by virtual potentiometers, colors...

# ------------- MAIN -----------------
# Main informations about the signal to
# process

NAME = "Geisslerlied"
FORMAT = '.wav'

PATH_OBJ_BASIS = os.path.join(BASE_DIR, 'uploads/audio/')
PATH_OBJ = PATH_OBJ_BASIS + ""
PATH_RESULT = os.path.join(BASE_DIR, 'uploads/photos/')
teta = 0.9 # 0.976
if teta > 1:
    teta = 1
elif teta < 0:
    teta = 0

superpose_threshold = 0.94
if superpose_threshold > 1:
    superpose_threshold = 1
elif superpose_threshold < 0:
    superpose_threshold = 0

min_matrix = 0.94
if min_matrix > 1:
    min_matrix = 1
elif min_matrix < 0:
    min_matrix = 0

d_threshold = 0.1  # 0.1 for dynamic, 150 for fourier
if d_threshold < 0:
    d_threshold = 0
# processing must be str 'symbols' or 'signal'
processing = 'signal'
verbose = 0


# === SIMILARITY AND SEGMENTATION RULES ===
# -------- SIGNAL SIMILARITY RULES --------
DIFF_CONCORDANCE = 1
EUCLID_DISTANCE = 0

if DIFF_CONCORDANCE + EUCLID_DISTANCE != 1:
    DIFF_CONCORDANCE = 1
    EUCLID_DISTANCE = 0

# ------ SIGNAL SEGMENTATION RULES --------
DIFF_FOURIER = 0
DIFF_DYNAMIC = 1

if DIFF_FOURIER + DIFF_DYNAMIC != 1:
    DIFF_FOURIER = 1
    DIFF_DYNAMIC = 0

# ------- SYMBOLS SIMILARITY RULES --------
STRICT_EQUALITY = 0
ALIGNMENT = 1

if STRICT_EQUALITY + ALIGNMENT != 1:
    STRICT_EQUALITY = 0
    ALIGNMENT = 1

# -------SYMBOLS SEGMENTATION RULES -------
# Rules that are activated or not and their
# parameters

RULE_1 = 1
RULE_2 = 1
RULE_3 = 1
RULE_4 = 0
RULE_5 = 1

ALIGNEMENT_rule3 = 0
ALIGNEMENT_rule4 = 0

# ------------- ALIGNEMENT ----------------
# Alignement parameters to reajust similarity
# matrix values and to define the compared
# symbols

QUOTIENT = 100
TRANSPOSITION = 1
LETTER_DIFF = 0

GAP_VALUE = -5
EXT_GAP_VALUE = -1
GAP = chr(0)
CORREC_VALUE = GAP_VALUE/2

# -------- SIGNAL SIM FUNCTIONS -----------
# parameters for signal similarity computation

# fft : 0.91; mfcc : 0.019 pour 50; cqt : 0.97
# at precision 2, 0.927 at precision 1
TETA = teta
AUDIBLE_THRESHOLD = 0.01
# fft : 35; mfcc : 60 # cqt : 140
D_THRESHOLD = d_threshold
GRAPH_COMPARISON = 0

# ----------- DATA PROCESSING --------------
# parameters for data processing

SR = 22050
HOP_LENGTH = 1024

PRECISION = 4
NB_NOTES = 48*PRECISION
NB_MFCC = 50
INIT = 0

MFCC_BIT = 0
CQT_BIT = 1
FFT_BIT = 0

if MFCC_BIT + CQT_BIT + FFT_BIT != 1:
    MFCC_BIT = 0
    CQT_BIT = 1
    FFT_BIT = 0

if CQT_BIT:
    NB_VALUES = NB_NOTES
elif MFCC_BIT:
    NB_VALUES = NB_MFCC
else:
    NB_VALUES = 0

# cqt
NOTES_PER_OCTAVE = 12*PRECISION
NOTE_MIN = 'C3'

# fft
# 0.5 for quarter_tone, 1 for
# half-tone, 2 for tone
TONE_PRECISION = 0.125
DIV = 20

TIME_STATS = 0
MFCC_NORMALISATION = 0
CLEAN_SPECTRUM = 0

# ------------- MIDI ------------------
# parameters for obtention of formal
# diagram from MIDI file

TEMPO = 120

# ------------ DISPLAY ----------------

# note : matrices are created in HSV
# H between 0 and 179
# S between 0 and 255
# V between 0 and 255

BASIC_FRAME = (0, 0, 0)  # black
BACKGROUND = (0, 0, 255)  # white
SEGMENTATION = (0, 255, 255)  # red
SEG_ERROR = (60, 255, 255)  # light green
CLASS_ERROR = (60, 255, 150)  # dark green
SILENT_FRAME = BACKGROUND



# --------- INTERFACE ---------------
# parameters to save or to show in .bmp
# or from pyplot
TO_SAVE_BMP = 0
TO_SHOW_BMP = 0
TO_SAVE_PYP = 0
TO_SHOW_PYP = 1

# to show or not the oracle at level 0
PLOT_ORACLE = 0
# to show the evolution of the formal
# diagrams
EVOL_PRINT = 1

# ------------ ALGOCOG ----------------

CORRECTION_BIT = 0
CORRECTION_BIT_COLOR = 0
SEGMENTATION_BIT = 0
WRITE_RESULTS = 0

NB_SILENCE = 1024*16

ALGO_VMO = 1
ALGO_REP = 0
ALGO_USUAL = 0

# ------------ VMO ---------------

PARCOURS = 1
INCERTITUDE = 3
SUFFIX_METHOD = 'complete'  # 'inc' ou 'complete'

SYNTHESIS = 0


class Param:
    NAME, FORMAT = None, None
    TETA = None
    min_matrix = None
    d_threshold = None

    MFCC_BIT = None
    CQT_BIT = None
    FFT_BIT = None

    DIFF_CONCORDANCE = None
    EUCLID_DISTANCE = None

    DIFF_FOURIER = None
    DIFF_DYNAMIC = None

    STRICT_EQUALITY = None
    ALIGNMENT = None

    RULE_1 = None
    RULE_2 = None
    RULE_3 = None
    RULE_4 = None
    RULE_5 = None

    CORRECTION_BIT = None

    def init(self, param):
        print("os path", os.path)
        self.NAME, self.FORMAT = os.path.splitext(param.objects.last().file.name.split('/')[-1])
        self.TETA = param.objects.last().sim_threshold  # 0.976
        self.min_matrix = param.objects.last().sim_materials
        self.d_threshold = param.objects.last().seg_threshold

        self.MFCC_BIT = param.objects.last().mfcc
        self.CQT_BIT = param.objects.last().cqt
        self.FFT_BIT = param.objects.last().fft

        self.DIFF_CONCORDANCE = param.objects.last().diff_concordance
        self.EUCLID_DISTANCE = param.objects.last().euclid_distance

        self.DIFF_FOURIER = param.objects.last().diff_fourier
        self.DIFF_DYNAMIC = param.objects.last().diff_dynamic

        self.STRICT_EQUALITY = param.objects.last().strict_equality
        self.ALIGNMENT = param.objects.last().alignment

        self.RULE_1 = param.objects.last().rule_1
        self.RULE_2 = param.objects.last().rule_2
        self.RULE_3 = param.objects.last().rule_3
        self.RULE_4 = param.objects.last().rule_4
        self.RULE_5 = param.objects.last().rule_5

        self.CORRECTION_BIT = not param.objects.last().transitory_frame

        # verification to avoid any bugs
        if self.TETA < 0:
            self.TETA = 0
            param.objects.last().sim_threshold = 0
        elif self.TETA > 1:
            self.TETA = 1
            param.objects.last().sim_threshold = 1

        if self.min_matrix < 0:
            self.min_matrix = 0
            param.objects.last().sim_materials = 0
        elif self.min_matrix > 1:
            self.min_matrix = 1
            param.objects.last().sim_materials = 1

        if self.d_threshold < 0:
            self.d_threshold = 0
            param.objects.last().seg_threshold = 0

        sum = 0
        if self.MFCC_BIT:
            sum += 1
        if self.FFT_BIT:
            sum += 1
        if self.CQT_BIT:
            sum += 1
        if sum == 0 or sum > 1:
            self.MFCC_BIT = False
            self.CQT_BIT = True
            self.FFT_BIT = False
            # TODO: Est-ce que cela modifie la BDD ? A vérifier
            param.objects.last().mfcc = False
            param.objects.last().cqt = True
            param.objects.last().fft = False

        if (self.DIFF_CONCORDANCE and self.EUCLID_DISTANCE) or (not self.DIFF_CONCORDANCE and not self.EUCLID_DISTANCE):
            self.DIFF_CONCORDANCE = True
            self.EUCLID_DISTANCE = False
            param.objects.last().diff_concordance = True
            param.objects.last().euclid_distance = False

        if (self.DIFF_FOURIER and self.DIFF_DYNAMIC) or (not self.DIFF_FOURIER and not self.DIFF_DYNAMIC):
            self.DIFF_FOURIER = True
            self.DIFF_DYNAMIC = False
            param.objects.last().diff_fourier = True
            param.objects.last().diff_dynamic = False

        if (self.STRICT_EQUALITY and self.ALIGNMENT) or (not self.STRICT_EQUALITY and not self.ALIGNMENT):
            self.ALIGNMENT = True
            self.STRICT_EQUALITY = False
            param.objects.last().strict_equality = True
            param.objects.last().alignment = False

        print("TETA", self.TETA, param.objects.last().sim_threshold)
        print("min_matrix", self.min_matrix, param.objects.last().sim_materials)
        print("d_threshold", self.d_threshold, param.objects.last().seg_threshold)
        print("MFCC", self.MFCC_BIT, param.objects.last().mfcc,
              "CQT", self.CQT_BIT, param.objects.last().cqt,
              "FFT", self.FFT_BIT, param.objects.last().fft)
        print("DIFF_CONCORDANCE", self.DIFF_CONCORDANCE, param.objects.last().diff_concordance,
              "EUCLID_DISTANCE", self.EUCLID_DISTANCE, param.objects.last().euclid_distance)
        print("DIFF_FOURIER", self.DIFF_FOURIER, param.objects.last().diff_fourier,
              "DIFF_DYNAMIC", self.DIFF_DYNAMIC, param.objects.last().diff_dynamic)
        print("STRICT_EQUALITY", self.STRICT_EQUALITY, param.objects.last().strict_equality,
              "ALIGNMENT", self.ALIGNMENT, param.objects.last().alignment)


