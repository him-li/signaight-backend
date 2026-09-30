from .work_under_pressure import WorkUnderPressureVariables
from .moral_values import MoralValuesVariables
from .language_skills import LanguageSkillsVariables
from .interpersonal_skills import InterpersonalSkillsVariables
from .decision_making import DecisionMakingVariables
from .curiosity import CuriosityVariables
from .teamwork import TeamworkVariables
from .resilience import ResilienceVariables


class HeuristicsVariables(WorkUnderPressureVariables,
                          MoralValuesVariables,
                          LanguageSkillsVariables,
                          InterpersonalSkillsVariables,
                          DecisionMakingVariables,
                          CuriosityVariables,
                          TeamworkVariables,
                          ResilienceVariables
                          ):
    pass
