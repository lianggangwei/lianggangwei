from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Union


class ElementType(Enum):
    CONTACT = "contact"
    COIL = "coil"
    TIMER = "timer"
    COUNTER = "counter"
    COMPARE = "compare"
    MATH = "math"
    JUMP = "jump"
    CALL = "call"
    END = "end"


class ContactType(Enum):
    NORMALLY_OPEN = "NO"
    NORMALLY_CLOSED = "NC"
    RISING_EDGE = "P"
    FALLING_EDGE = "N"


class TimerType(Enum):
    TON = "TON"
    TOF = "TOF"
    TONR = "TONR"


class CounterType(Enum):
    CTU = "CTU"
    CTD = "CTD"
    CTUD = "CTUD"


class CoilType(Enum):
    NORMAL = "normal"
    SET = "set"
    RESET = "reset"
    PULSE = "pulse"


@dataclass
class Position:
    row: int
    column: int


@dataclass
class LadderElement:
    element_type: ElementType
    address: str
    position: Position
    id: Optional[str] = None

    def validate_address(self) -> bool:
        if not self.address:
            return False
        return self._validate_address_format()

    def _validate_address_format(self) -> bool:
        return True


@dataclass
class Contact(LadderElement):
    contact_type: ContactType = ContactType.NORMALLY_OPEN
    element_type: ElementType = field(init=False, default=ElementType.CONTACT)

    def _validate_address_format(self) -> bool:
        valid_prefixes = ['X', 'Y', 'M', 'L', 'F', 'B', 'D', 'W', 'T', 'C']
        if len(self.address) < 2:
            return False
        prefix = self.address[0].upper()
        if prefix not in valid_prefixes:
            return False
        try:
            int(self.address[1:])
            return True
        except ValueError:
            return False


@dataclass
class Coil(LadderElement):
    coil_type: CoilType = CoilType.NORMAL
    element_type: ElementType = field(init=False, default=ElementType.COIL)

    def _validate_address_format(self) -> bool:
        valid_prefixes = ['Y', 'M', 'L', 'F', 'B']
        if len(self.address) < 2:
            return False
        prefix = self.address[0].upper()
        if prefix not in valid_prefixes:
            return False
        try:
            int(self.address[1:])
            return True
        except ValueError:
            return False


@dataclass
class Timer(LadderElement):
    timer_type: TimerType = TimerType.TON
    preset_value: int = 0
    current_value: int = 0
    time_base: str = "100ms"
    element_type: ElementType = field(init=False, default=ElementType.TIMER)

    def _validate_address_format(self) -> bool:
        if not self.address.startswith('T') and not self.address.startswith('t'):
            return False
        try:
            int(self.address[1:])
            return True
        except ValueError:
            return False

    def validate_preset(self) -> bool:
        return self.preset_value >= 0


@dataclass
class Counter(LadderElement):
    counter_type: CounterType = CounterType.CTU
    preset_value: int = 0
    current_value: int = 0
    element_type: ElementType = field(init=False, default=ElementType.COUNTER)

    def _validate_address_format(self) -> bool:
        if not self.address.startswith('C') and not self.address.startswith('c'):
            return False
        try:
            int(self.address[1:])
            return True
        except ValueError:
            return False

    def validate_preset(self) -> bool:
        return self.preset_value >= 0


@dataclass
class Rung:
    number: int
    elements: List[LadderElement] = field(default_factory=list)
    comment: str = ""
    is_active: bool = True

    def add_element(self, element: LadderElement):
        self.elements.append(element)

    def validate(self) -> tuple[bool, List[str]]:
        errors = []
        if not self.elements:
            errors.append(f"梯级 {self.number} 为空")
            return False, errors
        
        has_input = False
        has_output = False
        
        for element in self.elements:
            if isinstance(element, (Contact, Timer, Counter)):
                has_input = True
            elif isinstance(element, Coil):
                has_output = True
        
        if has_input and not has_output:
            errors.append(f"梯级 {self.number} 有输入但没有输出")
        if not has_input and has_output:
            errors.append(f"梯级 {self.number} 有输出但没有输入")
        
        return len(errors) == 0, errors


@dataclass
class LadderProgram:
    name: str = "Mitsubishi_Program"
    rungs: List[Rung] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)

    def add_rung(self, rung: Rung):
        self.rungs.append(rung)

    def get_rung(self, number: int) -> Optional[Rung]:
        for rung in self.rungs:
            if rung.number == number:
                return rung
        return None

    def validate_all(self) -> tuple[bool, List[str]]:
        all_errors = []
        all_valid = True
        
        for rung in self.rungs:
            valid, errors = rung.validate()
            if not valid:
                all_valid = False
                all_errors.extend(errors)
            
            for element in rung.elements:
                if not element.validate_address():
                    all_valid = False
                    all_errors.append(f"梯级 {rung.number}: 无效的地址 '{element.address}'")
        
        return all_valid, all_errors
