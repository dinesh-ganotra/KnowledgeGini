"""Gini with Knowledge -- simulation code for "Effect of Time Rate of
Knowledge Spread on Gini Ratio" (Journal of the Knowledge Economy).

The model lives in game_of_knowledge; the parameter studies behind the
paper's figures are in studies.
"""
__version__ = "1.0"
from .game_of_knowledge import game_of_knowledge, load_data, gini, BASELINE_R_RATIO
