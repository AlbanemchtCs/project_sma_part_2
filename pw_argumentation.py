from mesa import Model
from mesa.time import RandomActivation
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.message.Message import Message
from communication.preferences.Preferences import Profile_pref,Preferences
from communication.message.MessagePerformative import MessagePerformative
from communication.preferences.Value import Value
from communication.preferences.Item import Item
from communication.preferences.CriterionValue import CriterionValue
from communication.arguments import Argument
import pandas as pd
import numpy as np
ENGINES =  pd.read_csv("engines.csv")
DISTRIB = pd.DataFrame()
DISTRIB['min'] = ENGINES.min()
DISTRIB['max'] = ENGINES.max()
DISTRIB = DISTRIB.drop(index=['Description','Nom'])

class ArgumentAgent(CommunicatingAgent):
    """ ArgumentAgent which inherit from CommunicatingAgent. """
    def __init__(self, unique_id, model, name,list_items):
        super().__init__(unique_id, model, name)
        
        self.preference = Preferences()
        self.list_items = list_items
        self.committed = False
        self.args = []
        self.pop = 0
    def step(self):
        super().step()
        list_messages = self.get_new_messages()
        # compute all messages
        for message in list_messages:
            print(message)
                
            #case PROPOSE
            if message.get_performative() == MessagePerformative.PROPOSE:
                self.args = []
                propose = message.get_content()
                # get most prefered item
                pref  = self.list_items_left[-1]
                if self.preference.is_item_among_top_10_percent(propose, self.list_items):
                    # case proposition proposes the most prefered item
                    if propose == pref:
                        #accept
                       m = Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ACCEPT, content=pref)
                       self.send_message(m)
                
                    else:
                        # propose (impossible in our case with 5 engines)
                        m = Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.PROPOSE, content=pref)
                        self.send_message(m)
                else:
                    #ask why if engine isn't in top 10
                    m =  Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ASK_WHY, content=propose)
                    self.send_message(m)
            # case COMMIT and ACCEPT
            elif message.get_performative() == MessagePerformative.ACCEPT or message.get_performative() == MessagePerformative.COMMIT:
                if not self.committed:
                    # Can commit only one time
                    self.committed = True
                    m = Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.COMMIT, content=message.get_content())
                    self.send_message(m)
            # case ASK_WHY
            elif message.get_performative() == MessagePerformative.ASK_WHY:
                item = message.get_content()
                send_arg = self.new_argument()
                self.args.append(send_arg)
                if send_arg is None: 
                    # case choose an other item
                    if self.pop <2:
                        self.list_items_left.pop(-1)
                        other_item = self.list_items_left[-1]
                        self.args = [] 
                        self.pop += 1
                        m = Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.PROPOSE, content=other_item)
                    else:
                        m = Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.COMMIT, content=message.get_content())
                    self.send_message(m)
                else:
                    self.args.append(send_arg)
                    m = Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content = send_arg)
                    self.send_message(m)
            # Case ARGUE
            elif message.get_performative() == MessagePerformative.ARGUE:
                
                arg = message.get_content()
                self.args.append(arg)
                # first try to find a counter_argument
                new_args = self.counter_argument(arg)
                # second try to find a simple argument undiscuss with item and criterion
                if new_args is None:
                    new_args = self.new_argument()
                # else Accept
                if new_args is None:
                    # case choose an other item
                    if self.pop <2:
                        self.list_items_left.pop(-1)
                        other_item = self.list_items_left[-1]
                        self.args = [] 
                        self.pop += 1
                        m = Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.PROPOSE, content=other_item)
                    else:
                        m = Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ACCEPT, content=arg.get_item())
                    self.send_message(m)
                else:
                    # Sends the argue
                    self.args.append(new_args)
                    m = Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content= new_args)
                    self.send_message(m)
    """
    Return a new argument on the most prefered item
    """
    def new_argument(self):
        
        name_list = self.preference.get_criterion_name_list()
        val_list = [self.preference.get_value(self.list_items_left[-1],crit) for crit in name_list]
        val_list,name_list = zip(*sorted(zip(val_list,name_list)))
        for crit in name_list[:3]:
            a = Argument(self.list_items_left[-1],0,[crit])
            if not a in self.args:
                return a
            else:
                del a
        return None
    """
    return a counter_argument of arg
    """
    def counter_argument(self,arg):
        if arg.type_arg == 0:# case o_i, c_i = x
            crit = arg.args[0]
            val = self.preference.get_value(arg.item,crit)
            my_val = self.preference.get_value(self.list_items_left[-1],crit)
            if my_val > val:# case o_j, c_j > c_i
                a = Argument(self.list_items_left[-1],1,[crit,arg.item])
                if not a in self.args:
                    return a
            elif my_val == val:# case o_j, c_j = c_i
                a = Argument(self.list_items_left[-1],2,[crit,arg.item])
                if not a in self.args:
                    return a
            elif val < len(Value)/2:# case not o_i, c_i is bad
                a = Argument(self.list_items_left[-1],3,[crit,arg.item])
                if not a in self.args:
                    return a
        # case o_j, c_j>c_i exist c
        name_list = self.preference.get_criterion_name_list()
        for crit in name_list:
            val = self.preference.get_value(arg.item,crit)
            my_val = self.preference.get_value(self.list_items_left[-1],crit)
            if my_val > val:
                a = Argument(self.list_items_left[-1],1 ,[crit,arg.item])
                if not a in self.args:
                    return a
        
        return None
    """
    return preference
    """
    def get_preference(self):
        return self.preference
    """
    generate preferences with profiles
    """
    def generate_preferences(self,distrib,nb_val):
        #case profile
        self.P = Profile_pref(distrib,nb_val)
        self.preference.set_criterion_name_list(list(DISTRIB.index))
        for item in self.list_items:
            for crit in DISTRIB.index:
                self.preference.add_criterion_value(CriterionValue(item,
                                                                   crit,
                                                                  float(self.P.get_value(float(ENGINES[ENGINES['Nom'] == item.get_name()][crit]), crit))))
        self.list_items = self.preference.sorted_item_list(self.list_items)
        self.list_items_left = self.list_items
        
class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model. """
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.messages_service = MessageService(self.schedule)
        self.running = True
        
    def step(self):
        self.messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    argument_model = ArgumentModel()
    list_items = []
    for i in range(len(ENGINES)):
        list_items.append(Item(ENGINES['Nom'][i],ENGINES['Description'][i]))
    a = ArgumentAgent(1,argument_model, "agent_1",list_items)
    a.generate_preferences(DISTRIB,len(Value))
    print("ordre de préférence croissant de agent_1: ",[v.get_name() for v in a.list_items])
    b = ArgumentAgent(2,argument_model, "agent_2",list_items)
    b.generate_preferences(DISTRIB,len(Value))
    print("ordre de préférence croissant de agent_2: ",[v.get_name() for v in b.list_items])
    argument_model.schedule.add(a)
    argument_model.schedule.add(b)
    most_preferred_item = b.preference.most_preferred(list_items)
    b.send_message(Message(b.get_name(), a.get_name(), MessagePerformative.PROPOSE, most_preferred_item))
    while not a.committed or not b.committed:
        argument_model.step()

