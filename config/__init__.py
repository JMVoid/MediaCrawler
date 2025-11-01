# 声明：本代码仅供学习和研究目的使用。

# 导入子模块，以便通过 config.bilibili_config 的方式访问
from . import base_config
from . import bilibili_config
from . import db_config
from . import dy_config
from . import ks_config
from . import tieba_config
from . import weibo_config
from . import xhs_config
from . import zhihu_config

# 为了向后兼容，将所有配置变量扁平化到 config 模块的命名空间中。
# 注意：如果不同文件中有同名变量，后导入的会覆盖先导入的。
# 这保留了旧的、扁平化的配置访问方式，例如 config.KEYWORDS
_modules = [
    base_config, db_config, bilibili_config, dy_config,
    ks_config, tieba_config, weibo_config, xhs_config, zhihu_config
]

for _module in _modules:
    _vars = {k: v for k, v in vars(_module).items() if not k.startswith('__')}
    globals().update(_vars)
