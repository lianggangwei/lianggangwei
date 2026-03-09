import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.plc import (
    LadderProgram, Rung, Contact, Coil, Timer, Counter, Position,
    ContactType, CoilType, TimerType, CounterType,
    LadderParser, LadderGenerator, LadderSerializer,
    LadderValidator, QuickValidator
)


def example_1_simple_program():
    print("=" * 60)
    print("示例1：创建简单的启动停止程序")
    print("=" * 60)
    
    program = LadderProgram(name="启动停止电路")
    
    rung1 = Rung(number=1, comment="启动停止自锁")
    rung1.add_element(Contact(address="X0", position=Position(row=1, column=0), contact_type=ContactType.NORMALLY_OPEN))
    rung1.add_element(Contact(address="Y0", position=Position(row=1, column=1), contact_type=ContactType.NORMALLY_OPEN))
    rung1.add_element(Contact(address="X1", position=Position(row=1, column=2), contact_type=ContactType.NORMALLY_CLOSED))
    rung1.add_element(Coil(address="Y0", position=Position(row=1, column=3)))
    program.add_rung(rung1)
    
    rung2 = Rung(number=2, comment="运行指示灯")
    rung2.add_element(Contact(address="Y0", position=Position(row=2, column=0), contact_type=ContactType.NORMALLY_OPEN))
    rung2.add_element(Coil(address="Y1", position=Position(row=2, column=1)))
    program.add_rung(rung2)
    
    text = LadderGenerator.generate_text(program)
    print("\n生成的代码:")
    print(text)
    
    validator = LadderValidator()
    valid, errors, warnings = validator.validate(program)
    
    print(f"\n校验结果: {'✅ 通过' if valid else '❌ 失败'}")
    if errors:
        print("错误:")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print("警告:")
        for w in warnings:
            print(f"  - {w}")
    
    return program


def example_2_parse_text():
    print("\n" + "=" * 60)
    print("示例2：解析文本格式的梯形图")
    print("=" * 60)
    
    ladder_text = """// 定时器示例程序
RUNG 1 启动定时器
LD X0
TON T0 100

RUNG 2 定时器输出
LD T0
OUT Y0

RUNG 3 计数器
LD X1
CTU C0 10

RUNG 4 计数器输出
LD C0
OUT Y1
"""
    
    print("\n输入代码:")
    print(ladder_text)
    
    program, parse_errors = LadderParser.parse_text(ladder_text)
    
    if parse_errors:
        print("\n解析错误:")
        for e in parse_errors:
            print(f"  - {e}")
        return None
    
    print(f"\n✅ 解析成功！共 {len(program.rungs)} 个梯级")
    
    validator = LadderValidator()
    valid, errors, warnings = validator.validate(program)
    
    print(f"\n完整校验: {'✅ 通过' if valid else '❌ 失败'}")
    if errors:
        print("错误:")
        for e in errors:
            print(f"  - {e}")
    
    return program


def example_3_quick_validation():
    print("\n" + "=" * 60)
    print("示例3：快速语法校验")
    print("=" * 60)
    
    test_cases = [
        ("LD X0", True, "正常的指令"),
        ("OUT Y10", True, "正常的输出"),
        ("TON T0 100", True, "正常的定时器"),
        ("INVALID X0", False, "无效的指令"),
        ("LD", False, "缺少参数"),
        ("TON T0 ABC", False, "预设值不是整数"),
    ]
    
    for code, should_be_valid, description in test_cases:
        valid, errors = QuickValidator.quick_validate_text(code)
        status = "✅" if valid == should_be_valid else "❌"
        print(f"{status} [{description}] '{code}'")
        if errors:
            for e in errors:
                print(f"      {e}")


def example_4_json_serialization():
    print("\n" + "=" * 60)
    print("示例4：JSON序列化和反序列化")
    print("=" * 60)
    
    program = LadderProgram(name="序列化测试")
    
    rung = Rung(number=1, comment="测试梯级")
    rung.add_element(Contact(address="X0", position=Position(row=1, column=0)))
    rung.add_element(Coil(address="Y0", position=Position(row=1, column=1)))
    program.add_rung(rung)
    
    json_str = LadderSerializer.to_json(program)
    print("\n序列化为JSON:")
    print(json_str[:200] + "..." if len(json_str) > 200 else json_str)
    
    restored = LadderSerializer.from_json(json_str)
    print(f"\n✅ 反序列化成功！程序名: {restored.name}, 梯级数: {len(restored.rungs)}")


def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "三菱梯形图工具 - 示例程序" + " " * 26 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        example_1_simple_program()
        example_2_parse_text()
        example_3_quick_validation()
        example_4_json_serialization()
        
        print("\n" + "=" * 60)
        print("🎉 所有示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
