from app.prompt.domain.service.prompt_service import PromptService
from app.prompt.domain.model.prompt import Prompt
from app.util.yaml_loader import YamlLoader
import json
from typing import Any, Optional
from app.util.logger import get_logger
logger = get_logger(__name__)

class PromptServiceV2(PromptService):

    def __init__(self, category: str):
        self.category = category

    def create_prompt(self, user_content: Optional[dict] = None) -> Prompt:
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

        # プロンプトにあたるsystemのmessageを定義
        outline = self._create_outline(define_data)
        input_format = self._create_input_format(sample_data)
        output_format = self._create_output_format(sample_data)
        constraint = self._create_constraint(define_data)
        inout_sample = self._create_inout_sample(sample_data)
        system_message: str = outline + "\n\n" + input_format + "\n\n" + output_format + "\n\n" + constraint + "\n\n" + inout_sample

        # 引数のmessageを作成
        messages = []
        messages.append({
            "role": "system",
            "content": system_message
        })
        user_message = self._create_user_content(user_content)
        if user_message is not None:
            messages.append(user_message)

        return Prompt.of(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            n=n,
            stop=stop,
            temperature=temperature,
            timeout=timeout
        )

    def _create_user_content(self, user_content: str) -> Optional[dict[str, Any]]:
        if user_content == "":
            return None
        return {
            "role": "user",
            "content": json.dumps(user_content, ensure_ascii=False)
        }

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
        if "input" not in sample_data:
            return ""
        input_formats:dict[str, Any] = sample_data["input"]
        result = "## 入力の形式\n\n"
        for key, format in input_formats.items():
            description: str = format["description"]
            result += f"・{key}: {description}\n"
        return result.strip()

    def _create_output_format(self, sample_data) -> str:
        if "output" not in sample_data:
            return ""
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
