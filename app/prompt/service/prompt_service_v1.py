from prompt.domain.service.prompt_service import PromptService
from prompt.domain.model.prompt import Prompt
from util.yaml_loader import YamlLoader
import json

class PromptServiceV1(PromptService):
    def __init__(self, category: str):
        self.category = category

    def create_prompt(self) -> Prompt:
        define_data = YamlLoader.load_define(self.category)
        system_message: str = define_data["prompt"]["system"] + \
            "\n\n" + self._get_inout_example()
        return Prompt.of(
            messages=[
                {
                    "role": "system",
                    "content": system_message
                }
            ],
            model=define_data["model"] if "model" in define_data else None,
            max_tokens=define_data["max_tokens"] if "max_tokens" in define_data else None,
            n=define_data["n"] if "n" in define_data else None,
            stop=define_data["stop"] if "stop" in define_data else None,
            temperature=define_data["temperature"] if "temperature" in define_data else None,
            timeout=define_data["timeout"] if "timeout" in define_data else None,
        )

    def _get_inout_example(self) -> str:
        sample_data = YamlLoader.load_sample(self.category)
        result = ""
        for idx, item in enumerate(sample_data):
            if "input" in item:
                pass
            if "output" in item:
                result += f"\n## 出力例{idx+1}\n\n"
                result += json.dumps(item["output"], ensure_ascii=False)
                result += "\n"
        result = result.strip()
        return result
