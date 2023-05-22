from prompt.domain.service.prompt_service import PromptService
from prompt.domain.model.prompt import Prompt
from util.yaml_loader import YamlLoader
import json
from typing import Any

class PromptServiceV2(PromptService):


    def __init__(self, category: str):
        self.category = category

    def create_prompt(self) -> Prompt:
        # yamlファイルをロード
        define_data = self._load_define()
        sample_data = self._load_sample()

        # message以外のパラメータを定義
        model = define_data["model"] if "model" in define_data else None
        max_tokens = define_data["max_tokens"] if "max_tokens" in define_data else None
        n = define_data["n"] if "n" in define_data else None
        stop = define_data["stop"] if "stop" in define_data else None
        temperature = define_data["temperature"] if "temperature" in define_data else None
        timeout = define_data["timeout"] if "timeout" in define_data else None

        # messageを定義
        outline = self._create_outline(define_data)
        input_format = self._create_input_format(sample_data)
        output_format = self._create_output_format(sample_data)
        constraint = self._create_constraint(define_data)
        inout_sample = self._create_inout_sample(sample_data)
        system_message: str = outline + "\n\n" + input_format + "\n\n" + output_format + "\n\n" + constraint + "\n\n" + inout_sample

        return Prompt.of(
            messages=[
                {
                    "role": "system",
                    "content": system_message
                }
            ],
            model=model,
            max_tokens=max_tokens,
            n=n,
            stop=stop,
            temperature=temperature,
            timeout=timeout
        )

    def _create_inout_sample(self, sample_data) -> str:
        result = ""
        for idx, item in enumerate(sample_data["samples"]):
            if "input" in item:
                result += f"\n## 入力例{idx+1}\n\n"
                result += json.dumps(item["input"], ensure_ascii=False)
                result += "\n"
            if "output" in item:
                result += f"\n## 出力例{idx+1}\n\n"
                result += json.dumps(item["output"], ensure_ascii=False)
                result += "\n"
        result = result.strip()
        return result


    def _create_outline(self, define_data) -> str:
        title = define_data["prompt"]["title"]
        return """あなたは%sです。
以下の「入力の形式」「出力の形式」「制約」「入力例」「出力例」をもとに、JSON文字列を出力してください。""" % title

    def _create_constraint(self, define_data) -> str:
        constraints = define_data["prompt"]["constraint"]
        result = "## 制約\n\n"
        for constraint in constraints:
            result += f"・{constraint}\n"
        return result.strip()

    def _create_input_format(self, sample_data) -> str:
        input_formats:dict[str, Any] = sample_data["input"]
        result = "## 入力の形式\n\n"
        for key, format in input_formats.items():
            description: str = format["description"]
            result += f"・{key}: {description}\n"
        return result.strip()

    def _create_output_format(self, sample_data) -> str:
        output_formats: dict[str, Any] = sample_data["output"]
        result = "## 出力の形式\n\n"
        for key, format in output_formats.items():
            description: str = format["description"]
            result += f"・{key}: {description}\n"
        return result.strip()

    def _load_define(self):
        return YamlLoader.load_define(self.category)

    def _load_sample(self):
        return YamlLoader.load_sample(self.category)
