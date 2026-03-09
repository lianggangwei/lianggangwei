from typing import List, Tuple, Set, Dict
from .elements import (
    LadderProgram, Rung, LadderElement,
    Contact, Coil, Timer, Counter,
    ContactType, CoilType
)


class ValidationError:
    def __init__(self, message: str, rung_number: int = None, element: LadderElement = None, severity: str = "error"):
        self.message = message
        self.rung_number = rung_number
        self.element = element
        self.severity = severity
    
    def __str__(self):
        if self.rung_number:
            return f"[{self.severity.upper()}] 梯级 {self.rung_number}: {self.message}"
        return f"[{self.severity.upper()}] {self.message}"


class LadderValidator:
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
    
    def validate(self, program: LadderProgram) -> Tuple[bool, List[ValidationError], List[ValidationError]]:
        self.errors = []
        self.warnings = []
        
        self._validate_program_structure(program)
        self._validate_addresses(program)
        self._validate_duplicate_coils(program)
        self._validate_timer_counter_presets(program)
        self._validate_rung_logic(program)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_program_structure(self, program: LadderProgram):
        if not program.rungs:
            self.errors.append(ValidationError("程序为空，没有梯级", severity="error"))
            return
        
        rung_numbers = [rung.number for rung in program.rungs]
        if len(rung_numbers) != len(set(rung_numbers)):
            self.errors.append(ValidationError("存在重复的梯级编号", severity="error"))
        
        expected = 1
        for rung in program.rungs:
            if rung.number != expected:
                self.warnings.append(ValidationError(f"梯级编号不连续，期望 {expected}，实际 {rung.number}", severity="warning"))
            expected = rung.number + 1
    
    def _validate_addresses(self, program: LadderProgram):
        for rung in program.rungs:
            for element in rung.elements:
                if not element.address:
                    self.errors.append(ValidationError("元素地址为空", rung.number, element, severity="error"))
                    continue
                
                if not element.validate_address():
                    self.errors.append(ValidationError(f"无效的地址格式: '{element.address}'", rung.number, element, severity="error"))
    
    def _validate_duplicate_coils(self, program: LadderProgram):
        coil_addresses: Dict[str, List[int]] = {}
        
        for rung in program.rungs:
            for element in rung.elements:
                if isinstance(element, Coil) and element.coil_type == CoilType.NORMAL:
                    addr = element.address.upper()
                    if addr not in coil_addresses:
                        coil_addresses[addr] = []
                    coil_addresses[addr].append(rung.number)
        
        for addr, rungs in coil_addresses.items():
            if len(rungs) > 1:
                self.warnings.append(ValidationError(
                    f"线圈 '{addr}' 在多个梯级中输出: {', '.join(map(str, rungs))}",
                    severity="warning"
                ))
    
    def _validate_timer_counter_presets(self, program: LadderProgram):
        for rung in program.rungs:
            for element in rung.elements:
                if isinstance(element, Timer):
                    if element.preset_value < 0:
                        self.errors.append(ValidationError(
                            f"定时器预设值不能为负数: {element.preset_value}",
                            rung.number, element, severity="error"
                        ))
                    if element.preset_value > 32767:
                        self.warnings.append(ValidationError(
                            f"定时器预设值可能超出范围: {element.preset_value}",
                            rung.number, element, severity="warning"
                        ))
                
                elif isinstance(element, Counter):
                    if element.preset_value < 0:
                        self.errors.append(ValidationError(
                            f"计数器预设值不能为负数: {element.preset_value}",
                            rung.number, element, severity="error"
                        ))
                    if element.preset_value > 32767:
                        self.warnings.append(ValidationError(
                            f"计数器预设值可能超出范围: {element.preset_value}",
                            rung.number, element, severity="warning"
                        ))
    
    def _validate_rung_logic(self, program: LadderProgram):
        for rung in program.rungs:
            valid, errors = rung.validate()
            if not valid:
                for error in errors:
                    self.errors.append(ValidationError(error, rung.number, severity="error"))
            
            self._check_unused_inputs(rung)
    
    def _check_unused_inputs(self, rung: Rung):
        used_addresses: Set[str] = set()
        
        for element in rung.elements:
            if isinstance(element, Contact):
                used_addresses.add(element.address.upper())
        
        warnings: List[ValidationError] = []


class SyntaxChecker:
    @staticmethod
    def check_line(line: str) -> Tuple[bool, List[str]]:
        line = line.strip()
        errors = []
        
        if not line or line.startswith('//') or line.startswith('#'):
            return True, []
        
        valid_instructions = [
            'LD', 'LDI', 'AND', 'ANI', 'OR', 'ORI',
            'OUT', 'SET', 'RST', 'PLS', 'PLF',
            'TON', 'TOF', 'TONR',
            'CTU', 'CTD', 'CTUD',
            'RUNG'
        ]
        
        parts = line.split()
        if not parts:
            return True, []
        
        instruction = parts[0].upper()
        
        if instruction.startswith('RUNG'):
            return True, []
        
        valid_instruction_found = False
        for valid in valid_instructions:
            if instruction.startswith(valid):
                valid_instruction_found = True
                break
        
        if not valid_instruction_found:
            errors.append(f"未知的指令: '{parts[0]}'")
            return False, errors
        
        if instruction in ['LD', 'LDI', 'AND', 'ANI', 'OR', 'ORI', 'OUT', 'SET', 'RST']:
            if len(parts) < 2:
                errors.append(f"指令 '{instruction}' 需要一个地址参数")
                return False, errors
        
        elif instruction in ['TON', 'TOF', 'TONR', 'CTU', 'CTD', 'CTUD']:
            if len(parts) < 3:
                errors.append(f"指令 '{instruction}' 需要地址和预设值两个参数")
                return False, errors
            try:
                int(parts[2])
            except ValueError:
                errors.append(f"预设值必须是整数: '{parts[2]}'")
                return False, errors
        
        return len(errors) == 0, errors


class QuickValidator:
    @staticmethod
    def quick_validate_text(text: str) -> Tuple[bool, List[str]]:
        lines = text.strip().split('\n')
        all_errors = []
        
        for line_num, line in enumerate(lines, 1):
            valid, errors = SyntaxChecker.check_line(line)
            if not valid:
                for error in errors:
                    all_errors.append(f"行 {line_num}: {error}")
        
        return len(all_errors) == 0, all_errors
