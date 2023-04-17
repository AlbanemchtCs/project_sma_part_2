# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 18:20:52 2023

@author: Admin
"""
import random 

class Argument:
    def __init__(self,item,type_arg,args):
        self.item = item
        self.type_arg = type_arg
        self.args = args
    def get_item(self):
        return self.item
    def __str__(self):
        if self.type_arg == 0:
            r = random.randint(0,1)
            if r== 0:
                return "Je préfère " + self.item.get_name() + " pour " + self.args[0] 
            elif r==1:
                return "Le " + self.item.get_name() + " a une bonne performance sur " + self.args[0] 
        elif self.type_arg == 1:
            r = random.randint(0,1)
            if r== 0:
                return self.item.get_name() + " est meilleur que " + self.args[1].get_name()  + " du point de vue de " + self.args[0]
            elif r==1:
                return "Par rapport au critère " + self.args[0] + " le " + self.item.get_name() + " a une meilleure performance que " + self.args[1].get_name()

        elif self.type_arg == 2:
            return self.item.get_name() + " est équivalent à " + self.args[1].get_name()  + " du point de vue de " + self.args[0]
        elif self.type_arg == 3:
            return self.args[1].get_name() + " est mauvais du point de vue de " + self.args[0]
    def __eq__(a,b):
        return a.item == b.item and a.type_arg  == b.type_arg and a.args == b.args