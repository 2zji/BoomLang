import sys

class BoomLang:
    def __init__(self):
        self.data = [0] * 256  # 메모리
        self.ptr = 0            # 포인터 위치

    def toNumber(self, code: str) -> int:
        """붐/뱅 개수로 숫자 계산"""
        return code.count("붐") - code.count("뱅")

    @staticmethod
    def getType(code: str):
        """명령어 판별"""
        if code.startswith("쿵"):
            return "IF"
        if code.startswith("차"):
            return "LOOP_START"
        if code.startswith("촤"):
            return "LOOP_END"
        if "붐붐붐" in code:
            return "PTR_RIGHT"
        if "뱅뱅뱅" in code:
            return "PTR_LEFT"
        if "붐붐" in code:
            return "RESET"
        if "칰ㅋ" in code:
            return "PRINT_ASCII"
        if "칰" in code:
            return "PRINT"
        if "췍" in code:
            return "NEWLINE"
        if "비트박스" in code and "체크!" in code:
            return "END"
        return "CMD"

    def compile(self, code: str):
        lines = [line.strip() for line in code.split("\n") if line.strip()]
        index = 0
        loop_stack = {}

        # 루프 짝 찾기
        stack = []
        for i, line in enumerate(lines):
            if line.startswith("차"):
                stack.append(i)
            elif line.startswith("촤"):
                if not stack:
                    raise SyntaxError("닫히지 않은 '차' 루프가 있습니다.")
                start = stack.pop()
                loop_stack[start] = i
                loop_stack[i] = start
        if stack:
            raise SyntaxError("'차' 루프가 닫히지 않았습니다.")

        while index < len(lines):
            line = lines[index]
            cmd_type = self.getType(line)

            if cmd_type == "CMD":
                self.data[self.ptr] += self.toNumber(line)
            elif cmd_type == "RESET":
                self.data[self.ptr] = 0
            elif cmd_type == "PTR_RIGHT":
                self.ptr = (self.ptr + 1) % len(self.data)
            elif cmd_type == "PTR_LEFT":
                self.ptr = (self.ptr - 1) % len(self.data)
            elif cmd_type == "PRINT":
                print(self.data[self.ptr], end="")
            elif cmd_type == "PRINT_ASCII":
                print(chr(self.data[self.ptr]), end="")
            elif cmd_type == "NEWLINE":
                print()
            elif cmd_type == "LOOP_START":
                if self.data[self.ptr] == 0:
                    index = loop_stack[index]
            elif cmd_type == "LOOP_END":
                if self.data[self.ptr] != 0:
                    index = loop_stack[index]
            elif cmd_type == "IF":
                cond = line.replace("쿵", "").strip()
                if "~" not in cond:
                    raise SyntaxError("조건문 쿵 구문 오류 (A~B 형태 필요)")
                left, right = cond.split("~")
                if self.toNumber(left) != self.toNumber(right):
                    index += 1
            elif cmd_type == "END":
                sys.exit(0)

            index += 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python boomlang.py <파일>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    interpreter = BoomLang()
    interpreter.compile(code)
