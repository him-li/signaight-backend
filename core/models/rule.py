from typing import Dict, List, Optional, Any
from .base import SignAIghtSchema


class RuleCondition(SignAIghtSchema):
    name: str
    operator: str
    value: Any = None
    params: Optional[Dict] = None


class RuleConditions(SignAIghtSchema):
    all: Optional[List[RuleCondition]] = None
    any: Optional[List[RuleCondition]] = None


class RuleAction(SignAIghtSchema):
    name: str
    params: Optional[Dict] = None


class Rule(SignAIghtSchema):
    label: str
    conditions: RuleConditions
    actions: List[RuleAction]
