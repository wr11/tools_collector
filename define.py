'''各种定义'''

from collections import namedtuple

CONSTANTTHEME = "推荐"

_USERDATAATTR = [
    'tool_theme',
    'tool_items',
    'tool_item_name',
    'tool_item_path',
]
USERDATAATTR = namedtuple("USERDATAATTR", _USERDATAATTR)(*_USERDATAATTR)

USER_TOOL_DATA_PATH = 'usertooldata.json'  # 工具数据文件名称