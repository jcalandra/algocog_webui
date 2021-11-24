from .oracle_mso import create_oracle
from .formal_diagram_mso import print_formal_diagram_init

# The function that initialize the Multi_Scale Oracle is defined in this file


# ============================================ MULTI-SCALED ORACLE =====================================================
def structure_init(flag, level):
    """Initialize the Multi-Scale Oracle."""
    f_oracle = create_oracle(flag)
    link = [0]
    history_next = []
    concat_obj = ''
    formal_diagram = []
    formal_diagram_graph = print_formal_diagram_init(level)
    matrix = ["", []]
    return f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix
