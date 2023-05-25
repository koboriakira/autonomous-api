from app.prompt.domain.dto.prompt_version import PromptVersion
from app.prompt.domain.service.prompt_service import PromptService
from app.prompt.service.prompt_service_v1 import PromptServiceV1
from app.prompt.service.prompt_service_v2 import PromptServiceV2
from app.util.yaml_loader import YamlLoader

class PromptServiceBuilder:
    @classmethod
    def create(cls, category: str) -> PromptService:
        define_data = YamlLoader.load_define(category)
        prompt_version = cls._get_prompt_version(define_data)
        match prompt_version:
            case PromptVersion.V1:
                return PromptServiceV1(category=category)
            case PromptVersion.V2:
                return PromptServiceV2(category=category)
            case _:
                raise Exception(f'Invalid prompt version: %s' % prompt_version)

    @classmethod
    def _get_prompt_version(cls, define_data) -> PromptVersion:
        if "version" in define_data:
            return PromptVersion(define_data["version"])
        else:
            return PromptVersion.V1
