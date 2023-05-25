from enum import Enum
from app.prompt.controller.prompt_controller_impl import PromptControllerImpl

class SubCommand(Enum):
    HEALTHCHECK = "healthcheck"
    HOW_TO_COMMAND = "how_to_command"

    def create_prompt_controller(self):
        return PromptControllerImpl(category=str(self.value))
