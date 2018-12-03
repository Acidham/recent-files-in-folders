import json
"""
Alfred Script Filter generator class
Version: 0.93
"""


class Items:

    def __init__(self):
        self.item = {}
        self.items = []
        self.mods = {}

    def setKv(self, key, value):
        """
        Set a key value pair to item
        :param key: Name of the Key (str)
        :param value: value (str)
        """
        self.item.update({key: value})

    def addItem(self):
        """
        finally add an item to the items
        """
        self.items.append(self.item)
        self.item = {}
        self.mods = {}

    def setItem(self, **kwargs):
        """
        Add multiple key values to define an item
        :param kwargs: title,subtitle,arg,valid,quicklookurl,uid,automcomplete,type
        """
        for key, value in kwargs.items():
            self.setKv(key, value)

    def getItem(self, d_type=""):
        """
        get current item definition for validation
        :param d_type: defines returned data format; "JSON" if readable
        json is required for debugging purpose
        :return: readable JSON or JSON data
        """
        if d_type == "":
            return self.item
        else:
            return json.dumps(self.item, indent=4)

    def getItems(self, d_type="dict"):
        """
        get the final items data for which represents
        the script filter output
        :param d_type: defines returned data format; "json" if readable "dict" for processing data
        json is required for debugging purpose
        :return: readable JSON or JSON data
        """
        valid_keys = {"json", "dict"}
        if d_type not in valid_keys:
            raise ValueError("Type must be in: %s" % valid_keys)
        the_items = {}
        the_items.update({"items": self.items})
        if d_type == "dict":
            return the_items
        elif d_type == "json":
            return json.dumps(the_items, indent=4)

    def setIcon(self, m_path, m_type=""):
        """
        Set the icon of an item
        :param m_path: File path to the icon
        :param m_type: icon,fileicon or png
        """
        self.setKv("icon", self.__define_icon(m_path, m_type))

    def __define_icon(self,path,m_type=""):
        """
        Private method to create icon set
        :param path: str
        :param m_type: str
        :return: icon dict
        """
        icon = {}
        if m_type != "":
            icon.update({"type": m_type})
        icon.update({"path": path})
        return icon

    def addMod(self, key, arg, subtitle, valid=True, icon_path="", icon_type=""):
        """
        add a mod to an item
        :param key: "alt","cmd","shift" (str)
        :param arg: str
        :param subtitle: str
        :param valid: "true" | "false" (str)
        :param icon_path: str
        :param icon_type: str
        """
        valid_keys = {"alt","cmd","shift","ctrl"}
        if key not in valid_keys:
            raise ValueError("Key must be in: %s" % valid_keys)
        mod = {}
        mod.update({"arg":arg})
        mod.update({"subtitle":subtitle})
        mod.update({"valid":valid})
        if icon_path != "":
            the_icon = self.__define_icon(icon_path,icon_type)
            mod.update({"icon":the_icon})
        self.mods.update({key:mod})

    def addModsToItems(self):
        """
        Finally add mods to the items
        """
        self.setKv("mods", self.mods)

    def updateItem(self, id, key, value):
        """
        Update an Alfred script filter item key with a new value
        :param id: int, list index
        :param key: str, key which needs to be updated
        :param value: int or str, new value
        """
        dict_item = self.items[id]
        kv = dict_item[key]
        dict_item[key] = kv + value
        self.items[id] = dict_item



