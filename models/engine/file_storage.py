#!/usr/bin/python3
"""Defines the FileStorage class."""
import json

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storag.

    Attributes:
        __file_path (str): >> The name of the file to save objects to.
        __objects (dict): >> A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Return the <dictionary __objects>"""
        return FileStorage.__objects
    
    def save(self):
        """Serialize __objects to the <JSON file __file_path>"""
        obj_dict = FileStorage.__objects
        obj_dict = {obj: obj_dict[obj].to_dict() for obj in obj_dict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        ob_cl_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ob_cl_name, obj.id)] = obj


    def reload(self):
        """Deserialize the JSON file <__file_path> to __objects, if exists"""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    clsName = o["__class__"]
                    del o["__class__"]
                    self.new(eval(clsName)(**o))
        except FileNotFoundError:
            return

