#!/usr/bin/env python3

from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Value import Value
import numpy as np
import random

class Preferences:
    """Preferences class.
    This class implements the preferences of an agent.

    attr:
        criterion_name_list: the list of criterion name (ordered by importance)
        criterion_value_list: the list of criterion value
    """

    def __init__(self):
        """Creates a new Preferences object.
        """
        self.__criterion_name_list = []
        self.__criterion_value_list = []

    def get_criterion_name_list(self):
        """Returns the list of criterion name.
        """
        return self.__criterion_name_list

    def get_criterion_value_list(self):
        """Returns the list of criterion value.
        """
        return self.__criterion_value_list

    def set_criterion_name_list(self, criterion_name_list):
        """Sets the list of criterion name.
        """
        self.__criterion_name_list = criterion_name_list

    def add_criterion_value(self, criterion_value):
        """Adds a criterion value in the list.
        """
        self.__criterion_value_list.append(criterion_value)

    def get_value(self, item, criterion_name):
        """Gets the value for a given item and a given criterion name.
        """
        for value in self.__criterion_value_list:
            if value.get_item() == item and value.get_criterion_name() == criterion_name:
                return value.get_value()
        return None

    def is_preferred_criterion(self, criterion_name_1, criterion_name_2):
        """Returns if a criterion 1 is preferred to the criterion 2.
        """
        for criterion_name in self.__criterion_name_list:
            if criterion_name == criterion_name_1:
                return True
            if criterion_name == criterion_name_2:
                return False

    def is_preferred_item(self, item_1, item_2):
        """Returns if the item 1 is preferred to the item 2.
        """
        return item_1.get_score(self) > item_2.get_score(self)

    def most_preferred(self, item_list):
        """Returns the most preferred item from a list.
        """
        result = np.array([item.get_score(self) for item in item_list])
        best_item = item_list[result.argmax()]
        return best_item
    
    def sorted_item_list(self,item_list):
        """Returns ordered item_list with score
        """
        result = [item.get_score(self) for item in item_list]
        result,item_list  = zip(*sorted(zip(result,item_list)))
        return list(item_list)
    def is_item_among_top_10_percent(self, item, item_list):
        """
        Return whether a given item is among the top 10 percent of the preferred items.

        :return: a boolean, True means that the item is among the favourite ones
        """
        item_list = self.sorted_item_list(item_list)
        id_10_percent = len(item_list)*0.1
        item_10_percent_list = item_list[-int(id_10_percent):] if id_10_percent>1 else item_list[-1:]
        return item in item_10_percent_list

"""
Profile_pref : generate preferences with reference profiles of motor
    DISTRIB : dataframe with 'min' and 'max' of ENGINES for each columns
    nb_value : number of values at the end (if nb_value =5, 4 profile are created to split 5 values)
    type_profile : "full_random" create full random profiles (useful in our case)
"""
class Profile_pref:
    def __init__(self,DISTRIB,nb_value,type_profile = "full_random"):
        self.profile = {}
        self.name_criterion  = DISTRIB.index
        self.nb_value = nb_value
        for name_col in DISTRIB.index:
            self.profile[name_col] = []
            min_val = DISTRIB['min'][name_col]
            max_val = DISTRIB['max'][name_col]
            # stable profile
            if type_profile == "stable":
                for i in range(1,nb_value-1):
                    self.profile[name_col].append(random.uniform((i-0.25)*(max_val-min_val)/nb_value+min_val,
                                                                 (i+0.25)*(max_val-min_val)/nb_value+min_val))
            elif type_profile == "full_random":
                for i in range(1,nb_value-1):
                    self.profile[name_col].append(random.uniform(min_val,max_val))
                self.profile[name_col] = sorted(self.profile[name_col])
    """
    get_value  : return value with val of a engine on a criterion (criterion_name)
    """
    def get_value(self,val,criterion_name):
        return self.nb_value-1-float(sum(np.array(self.profile[criterion_name])<=val))

if __name__ == '__main__':
    """Testing the Preferences class.
    """
    agent_pref = Preferences()
    agent_pref.set_criterion_name_list([CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                        CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                        CriterionName.NOISE])

    diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.PRODUCTION_COST,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.CONSUMPTION,
                                                  Value.GOOD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.DURABILITY,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.ENVIRONMENT_IMPACT,
                                                  Value.VERY_BAD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.NOISE,
                                                  Value.VERY_BAD))

    electric_engine = Item("Electric Engine", "A very quiet engine")
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.PRODUCTION_COST,
                                                  Value.BAD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.CONSUMPTION,
                                                  Value.VERY_BAD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.DURABILITY,
                                                  Value.GOOD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.ENVIRONMENT_IMPACT,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.NOISE,
                                                  Value.VERY_GOOD))

    """test list of preferences"""
    print(diesel_engine)
    print(electric_engine)
    print(diesel_engine.get_value(agent_pref, CriterionName.PRODUCTION_COST))
    print(agent_pref.is_preferred_criterion(CriterionName.CONSUMPTION, CriterionName.NOISE))
    print('Electric Engine > Diesel Engine : {}'.format(agent_pref.is_preferred_item(electric_engine, diesel_engine)))
    print('Diesel Engine > Electric Engine : {}'.format(agent_pref.is_preferred_item(diesel_engine, electric_engine)))
    print('Electric Engine (for agent 1) = {}'.format(electric_engine.get_score(agent_pref)))
    print('Diesel Engine (for agent 1) = {}'.format(diesel_engine.get_score(agent_pref)))
    print('Most preferred item is : {}'.format(agent_pref.most_preferred([diesel_engine, electric_engine]).get_name()))
