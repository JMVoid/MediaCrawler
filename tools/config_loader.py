# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

import os
from typing import Any
import yaml
import config # 导入根 config 模块


def load_and_override_config(config_path: str | None):
    """
    从指定的 YAML 文件加载配置，并覆盖默认的 .py 配置。
    如果未指定路径，则会依次尝试加载当前工作目录下的 'config.yaml' 和 'config.yml'。
    """
    if not config_path:
        default_paths = [
            os.path.join(os.getcwd(), "config.yaml"),
            os.path.join(os.getcwd(), "config.yml"),
        ]
        for path in default_paths:
            if os.path.exists(path):
                config_path = path
                break
        else:
            return  # 没有指定配置文件，默认路径也不存在，直接返回

    if not os.path.exists(config_path):
        print(f"[配置] 警告：指定的配置文件不存在于: {config_path}")
        return

    print(f"[配置] 从 {config_path} 加载并覆盖配置...")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)

        if not yaml_config:
            return

        # 遍历 YAML 中的每个配置块，例如 base_config:, xhs_config:
        for section_name, section_config in yaml_config.items():
            # 查找对应的配置模块，例如 config.base_config
            module_to_update = getattr(config, section_name, None)

            if module_to_update is None:
                print(f"[配置] 警告：未找到名为 '{section_name}' 的配置模块，已跳过。")
                continue

            if not isinstance(section_config, dict):
                continue

            for key, value in section_config.items():
                # 检查该配置项是否已存在于模块中
                if hasattr(module_to_update, key):
                    old_value = getattr(module_to_update, key)
                    # PyYAML 已经自动转换了类型，无需手动转换
                    print(f"  -> 在 '{section_name}' 中覆盖 '{key}': 从 '{old_value}' -> '{value}'")
                    setattr(module_to_update, key, value)

                    # 同时更新顶层的 config 模块（如果其中存在同名变量）
                    if hasattr(config, key):
                        setattr(config, key, value)
                else:
                    print(f"[配置] 警告：配置项 '{key}' 在模块 '{section_name}' 中不存在，已跳过。")

    except yaml.YAMLError as e:
        print(f"[配置] 错误：解析 YAML 配置文件失败: {e}")
    except Exception as e:
        print(f"[配置] 加载外部配置时发生未知错误: {e}")
