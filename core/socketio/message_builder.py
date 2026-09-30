class MessageBuilder:
    @staticmethod
    def action_builder_fetch(entity):
        return {
            "request_type": "http",
            "method": "get",
            "ident": f"urn:signaight:{entity}"
        }

    @classmethod
    def build_message(
            cls,
            entity_type,
            entity_id,
            title,
            body,
            additional_actions=None):
        actions = [cls.action_builder_fetch(entity_type)]
        if additional_actions:
            actions.extend(additional_actions)
        return {
            "type": "info",
            "context": f"urn:signaight:{entity_type}:uuid:{entity_id}",
            "title": title,
            "body": body,
            "actions": actions
        }

    @classmethod
    def search_message(cls, search_id, status):
        title = f"{status.capitalize()} Search"
        body = f"Search {search_id} was {status.lower()}"
        additional_actions = ([cls.action_builder_fetch("persons")] if
                              status != "seen" else None)
        return cls.build_message(
            "events/search",
            search_id,
            title,
            body,
            additional_actions)

    @classmethod
    def active_search_message(cls, active_search_id, status):
        title = f"{status.capitalize()} Active Search"
        body = f"Search {active_search_id} was {status.lower()}"
        additional_actions = ([cls.action_builder_fetch("events")] if
                              status != "seen" else None)
        return cls.build_message(
            "events/active_search",
            active_search_id,
            title,
            body,
            additional_actions)

    @classmethod
    def recalculation_message(cls, recalculation_id, status):
        title = f"{status.capitalize()} Recalculation"
        body = f"Recalculation {recalculation_id} was {status.lower()}"
        additional_actions = ([cls.action_builder_fetch("events")] if
                              status != "seen" else None)
        return cls.build_message(
            "events/recalculation",
            recalculation_id,
            title,
            body,
            additional_actions)

    @classmethod
    def project_message(cls, project_id, action):
        title = f"{action.capitalize()} Project"
        body = f"Project {project_id} was {action.lower()}"
        return cls.build_message("projects", project_id, title, body)

    @classmethod
    def person_message(cls, person_id, action, project_id=None):
        if project_id:
            title = f"{action.capitalize()} Person"
            body = f"Persons added to project {project_id}"
        else:
            title = f"{action.capitalize()} Person"
            body = f"Person {person_id} was {action.lower()}"
        return cls.build_message(
            "persons",
            person_id or project_id,
            title,
            body)
    
    @classmethod
    def persons_batch_delete_message(cls, action: str, count:int=""):
        title = f"{action.capitalize()}"
        body = f"Batch deletion of {count} persons {action.lower()}"
        return cls.build_message(
            "persons_batch_deleted",
            count,
            title,
            body)
