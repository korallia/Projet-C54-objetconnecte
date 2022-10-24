from ActionState import ActionState
from State import State
from abc import abstractmethod

class MonitoredState:
        
    def __init__(self, parameters: State.Parameters):
        ActionState.__init__(parameters)
        self.__counter_last_entry: complex = 0
        self.__counter_last_exit: complex = 0
        self.__entry_count: int = 0
        self.custom_value: any
    
    @property
    def entry_count(self):
        return self.__entry_count
    
    @property
    def last_entry_time(self):
        return self.__counter_last_entry
    
    @property
    def last_exit_time(self):
        return self.__counter_last_exit
    
    def reset_entry_count(self):
        self.__entry_count = 0
    
    def resert_last_times(self):
        self.__counter_last_entry = 0
        self.__counter_last_exit = 0
    
    @abstractmethod
    def exec_entering_action(self):
        ActionState.do_entering_action(self)
        
    @abstractmethod
    def exec_exiting_action(self):
        ActionState.do_exiting_action(self)