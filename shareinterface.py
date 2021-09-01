'''这里是自己封装的接口'''

import json

class ShareJson:
    def dumps(data:dict, path):
        '''数据写入'''
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def loads(path):
        '''读取数据'''
        with open(path, 'rb') as f:
            data = json.load(f)
        return data