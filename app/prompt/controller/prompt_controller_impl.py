from prompt.domain.controller.prompt_controller import PromptController
import openai
from openai_response_text import OpenaiResponseText
from openai.error import RateLimitError
from common.dto.response import Response, Error, ErrorType
from prompt.domain.service.prompt_service import PromptService
from prompt.domain.service.prompt_service_builder import PromptServiceBuilder
from typing import Optional


class PromptControllerImpl(PromptController):
    prompt_service: PromptService

    def __init__(self, category: str, user_content: Optional[str] = None):
        self.prompt_service = PromptServiceBuilder().create(
            category=category,
            user_content=user_content)

    async def handle_async(self):
      try:
        params = self.prompt_service.create_prompt()
        response = await openai.ChatCompletion.acreate(**params.__dict__)
        response_raw_text = response.choices[0].message.content
        response_text = OpenaiResponseText.from_raw_text(response_raw_text)
        json_data = response_text.to_json()
        return Response(data=json_data, raw_data=response_raw_text)
      except RateLimitError as e:
        error = Error(type=ErrorType.RATE_LIMIT_ERROR, message=str(e))
        return Response(error=error, raw_data=response_raw_text)
      except Exception as e:
        error = Error(type=ErrorType.UNKNOWN_ERROR, message=str(e))
        return Response(error=error, raw_data=response_raw_text)

    def handle(self):
      try:
        params = self.prompt_service.create_prompt()
        response = openai.ChatCompletion.create(**params.__dict__)
        response_raw_text = response.choices[0].message.content
        response_text = OpenaiResponseText.from_raw_text(response_raw_text)
        json_data = response_text.to_json()
        return Response(data=json_data, raw_data=response_raw_text)
      except RateLimitError as e:
        error = Error(type=ErrorType.RATE_LIMIT_ERROR, message=str(e))
        return Response(error=error, raw_data=response_raw_text)
      except Exception as e:
        error = Error(type=ErrorType.UNKNOWN_ERROR, message=str(e))
        return Response(error=error, raw_data=response_raw_text)
