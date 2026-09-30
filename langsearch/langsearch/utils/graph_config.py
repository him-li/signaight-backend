from pathlib import Path
from pylitmus import create_engine, Rule, Severity, DecisionTier
from typing import Optional, Dict
from yaml import safe_load as yaml_safe_load

def load_graph_config(path: Path) -> dict | None:
    try:
        with path.open() as fp:
            agent_config_dict = yaml_safe_load(fp)
    except Exception as e:
        print(str(e))
        return None
    agent_config = agent_config_dict.get('config', {})

    if flows := agent_config.get('flows', {}):
        for key, flow in flows.items():
            for node_name, node_config in flow.items():
                if node_name == 'config':
                    continue
                rule_defualts = {
                    'name': node_name,
                    'description': node_name,
                    'category': 'NODES',
                    'severity': Severity.HIGH
                }
                for i, rule in enumerate(node_config.get('rules', [])):
                    rule['code'] = f"{node_name}_{i}"
                    node_config['rules'][i] = Rule(**{**rule_defualts, **rule})
                node_config['decision_tiers'] = [DecisionTier(**dt)
                    for dt in node_config.get('decision_tiers', [])]
                # inject adopted node config
                agent_config['flows'][key][node_name] = node_config
    return agent_config
