from model.Cells.CrystalGrainCell import CrystalGrainCell
from model.RuleSets.NucleationRuleSet import NucleationRuleSet


class RecristalizationRuleSet(NucleationRuleSet):
    cell_type = CrystalGrainCell
    required_dimension = 2

    def __init__(self, iteration=0):
        super().__init__()
        self.iteration = iteration
        self.dislocations = 100
        self.border_dislocation_rate = 2.
        self.cell_dislocation_rate = 0.5




