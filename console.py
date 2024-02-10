#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import stOrAgE
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def pARse_cAse(arg):
    cuRlyBrAces = re.search(r"\{(.*?)\}", arg)
    bRAckEts = re.search(r"\[(.*?)\]", arg)
    if cuRlyBrAces is None:
        if bRAckEts is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lExER = split(arg[:bRAckEts.span()[0]])
            rETL_1 = [i.strip(",") for i in lExER]
            rETL_1.append(bRAckEts.group())
            return rETL_1
    else:
        lExER = split(arg[:cuRlyBrAces.span()[0]])
        rETL_1 = [i.strip(",") for i in lExER]
        rETL_1.append(cuRlyBrAces.group())
        return rETL_1


class Command_HbNb(cmd.Cmd):
    """Defines the HolbertonBnB comM_and interpreter.

    Attributes:
        prompt (str): The comM_and prompt.
    """

    prompt = "(hbnb) "
    classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def empty_line(self):
        """Do nothing upon receiving an empty line."""
        pass

    def defAult(self, aRg):
        """Default behavior for cmd module when input is invalid"""
        arg_dICt = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "cOuNt": self.do_count,
            "update": self.do_update
        }
        mAtC_h = re.search(r"\.", aRg)
        if mAtC_h is not None:
            aRg_l = [aRg[:mAtC_h.span()[0]], aRg[mAtC_h.span()[1]:]]
            mAtC_h = re.search(r"\((.*?)\)", aRg_l[1])
            if mAtC_h is not None:
                comM_and = [aRg_l[1][:mAtC_h.span()[0]], mAtC_h.group()[1:-1]]
                if comM_and[0] in arg_dICt.keys():
                    call = "{} {}".format(aRg_l[0], comM_and[1])
                    return arg_dICt[comM_and[0]](call)
        print("*** Unknown syntax: {}".format(aRg))
        return False

    def doquit(self, aRg):
        """Quit comM_and to exit the program."""
        return True

    def doEOF(self, aRg):
        """EOF signal to exit the program."""
        print("")
        return True

    def docreate(sElF, aRg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        aRg_l = pARse_cAse(aRg)
        if len(aRg_l) == 0:
            print("** class name missing **")
        elif aRg_l[0] not in Command_HbNb.classes:
            print("** class doesn't exist **")
        else:
            print(eval(aRg_l[0])().id)
            stOrAgE.save()

    def doshow(self, aRg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        aRg_l = pARse_cAse(aRg)
        oBj_dICt = storage.all()
        if len(aRg_l) == 0:
            print("** class name missing **")
        elif aRg_l[0] not in Command_HbNb.classes:
            print("** class doesn't exist **")
        elif len(aRg_l) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(aRg_l[0], aRg_l[1]) not in oBj_dICt:
            print("** no instance found **")
        else:
            print(oBj_dICt["{}.{}".format(aRg_l[0], aRg_l[1])])

    def dodestroy(self, aRg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        aRg_l = pARse_cAse(aRg)
        oBj_dICt = stOrAgE.all()
        if len(aRg_l) == 0:
            print("** class name missing **")
        elif aRg_l[0] not in Command_HbNb.classes:
            print("** class doesn't exist **")
        elif len(aRg_l) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(aRg_l[0], aRg_l[1]) not in oBj_dICt.keys():
            print("** no instance found **")
        else:
            del oBj_dICt["{}.{}".format(aRg_l[0], aRg_l[1])]
            stOrAgE.save()

    def doall(self, aRg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        aRg_l = pARse_cAse(aRg)
        if len(aRg_l) > 0 and aRg_l[0] not in Command_HbNb.classes:
            print("** class doesn't exist **")
        else:
            oBjE_l = []
            for obj in stOrAgE.all().values():
                if len(aRg_l) > 0 and aRg_l[0] == obj.__class__.__name__:
                    oBjE_l.append(obj.__str__())
                elif len(aRg_l) == 0:
                    oBjE_l.append(obj.__str__())
            print(oBjE_l)

    def docount(self, aRg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        aRg_l = pARse_cAse(aRg)
        cOuNt = 0
        for obj in stOrAgE.all().values():
            if aRg_l[0] == obj.__class__.__name__:
                cOuNt += 1
        print(cOuNt)

    def doupdate(self, aRg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        aRg_l = pARse_cAse(aRg)
        oBj_dICt = stOrAgE.all()

        if len(aRg_l) == 0:
            print("** class name missing **")
            return False
        if aRg_l[0] not in Command_HbNb.classes:
            print("** class doesn't exist **")
            return False
        if len(aRg_l) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(aRg_l[0], aRg_l[1]) not in oBj_dICt.keys():
            print("** no instance found **")
            return False
        if len(aRg_l) == 2:
            print("** attribute name missing **")
            return False
        if len(aRg_l) == 3:
            try:
                type(eval(aRg_l[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(aRg_l) == 4:
            obj = oBj_dICt["{}.{}".format(aRg_l[0], aRg_l[1])]
            if aRg_l[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[aRg_l[2]])
                obj.__dict__[aRg_l[2]] = valtype(argl[3])
            else:
                obj.__dict__[aRg_l[2]] = aRg_l[3]
        elif type(eval(aRg_l[2])) == dict:
            obj = oBj_dICt["{}.{}".format(aRg_l[0], aRg_l[1])]
            for k, v in eval(aRg_l[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        stOrAgE.save()


if __name__ == "__main__":
    Command_HbNb().cmdloop()
