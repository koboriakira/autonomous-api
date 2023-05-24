import os
import yaml

class YamlLoader:
    PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    PROMPT_DIR_PATH = 'app/prompts'
    FILE_PATH_DEFINE_YAML = 'define.yaml'
    FILE_PATH_SAMPLE_YAML = 'sample.yaml'
    @classmethod
    def load(cls, category: str, file_name: str):
        with open(f'%s/%s/%s/%s' % (cls.PROJECT_ROOT_PATH,
                                    cls.PROMPT_DIR_PATH,
                                    category,
                                    file_name)) as file:
            return yaml.safe_load(file)

    @classmethod
    def load_define(cls, category: str):
        return cls.load(category, cls.FILE_PATH_DEFINE_YAML)

    @classmethod
    def load_sample(cls, category: str):
        return cls.load(category, cls.FILE_PATH_SAMPLE_YAML)
