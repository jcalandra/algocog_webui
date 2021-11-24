import time
import os
import matplotlib.pyplot as plt
from .signal_mso import algo_cog
from website.settings import BASE_DIR
from acwebui.src.parameters import PATH_OBJ
from acwebui.src.parameters import Param
from acwebui.models import parameter
from acwebui.models import formalDiagram

# import formal_diagram_mso as fd_mso

# This is the main loop for the whole cognitive algorithm


# ======================================= COGNITIVE ALGORITHM MAIN FUNCTION ============================================
def mso_exec():
    """ Main function of the cognitive algorithm."""
    params = Param()
    params.init(parameter)
    print("TETA=", params.TETA, "CQT_BIT=", params.CQT_BIT, "d_threshold=", params.d_threshold)
    path = PATH_OBJ + params.NAME + params.FORMAT
    start_time_full = time.time()

    level_max = -1
    tab_f_oracle = []
    audio = []
    mso_oracle = [level_max, tab_f_oracle, audio]

    algo_cog(path, mso_oracle, params)
    print("Temps d execution de l'algorithme entier : %s secondes ---" % (time.time() - start_time_full))

    new_fd = []
    FD = formalDiagram()

    # printing the results in the shell
    for i in range(len(mso_oracle[1])):
        new_fd.append([tab_f_oracle[i][0].data[j]
                       for j in range(1, len(tab_f_oracle[i][0].data))])
        print("new_fd_" + str(i) + ": ", new_fd[i])
        print("link_" + str(i) + ": ", mso_oracle[1][i][1])
        print("history next : ", mso_oracle[1][i][2])
        print("matrix_next : ", mso_oracle[1][i][6])
        FD.add(os.path.join(BASE_DIR, 'uploads/photos/') + str(i) + ".png")
    plt.pause(10)
    plt.close('all')


#mso_exec()
