import openai
from typing import Optional
from openai.error import RateLimitError
from app.prompt.domain.controller.prompt_controller import PromptController
from app.prompt.domain.model.openai_response_text import OpenaiResponseText
from app.common.dto.response import Response, Error, ErrorType
from app.prompt.domain.service.prompt_service import PromptService
from app.prompt.domain.service.prompt_service_builder import PromptServiceBuilder
from app.util.logger import get_logger
logger = get_logger(__name__)


class PromptControllerImpl(PromptController):
    prompt_service: PromptService
    unique_id: int

    def __init__(self, category: str):
        self.prompt_service = PromptServiceBuilder().create(category=category)
        self.unique_id = id(self)

    async def handle_async(self, user_content: Optional[dict] = None):
      try:
        params = self.prompt_service.create_prompt(user_content=user_content)
        logger.info("prompt: %s" % str(params.messages))
        logger.info("[%s]execute openai.ChatCompletion.acreate" % self.unique_id)
        response = await openai.ChatCompletion.acreate(**params.__dict__)
        response_raw_text = response.choices[0].message.content
        response_text = OpenaiResponseText.from_raw_text(response_raw_text)
        json_data = response_text.to_json()
        logger.info("[%s] %s" % (self.unique_id, json_data))
        return Response(data=json_data, raw_data=response_raw_text)
      except RateLimitError as e:
        error = Error(type=ErrorType.RATE_LIMIT_ERROR, message=str(e))
        return Response(error=error)
      except Exception as e:
        error = Error(type=ErrorType.UNKNOWN_ERROR, message=str(e))
        return Response(error=error)

    def handle(self, user_content: Optional[dict] = None):
      try:
        params = self.prompt_service.create_prompt(user_content=user_content)
        logger.info("prompt: %s" % str(params.messages))
        logger.info("[%s]execute openai.ChatCompletion.create" %
                    self.unique_id)
        response = openai.ChatCompletion.create(**params.__dict__)
        response_raw_text = response.choices[0].message.content
        response_text = OpenaiResponseText.from_raw_text(response_raw_text)
        json_data = response_text.to_json()
        logger.info("[%s] %s" % (self.unique_id, json_data))
        return Response(data=json_data, raw_data=response_raw_text)
      except RateLimitError as e:
        error = Error(type=ErrorType.RATE_LIMIT_ERROR, message=str(e))
        return Response(error=error)
      except Exception as e:
        error = Error(type=ErrorType.UNKNOWN_ERROR, message=str(e))
        return Response(error=error)
