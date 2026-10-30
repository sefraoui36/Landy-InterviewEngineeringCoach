from typing import List, Dict, Any

class InterviewSession:
    def __init__(self, plan: Dict[str, Any]):
        self.questions: List[Dict[str, str]] = plan.get("questions", [])
        self.current_index = 0
        self.history: List[Dict[str, str]] = []

    def get_current_question(self) -> str:
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]["texte"]
        return "L'entretien est terminé."

    def add_user_response(self, response: str):
        if self.current_index < len(self.questions):
            q = self.questions[self.current_index]
            self.history.append({"question": q["texte"], "reponse": response})
            self.current_index += 1