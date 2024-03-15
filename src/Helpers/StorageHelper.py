import os
import json
import jsonpickle
from pprint import pprint

class StorageHelper:
    def __init__(self, path, name):
        self.name = name
        self.path = "{path}/{name}.json".format(path = path, name = name)
        if not os.path.exists(self.path):
            listStr = self._serialize([])
            self._setAll(listStr)

    def create(self, id, obj):
        # obj to dict
        dict = json.dumps(vars(obj))
        
        listStr = self._getAll()
        listDict = json.loads(listStr)[self.name]

        listDict.append({'id': id, 'value': dict})

        i = 0

        while (i < len(listDict)):
            if (type(listDict[i]['value']) is str):
                listDict[i]['value'] = json.loads(listDict[i]['value'])
            i += 1

        listStr = self._serialize(listDict)
        
        self._setAll(listStr)

        return True

    def read(self, id):
        listStr = self._getAll()
        listDict = json.loads(listStr)[self.name]

        for dict in listDict:
            if (dict['id'] == id):
                return dict['value']

        return {}

    def update(self, id, dict):
        listStr = self._getAll()
        listDict = json.loads(listStr)[self.name]

        i = 0
        while i < len(listDict):
            if (listDict[i]['id'] == id):
                listDict[i]['value'] = dict

                listStr = self._serialize(listDict)

                self._setAll(listStr)
                return True
            i += 1

        return False

    def delete(self, id):
        listStr = self._getAll()
        listDict = json.loads(listStr)[self.name]

        i = 0
        while i < len(listDict):
            if (listDict[i]['id'] == id):
                listDict.pop(i)

                listStr = self._serialize(listDict)

                self._setAll(listStr)
                return True
            i += 1

        return False

    def readAll(self):
        newListDict = []
        listStr = self._getAll()
        listDict = json.loads(listStr)[self.name]

        for dict in listDict:
            newListDict.append(dict['value'])

        return newListDict

    def _serialize(self, listDict):
        dict = {self.name: listDict}
        str = json.dumps(dict, indent = 4)
        return str

    def _setAll(self, str):
        with open(self.path, "w+") as f:
            f.write(str)

    def _getAll(self):
        with open(self.path) as f:
            listStr = ''.join(f.readlines())

            return listStr
