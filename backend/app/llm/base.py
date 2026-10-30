from abc import ABC,abstractmethod
from typing import Any,Dict,Optional


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt : Optional[str] = None, schema: Optional[Dict[str, Any]] = None) -> str :
      """Génére une aréponse a partir d'un prompt."""
    pass