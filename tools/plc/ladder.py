import json
from typing import Dict, List, Optional, Tuple
from .elements import (
    LadderProgram, Rung, LadderElement, Position,
    Contact, Coil, Timer, Counter,
    ContactType, CoilType, TimerType, CounterType, ElementType
)


class LadderParser:
    @staticmethod
    def parse_text(text: str) -> Tuple[LadderProgram, List[str]]:
        program = LadderProgram()
        errors = []
        lines = text.strip().split('\n')
        current_rung = None
        rung_number = 0
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//') or line.startswith('#'):
                continue
            
            if line.startswith('RUNG'):
                if current_rung is not None:
                    program.add_rung(current_rung)
                
                rung_number += 1
                current_rung = Rung(number=rung_number)
                parts = line.split(maxsplit=1)
                if len(parts) > 1:
                    current_rung.comment = parts[1]
            elif current_rung is not None:
                element = LadderParser._parse_element(line, current_rung.number)
                if element:
                    current_rung.add_element(element)
                else:
                    errors.append(f"梯级 {rung_number}: 无法解析元素 '{line}'")
        
        if current_rung is not None:
            program.add_rung(current_rung)
        
        return program, errors
    
    @staticmethod
    def _parse_element(line: str, rung_num: int) -> Optional[LadderElement]:
        line = line.strip()
        pos = Position(row=rung_num, column=0)
        
        if line.startswith('LD') or line.startswith('LDI'):
            parts = line.split()
            if len(parts) >= 2:
                contact_type = ContactType.NORMALLY_CLOSED if line.startswith('LDI') else ContactType.NORMALLY_OPEN
                return Contact(address=parts[1], position=pos, contact_type=contact_type)
        
        elif line.startswith('AND') or line.startswith('ANI'):
            parts = line.split()
            if len(parts) >= 2:
                contact_type = ContactType.NORMALLY_CLOSED if line.startswith('ANI') else ContactType.NORMALLY_OPEN
                return Contact(address=parts[1], position=pos, contact_type=contact_type)
        
        elif line.startswith('OUT'):
            parts = line.split()
            if len(parts) >= 2:
                return Coil(address=parts[1], position=pos)
        
        elif line.startswith('SET'):
            parts = line.split()
            if len(parts) >= 2:
                return Coil(address=parts[1], position=pos, coil_type=CoilType.SET)
        
        elif line.startswith('RST'):
            parts = line.split()
            if len(parts) >= 2:
                return Coil(address=parts[1], position=pos, coil_type=CoilType.RESET)
        
        elif line.startswith('TON') or line.startswith('TOF') or line.startswith('TONR'):
            parts = line.split()
            if len(parts) >= 3:
                timer_type = TimerType(parts[0])
                try:
                    preset = int(parts[2])
                    return Timer(address=parts[1], position=pos, timer_type=timer_type, preset_value=preset)
                except ValueError:
                    pass
        
        elif line.startswith('CTU') or line.startswith('CTD') or line.startswith('CTUD'):
            parts = line.split()
            if len(parts) >= 3:
                counter_type = CounterType(parts[0])
                try:
                    preset = int(parts[2])
                    return Counter(address=parts[1], position=pos, counter_type=counter_type, preset_value=preset)
                except ValueError:
                    pass
        
        return None


class LadderGenerator:
    @staticmethod
    def generate_text(program: LadderProgram) -> str:
        lines = []
        lines.append(f"// {program.name}")
        lines.append("// 自动生成的三菱梯形图程序")
        lines.append("")
        
        for rung in program.rungs:
            lines.append(f"RUNG {rung.number} {rung.comment}".strip())
            for element in rung.elements:
                lines.append(LadderGenerator._element_to_text(element))
            lines.append("")
        
        return '\n'.join(lines)
    
    @staticmethod
    def _element_to_text(element: LadderElement) -> str:
        if isinstance(element, Contact):
            prefix = 'LDI' if element.contact_type == ContactType.NORMALLY_CLOSED else 'LD'
            return f"{prefix} {element.address}"
        
        elif isinstance(element, Coil):
            if element.coil_type == CoilType.SET:
                return f"SET {element.address}"
            elif element.coil_type == CoilType.RESET:
                return f"RST {element.address}"
            else:
                return f"OUT {element.address}"
        
        elif isinstance(element, Timer):
            return f"{element.timer_type.value} {element.address} {element.preset_value}"
        
        elif isinstance(element, Counter):
            return f"{element.counter_type.value} {element.address} {element.preset_value}"
        
        return str(element)
    
    @staticmethod
    def generate_svg(program: LadderProgram) -> str:
        svg_parts = []
        svg_width = 1000
        svg_height = max(300, len(program.rungs) * 120 + 100)
        
        svg_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
        svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}">')
        svg_parts.append('<rect width="100%" height="100%" fill="#f5f5f5"/>')
        
        left_bus_x = 60
        right_bus_x = svg_width - 60
        y_start = 60
        rung_height = 110
        
        for rung_idx, rung in enumerate(program.rungs):
            y = y_start + rung_idx * rung_height
            
            svg_parts.append(f'<rect x="40" y="{y - 15}" width="{svg_width - 80}" height="95" fill="white" stroke="#ddd" stroke-width="1"/>')
            svg_parts.append(f'<rect x="45" y="{y - 10}" width="50" height="20" fill="#e8e8e8" stroke="#ccc" stroke-width="1"/>')
            svg_parts.append(f'<text x="70" y="{y + 4}" font-family="MS Gothic, Arial" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">{rung.number}</text>')
            if rung.comment:
                svg_parts.append(f'<text x="110" y="{y + 4}" font-family="MS Gothic, Arial" font-size="11" fill="#666">{rung.comment}</text>')
            
            svg_parts.append(f'<line x1="{left_bus_x}" y1="{y - 20}" x2="{left_bus_x}" y2="{y + 65}" stroke="#000" stroke-width="4"/>')
            svg_parts.append(f'<line x1="{right_bus_x}" y1="{y - 20}" x2="{right_bus_x}" y2="{y + 65}" stroke="#000" stroke-width="4"/>')
            
            x = left_bus_x + 25
            y_center = y + 25
            
            for element_idx, element in enumerate(rung.elements):
                if isinstance(element, Contact):
                    svg_parts.append(LadderGenerator._contact_to_svg(element, x, y_center))
                    x += 80
                elif isinstance(element, Coil):
                    svg_parts.append(LadderGenerator._coil_to_svg(element, x, y_center))
                    x += 80
                elif isinstance(element, Timer):
                    svg_parts.append(LadderGenerator._timer_to_svg(element, x, y_center))
                    x += 100
                elif isinstance(element, Counter):
                    svg_parts.append(LadderGenerator._counter_to_svg(element, x, y_center))
                    x += 100
            
            if x < right_bus_x - 30:
                last_x = x - 80
                if rung.elements:
                    last_elem = rung.elements[-1]
                    if isinstance(last_elem, Coil):
                        last_x = x - 80 + 45
                    elif isinstance(last_elem, (Timer, Counter)):
                        last_x = x - 100 + 85
                    else:
                        last_x = x - 80 + 55
                svg_parts.append(f'<line x1="{last_x}" y1="{y_center}" x2="{right_bus_x}" y2="{y_center}" stroke="#000" stroke-width="2"/>')
        
        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)
    
    @staticmethod
    def _contact_to_svg(contact: Contact, x: int, y: int) -> str:
        parts = []
        parts.append(f'<line x1="{x}" y1="{y}" x2="{x + 18}" y2="{y}" stroke="#000" stroke-width="2"/>')
        parts.append(f'<line x1="{x + 18}" y1="{y - 15}" x2="{x + 18}" y2="{y + 15}" stroke="#000" stroke-width="2.5"/>')
        parts.append(f'<line x1="{x + 42}" y1="{y - 15}" x2="{x + 42}" y2="{y + 15}" stroke="#000" stroke-width="2.5"/>')
        parts.append(f'<line x1="{x + 42}" y1="{y}" x2="{x + 62}" y2="{y}" stroke="#000" stroke-width="2"/>')
        
        if contact.contact_type == ContactType.NORMALLY_CLOSED:
            parts.append(f'<line x1="{x + 22}" y1="{y - 22}" x2="{x + 38}" y2="{y + 3}" stroke="#000" stroke-width="2"/>')
        
        parts.append(f'<text x="{x + 30}" y="{y + 40}" font-family="MS Gothic, Arial" font-size="12" text-anchor="middle" font-weight="bold">{contact.address}</text>')
        return '\n'.join(parts)
    
    @staticmethod
    def _coil_to_svg(coil: Coil, x: int, y: int) -> str:
        parts = []
        parts.append(f'<line x1="{x}" y1="{y}" x2="{x + 12}" y2="{y}" stroke="#000" stroke-width="2"/>')
        parts.append(f'<circle cx="{x + 32}" cy="{y}" r="18" fill="white" stroke="#000" stroke-width="2.5"/>')
        parts.append(f'<line x1="{x + 52}" y1="{y}" x2="{x + 62}" y2="{y}" stroke="#000" stroke-width="2"/>')
        
        if coil.coil_type == CoilType.SET:
            parts.append(f'<text x="{x + 32}" y="{y + 5}" font-family="MS Gothic, Arial" font-size="14" text-anchor="middle" font-weight="bold">S</text>')
        elif coil.coil_type == CoilType.RESET:
            parts.append(f'<text x="{x + 32}" y="{y + 5}" font-family="MS Gothic, Arial" font-size="14" text-anchor="middle" font-weight="bold">R</text>')
        elif coil.coil_type == CoilType.PULSE:
            parts.append(f'<text x="{x + 32}" y="{y + 5}" font-family="MS Gothic, Arial" font-size="14" text-anchor="middle" font-weight="bold">P</text>')
        
        parts.append(f'<text x="{x + 32}" y="{y + 48}" font-family="MS Gothic, Arial" font-size="12" text-anchor="middle" font-weight="bold">{coil.address}</text>')
        return '\n'.join(parts)
    
    @staticmethod
    def _timer_to_svg(timer: Timer, x: int, y: int) -> str:
        parts = []
        parts.append(f'<line x1="{x}" y1="{y}" x2="{x + 12}" y2="{y}" stroke="#000" stroke-width="2"/>')
        parts.append(f'<rect x="{x + 12}" y="{y - 28}" width="75" height="56" fill="#d4e8f7" stroke="#000" stroke-width="2" rx="2"/>')
        parts.append(f'<line x1="{x + 12}" y1="{y - 8}" x2="{x + 87}" y2="{y - 8}" stroke="#000" stroke-width="1.5"/>')
        parts.append(f'<text x="{x + 49}" y="{y - 13}" font-family="MS Gothic, Arial" font-size="11" text-anchor="middle" font-weight="bold">{timer.timer_type.value}</text>')
        parts.append(f'<text x="{x + 49}" y="{y + 12}" font-family="MS Gothic, Arial" font-size="11" text-anchor="middle">{timer.address}</text>')
        parts.append(f'<text x="{x + 49}" y="{y + 28}" font-family="MS Gothic, Arial" font-size="11" text-anchor="middle">K{timer.preset_value}</text>')
        parts.append(f'<line x1="{x + 87}" y1="{y}" x2="{x + 97}" y2="{y}" stroke="#000" stroke-width="2"/>')
        return '\n'.join(parts)
    
    @staticmethod
    def _counter_to_svg(counter: Counter, x: int, y: int) -> str:
        parts = []
        parts.append(f'<line x1="{x}" y1="{y}" x2="{x + 12}" y2="{y}" stroke="#000" stroke-width="2"/>')
        parts.append(f'<rect x="{x + 12}" y="{y - 28}" width="75" height="56" fill="#f7e8d4" stroke="#000" stroke-width="2" rx="2"/>')
        parts.append(f'<line x1="{x + 12}" y1="{y - 8}" x2="{x + 87}" y2="{y - 8}" stroke="#000" stroke-width="1.5"/>')
        parts.append(f'<text x="{x + 49}" y="{y - 13}" font-family="MS Gothic, Arial" font-size="11" text-anchor="middle" font-weight="bold">{counter.counter_type.value}</text>')
        parts.append(f'<text x="{x + 49}" y="{y + 12}" font-family="MS Gothic, Arial" font-size="11" text-anchor="middle">{counter.address}</text>')
        parts.append(f'<text x="{x + 49}" y="{y + 28}" font-family="MS Gothic, Arial" font-size="11" text-anchor="middle">K{counter.preset_value}</text>')
        parts.append(f'<line x1="{x + 87}" y1="{y}" x2="{x + 97}" y2="{y}" stroke="#000" stroke-width="2"/>')
        return '\n'.join(parts)


class LadderSerializer:
    @staticmethod
    def to_dict(program: LadderProgram) -> Dict:
        data = {
            'name': program.name,
            'rungs': []
        }
        
        for rung in program.rungs:
            rung_data = {
                'number': rung.number,
                'comment': rung.comment,
                'elements': []
            }
            
            for element in rung.elements:
                elem_data = {
                    'type': element.element_type.value,
                    'address': element.address,
                    'position': {'row': element.position.row, 'column': element.position.column}
                }
                
                if isinstance(element, Contact):
                    elem_data['contact_type'] = element.contact_type.value
                elif isinstance(element, Coil):
                    elem_data['coil_type'] = element.coil_type.value
                elif isinstance(element, Timer):
                    elem_data['timer_type'] = element.timer_type.value
                    elem_data['preset_value'] = element.preset_value
                elif isinstance(element, Counter):
                    elem_data['counter_type'] = element.counter_type.value
                    elem_data['preset_value'] = element.preset_value
                
                rung_data['elements'].append(elem_data)
            
            data['rungs'].append(rung_data)
        
        return data
    
    @staticmethod
    def from_dict(data: Dict) -> LadderProgram:
        program = LadderProgram(name=data.get('name', 'Unnamed'))
        
        for rung_data in data.get('rungs', []):
            rung = Rung(
                number=rung_data['number'],
                comment=rung_data.get('comment', '')
            )
            
            for elem_data in rung_data.get('elements', []):
                pos = Position(
                    row=elem_data['position']['row'],
                    column=elem_data['position']['column']
                )
                
                elem_type = ElementType(elem_data['type'])
                
                if elem_type == ElementType.CONTACT:
                    element = Contact(
                        address=elem_data['address'],
                        position=pos,
                        contact_type=ContactType(elem_data['contact_type'])
                    )
                elif elem_type == ElementType.COIL:
                    element = Coil(
                        address=elem_data['address'],
                        position=pos,
                        coil_type=CoilType(elem_data['coil_type'])
                    )
                elif elem_type == ElementType.TIMER:
                    element = Timer(
                        address=elem_data['address'],
                        position=pos,
                        timer_type=TimerType(elem_data['timer_type']),
                        preset_value=elem_data['preset_value']
                    )
                elif elem_type == ElementType.COUNTER:
                    element = Counter(
                        address=elem_data['address'],
                        position=pos,
                        counter_type=CounterType(elem_data['counter_type']),
                        preset_value=elem_data['preset_value']
                    )
                else:
                    continue
                
                rung.add_element(element)
            
            program.add_rung(rung)
        
        return program
    
    @staticmethod
    def to_json(program: LadderProgram) -> str:
        return json.dumps(LadderSerializer.to_dict(program), ensure_ascii=False, indent=2)
    
    @staticmethod
    def from_json(json_str: str) -> LadderProgram:
        data = json.loads(json_str)
        return LadderSerializer.from_dict(data)
