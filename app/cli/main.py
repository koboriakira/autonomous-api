import argparse
from app.cli.sub_command import SubCommand
from app.cli.option import Option

def get_args():
  parser = argparse.ArgumentParser()

  # 実装するコマンド名(ex. how-to-command)
  parser.add_argument("sub_command", type=str)

  # 以下は利用されるコマンドによって要否が変わるため、すべて任意とする
  parser.add_argument("--command", type=str)

  return parser.parse_args()

def execute():
    args = get_args()
    print("execute")
    if hasattr(args, 'sub_command'):
        sub_command = SubCommand(args.sub_command)
        print(sub_command)
    option = Option.from_args(args)
    print(option)
