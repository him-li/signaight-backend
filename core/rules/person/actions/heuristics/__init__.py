from .courage import CourageActions
from .curiosity import CuriosityActions
from .decision_making import DecisionMakingActions
from .flexibility import FlexibilityActions
from .interpersonal_skills import InterpersonalSkillsActions
from .language_skills import LanguageSkillsActions
from .moral_values import MoralValuesActions
from .resilience import ResilienceActions
from .teamwork import TeamworkActions
from .work_under_pressure import WorkUnderPressureActions
from .skills import SkillsActions
from .volunteering_experience import VolunteeringExperienceActions


class HeuristicsActions(CourageActions,
                        CuriosityActions,
                        DecisionMakingActions,
                        FlexibilityActions,
                        InterpersonalSkillsActions,
                        LanguageSkillsActions,
                        MoralValuesActions,
                        ResilienceActions,
                        TeamworkActions,
                        WorkUnderPressureActions,
                        SkillsActions,
                        VolunteeringExperienceActions
                        ):
    pass
