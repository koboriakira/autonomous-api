import argparse
import openai
import os
from app.prompt.controller.prompt_controller_impl import PromptControllerImpl
from app.resolver.controller.slack_controller_impl import SlackControllerImpl
from app.api.v1.api import ApiV1
from app.cli.sub_command import SubCommand
from app.cli.option import Option
from app.util.logger import get_logger
logger = get_logger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_args():
  parser = argparse.ArgumentParser()

  # 実装するコマンド名(ex. how-to-command)
  parser.add_argument("sub_command", type=str)

  # 以下は利用されるコマンドによって要否が変わるため、すべて任意とする
  parser.add_argument("--command", type=str)

  return parser.parse_args()

def execute():
    args = get_args()
    sub_command = SubCommand(args.sub_command)
    option = Option.from_args(args)
    prompt_controller = sub_command.create_prompt_controller()
    slack_controller = _get_slack_controller()
    api = ApiV1(prompt_controller=prompt_controller,
                slack_controller=slack_controller)
    user_content = option.to_user_content()
    response = api.execute(user_content=user_content)
    if response.is_ok():
        print(response.data["result"])
    else:
        print(response.error.message)

def _get_slack_controller():
    if os.getenv("SLACK_BOT_USER_OAUTH_TOKEN") is None:
        return None
    if os.getenv("SLACK_CHANNEL") is None:
        return None
    return SlackControllerImpl(
        bot_user_oauth_token=os.getenv("SLACK_BOT_USER_OAUTH_TOKEN"),
        channel="#" + os.getenv("SLACK_CHANNEL"))

if __name__ == "__main__":
    execute()
