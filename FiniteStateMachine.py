from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional

from Transition import Transition


class FiniteStateMachine:
    class OperationalState(Enum):
        UNITIALIZED = 1
        IDLE = 2
        RUNNING = 3
        TERMINAL_REACHED = 4

    class Layout:
        def __init__(self, initial_state: Optional['State'] = None, states: Optional[list['State']] = None):
            self.states = states
            self._initial_state = initial_state if initial_state.is_valid else None
            if self.states is None:
                self.states = []
            if self.initial_state is not None:
                self.states.append(self.initial_state)

        class State:
            class Parameters:
                terminal: bool
                do_in_state_when_entering: bool = False
                do_in_state_action_when_exiting: bool = False

            def __init__(self, parameters: 'Parameters' = Parameters()):
                self.__parameters = parameters
                self.__transition: Transition = []

            @property
            def is_valid(self) -> 'bool':
                if len(self.__transition) >= 1:
                    for val in self.__transition:
                        if not val.is_valid:
                            return False
                return True

            @property
            def is_terminal(self):
                return self.__parameters.terminal

            @property
            def is_transiting(self) -> 'Transition' or None:
                if len(self.__transition) >= 1:
                    for val in self.__transition:
                        if val.is_transiting:
                            return val
                return None

            def add_transition(self, next_transition: Transition):
                if isinstance(next_transition, Transition):
                    self.__transition.append(next_transition)
                else:
                    raise Exception("Error: Expecting a Type Transition!")

            @abstractmethod
            def _do_entering_action(self):
                pass

            @abstractmethod
            def _do_in_state_action(self):
                pass

            @abstractmethod
            def _do_exiting_action(self):
                pass

            def _exec_entering_action(self):
                if self.__parameters.do_in_state_when_entering:
                    self._do_entering_action()

            def _exec_in_state_action(self):
                self._do_in_state_action()

            def _exec_exiting_action(self):
                if self.__parameters.do_in_state_action_when_exiting:
                    self._do_exiting_action()

        @property
        def is_valid(self) -> bool:
            validity = False
            if self.states.__contains__(self.initial_state):
                for a_state in self.states:
                    if a_state is isinstance(self.states, State):
                        validity = True
            return validity

        @property
        def initial_state(self) -> 'State':
            return self._initial_state

        @initial_state.setter
        def initial_state(self, new_state: 'State') -> None:
            self._initial_state = new_state

        def add_state(self, new_state: 'State') -> None:
            if new_state.is_valid:
                self.states.append(new_state)

        def add_states(self, list_states: list['State']) -> None:
            for a_state in list_states:
                if a_state.is_valid:
                    self.states.append(a_state)

    def __init__(self, layout_parameter: 'Layout', unitialized: bool = True):  # do typing layount:Layount
        self.__layout = layout_parameter
        self.__current_applicative_state = None
        self.__current_operational_state = self.OperationalState.UNITIALIZED if unitialized \
            else self.OperationalState.IDLE

    @property
    def current_applicative_state(self):
        return self.__current_applicative_state

    @current_applicative_state.setter
    def current_applicative_state(self, value: 'State'):  # do typing value:state
        self.__current_applicative_state = value

    @property
    def current_operational_state(self):
        return self.__current_operational_state

    @current_operational_state.setter
    def current_operational_state(self, value: 'OperationalState'):
        self.__current_operational_state = value

    # TODO: do timer if float isnt none
    #TODO: for loop state in layout state list
    def run(self, reset: bool = True, time_budget: float = None):
        dt = datetime.now()
        on_continue = True
        if self.__current_operational_state == self.OperationalState.UNITIALIZED:
            self.current_applicative_state = self.__layout.initial_state
            self.__current_applicative_state._exec_entering_action()

            self.current_operational_state = self.OperationalState.IDLE
        while on_continue and (time_budget is None or datetime.now() - dt < time_budget):
            on_continue = self.track()
            print("post track")
        self.current_operational_state = self.OperationalState.TERMINAL_REACHED

    def track(self) -> bool:
        on_continue = True
        self.__current_operational_state = self.OperationalState.RUNNING
        if self.__current_applicative_state is None:
            #   the last transition was to None, so load the next stage
            if len(self.__layout.states) > 0:
                self.__current_applicative_state = self.__layout.states.pop(0)

        if self.__current_applicative_state is None:
            self.__current_operational_state = self.OperationalState.TERMINAL_REACHED
            on_continue = False
        elif self.__current_applicative_state.is_transiting is not None:
            if self.__current_applicative_state.is_terminal:
                self.__current_applicative_state._exec_exiting_action()
                self.__current_operational_state = self.OperationalState.TERMINAL_REACHED
                on_continue = False
            else:
             self._transit_by(self.__current_applicative_state.is_transiting)
        else:
            self.__current_applicative_state._exec_in_state_action()
        return on_continue

    def stop(self):
        self.current_operational_state = self.OperationalState.UNITIALIZED

    def reset(self):
        self.current_operational_state = self.OperationalState.IDLE
        self.current_applicative_state = self.__layout.initial_state

    def transit_to(self, state: 'State'):
        self.__current_applicative_state._exec_exiting_action()
        self.__current_applicative_state = state
        if self.__current_applicative_state is not None:
            self.__current_applicative_state._exec_entering_action()

    def _transit_by(self, transition: 'Transition'):
        self.__current_applicative_state._exec_exiting_action()
        transition.exec_transiting_action()
        self.__current_applicative_state = transition.next_state
        if self.__current_applicative_state is not None:
            self.__current_applicative_state._exec_entering_action()






# dt = datetime.now()
# print(datetime.timestamp(dt))
