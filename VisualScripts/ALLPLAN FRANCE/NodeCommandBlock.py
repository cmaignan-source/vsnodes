""" Script for NodeCommandBlock
"""

import re
import ast
import math
import random
import operator

from typing import Any

from NodeUtil import NodeBase, NodeFunctionUtil


NodeBase.trace_node_name('NodeCommandBlock')

#
# Authorized operators
#

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
    }

MATH_FUNCS = {
    "abs": math.fabs,
    "sqrt": math.sqrt,
    "pow": math.pow,

    "rad": math.radians,   # degrees -> radians
    "deg": math.degrees,   # radians -> degrees

    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,

    "log": math.log,       # log(x) = ln(x)
    "log10": math.log10,   # log base 10
    "exp": math.exp,       # e**x
    }

MATH_CONSTS = {
    "pi": math.pi
    }


def create_node(init_data):
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        created node
    """
    return NodeCommandBlock(init_data)


class NodeCommandBlock(NodeBase):
    """ Definition of class NodeCommandBlock
    """

    def _create_output(self) -> None:
        """ Execute instructions
        """
        # Init outputs
        self._set_init_node_output(self.build_ele.AsInteger)
        self._set_init_node_output(self.build_ele.AsDouble)
        self._set_init_node_output(self.build_ele.AsString)
        self._set_init_node_output(self.build_ele.AsList)

        self.build_ele.AsInteger.value = None
        self.build_ele.AsDouble.value = None
        self.build_ele.AsString.value = None
        self.build_ele.AsList.value = None

        if not self.build_ele.Command.value:
            self.error = "No instruction to execute"
            return

        text = self.build_ele.Command.value.strip()

        # Set of authorized names (functions and constants)
        allowed_names = set(MATH_FUNCS.keys()) | set(MATH_CONSTS.keys())

        # Regex pattern to detect a complete word from these names (pi, sqrt, ...)
        allowed_pattern = fr"\b({'|'.join(re.escape(name) for name in allowed_names)})\b"

        # Generate sequence
        if ".." in text:
            self.build_ele.AsList.value = self.create_sequence_from_text(text)

        # Create list
        elif "|" in text:
            items = text.split("|")
            seq = self.normalize_list_type(items)
            self.build_ele.AsList.value = seq

        # Random integers
        elif text.lower().startswith("rand(") and text.endswith(")"):
            try:
                args = [a.strip() for a in text[5:-1].split(",")]
                if len(args) != 3:
                    raise ValueError("rand(min,max,count)")
                min_val = int(args[0])
                max_val = int(args[1])
                count = int(args[2])
                if count > (max_val - min_val + 1):
                    raise ValueError("Count too large for unique integers in range")
                seq = sorted(random.sample(range(min_val, max_val + 1), count))
                self.build_ele.AsList.value = seq
            except Exception as e:
                self.build_ele.AsString.value = f"Random error: {e}"

        # Random floats
        elif text.lower().startswith("randf(") and text.endswith(")"):
            try:
                args = [a.strip() for a in text[6:-1].split(",")]
                if len(args) not in (3, 4):
                    raise ValueError("randf(min,max,count[,precision])")
                min_val = float(args[0])
                max_val = float(args[1])
                count = int(args[2])
                precision = int(args[3]) if len(args) == 4 else 3
                # Avoid infinite loop if request is impossible
                max_unique_values = int((max_val - min_val) * (10 ** precision)) + 1
                if count > max_unique_values:
                    raise ValueError(
                        f"Unable to generate {count} unique values "
                        f"with precision {precision} over the range {min_val}-{max_val}"
                    )
                seen = set()
                while len(seen) < count:
                    seen.add(round(random.uniform(min_val, max_val), precision))
                seq = sorted(seen)
                self.build_ele.AsList.value = seq
            except Exception as e:
                self.build_ele.AsString.value = f"Random error: {e}"

        # Simple arithmetic expression
        elif re.fullmatch(r"[0-9a-zA-Z\.\s\+\-\*/%\(\),]+", text):
            has_math_name = re.search(allowed_pattern, text)
            has_digit = re.search(r"\d", text)
            has_operator = re.search(r"[+\-*/%]", text)

            if has_math_name or (has_digit and has_operator):
                try:
                    result = self.calculate_expr(text)
                    if isinstance(result, (int, float)):
                        self.fill_numeric_output(result)
                    else:
                        self.build_ele.AsString.value = str(result)
                        self.build_ele.AsList.value = [result]
                except Exception as e:
                    self.build_ele.AsString.value = f"Calcul error: {e}"

            else:
                try:
                    val = float(text)
                    self.fill_numeric_output(val)
                except ValueError:
                    self.build_ele.AsString.value = text
                    self.build_ele.AsList.value = [text]

        # Text
        else:
            self.build_ele.AsString.value = text
            self.build_ele.AsList.value = [text]


    def normalize_list_type(self,
                            seq: str) -> list[int] | list[float] | str:
        """ Converts a list of strings into a homogeneous list (int, float, str)

        Args:
            seq: user input

        Returns:
            homogeneous list
        """
        # Clean spaces
        seq = [str(item).strip() for item in seq]

        # Integer
        try:
            return sorted([int(v) for v in seq])
        except ValueError:
            pass

        # Float
        try:
            return sorted([float(v) for v in seq])
        except ValueError:
            pass

        # String (default)
        return seq


    def fill_numeric_output(self,
                            val: str) -> None:
        """ Fill AsInteger / AsDouble / AsList depending on the numeric type

        Args:
            val: user input
        """
        if isinstance(val, int) or (isinstance(val, float) and val.is_integer()):
            self.build_ele.AsInteger.value = int(val)
            self.build_ele.AsDouble.value = float(val)
            self.build_ele.AsList.value = [int(val)]
        else:
            self.build_ele.AsDouble.value = float(val)
            self.build_ele.AsList.value = [float(val)]


    def calculate_expr(self, expr: str):
        """ Safely evaluates an arithmetic expression.

        Args:
            expr: string input
        """
        def eval_expr(node):
            if isinstance(node, ast.Expression):
                return eval_expr(node.body)

            # Numerical constants (integer / float)
            elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value

            # Binary operations
            elif isinstance(node, ast.BinOp):
                op_type = type(node.op)
                if op_type in OPS:
                    return OPS[op_type](eval_expr(node.left), eval_expr(node.right))
                raise ValueError(f"Operator {op_type} not allowed")

            # Unary operations (+x / -x)
            elif isinstance(node, ast.UnaryOp):
                op_type = type(node.op)
                if op_type in OPS:
                    return OPS[op_type](eval_expr(node.operand))
                raise ValueError(f"Unary operator {op_type} not allowed")

            # Mathematical operations : sqrt(x), pow(x, y), sin(x), cos(x), tan(x)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    fname = node.func.id
                    if fname in MATH_FUNCS:
                        args = [eval_expr(arg) for arg in node.args]
                        return MATH_FUNCS[fname](*args)
                raise ValueError("Function not allowed")

            # Mathematical constants : pi
            elif isinstance(node, ast.Name):
                if node.id in MATH_CONSTS:
                    return MATH_CONSTS[node.id]
                raise ValueError("Unknown constant")

            else:
                raise ValueError(f"Expression not allowed: {type(node)}")

        # Parse the expression and start the evaluation
        try:
            tree = ast.parse(expr, mode='eval')
        except SyntaxError as e:
            raise ValueError(f"Syntax error: {e}") from e

        return eval_expr(tree.body)


    def is_number(self, value: Any) -> bool:
        """ Check if value is a number

        Args:
            value: user input

        Returns:
         True / False
        """
        try:
            float(value)
            return True
        except Exception:
            return False


    def is_alpha(self, value: Any) -> bool:
        """ Check if value is a string

        Args:
            value: user input

        Returns:
         True / False
        """
        return bool(re.fullmatch(r"[A-Za-z]+", value))


    def clean_string(self, value: str) -> str:
        """ Remove spaces and quotes

        Args:
            value: user string input

        Returns:
            cleaned text
        """
        s = value.strip()
        while s.startswith('"') or s.startswith("'"):
            s = s[1:]
        while s.endswith('"') or s.endswith("'"):
            s = s[:-1]
        return s.strip()


    def alpha_to_num(self, s: str) -> int:
        """ Letter to number

        Args:
            s: string input

        Returns:
            number
        """
        s = s.upper()
        num = 0
        for c in s:
            num = num * 26 + (ord(c) - ord('A') + 1)
        return num - 1


    def num_to_alpha(self, n: int) -> str:
        """ Number to letter

        Args:
            n: number input

        Returns:
            letter
        """
        s = ""
        n += 1
        while n > 0:
            n, r = divmod(n - 1, 26)
            s = chr(r + ord('A')) + s
        return s


    def sequence_step(self,
                      start: str,
                      end: str,
                      step: int = 1,
                      is_alpha: bool = False) -> list:
        """ Generate sequences:
        - start..end
        - start..end..step

        Args:
            start: first element of the sequence
            end: last element of the sequence
            step: step between elements
            is_alpha: check if sequence of letters or numbers

        Returns:
            sequence as list
        """
        if step == 0:
            raise ValueError("Step cannot be zero")

        direction = 1 if start < end else -1
        step = abs(step) * direction

        if is_alpha:
            limit = end + direction
            return [self.num_to_alpha(n) for n in range(int(start), int(limit), int(step))]

        seq = []
        epsilon = 1e-9
        current = start
        while (direction == 1 and current <= end + epsilon) or \
            (direction == -1 and current >= end - epsilon):
            seq.append(int(current) if isinstance(current, float) and current.is_integer() else current)
            current += step
        return seq


    def sequence_with_count(self,
                            start: str,
                            end: str,
                            count: int,
                            is_alpha: bool = False) -> list:
        """ Generate sequences:
        - start..end..@count
        - start..@count..end

        Args:
            start: first element of the sequence
            end: last element of the sequence
            count: how many elements in the sequence
            is_alpha: check if sequence of letters or numbers

        Returns:
            sequence as list
        """
        if count == 1:
            return [self.num_to_alpha(start)] if is_alpha else [int(start) if start.is_integer() else start]

        step = (end - start) / (count - 1) if count > 1 else 0

        if is_alpha:
            return [self.num_to_alpha(round(start + i * step)) for i in range(count)]

        seq_nums = [start + i * step for i in range(count)]
        return [int(x) if x.is_integer() else x for x in seq_nums]


    def create_sequence_from_text(self, text: str) -> list:
        """ Function to create sequence following:
        - start..end (step = 1)
        - start..end..step
        - start..end..@count
        - start..@count..end

        Args:
            text: string

        Returns:
            list of sequence
        """
        result = []

        try:
            parts = text.split("..")
            if len(parts) not in (2, 3):
                raise ValueError("Syntax error: must contain 2 or 3 parts separated by '..'")

            # Clean strings
            parts_clean = list(map(self.clean_string, parts))

            # Case 1 => 2 elements (step = 1)
            if len(parts_clean) == 2:
                start_str, end_str = parts_clean
                if '@' in start_str or '@' in end_str:
                    raise ValueError("Syntax error: '@' forbidden in start or end")
                # Sequence of letters
                if self.is_alpha(start_str) and self.is_alpha(end_str):
                    return self.sequence_step(start= self.alpha_to_num(start_str),
                                              end= self.alpha_to_num(end_str),
                                              is_alpha= True
                                              )
                # Sequence of numbers
                elif self.is_number(start_str) and self.is_number(end_str):
                    return self.sequence_step(start= float(start_str),
                                              end= float(end_str),
                                              is_alpha= False
                                              )
                else:
                    raise ValueError("Syntax error: start and end must both be alphabetic or numeric")

            # Case 2 => 3 elements
            else:
                start_str, mid_str, end_str = parts_clean

                # Case 2a or 2b: with '@count'
                if mid_str.startswith("@") or end_str.startswith("@"):

                    count_str = None
                    start_token = None
                    end_token = None

                    # Case 2a: start..@count..end
                    if mid_str.startswith("@"):
                        count_str = mid_str[1:]
                        start_token = start_str
                        end_token = end_str

                    # Case 2b: start..end..@count
                    elif end_str.startswith("@"):
                        count_str = end_str[1:]
                        start_token = start_str
                        end_token = mid_str

                    if count_str is None:
                        raise ValueError("Syntax error: invalid '@count' syntax in sequence definition")

                    if not count_str.isdigit():
                        raise ValueError(f"Syntax error: '{count_str}' is not a valid number")

                    count = int(count_str)
                    if count < 1:
                        raise ValueError("Syntax error: count must be at least 1")

                    # Sequence of letters
                    if self.is_alpha(start_token) and self.is_alpha(end_token):
                        start = self.alpha_to_num(start_token)
                        end = self.alpha_to_num(end_token)
                        seq = self.sequence_with_count(start, end, count, True)
                        result.extend(seq)

                    # Sequence of numbers
                    elif self.is_number(start_token) and self.is_number(end_token):
                        start = float(start_token)
                        end = float(end_token)
                        seq = self.sequence_with_count(start, end, count, False)
                        result.extend(seq)

                # Case 2c: start..end..step
                else:
                    # Sequence of letters
                    if self.is_alpha(start_str) and self.is_alpha(mid_str) and self.is_number(end_str):
                        # Sequence of letters
                        if self.is_alpha(start_str) and self.is_alpha(mid_str) and self.is_number(end_str):
                            return self.sequence_step(self.alpha_to_num(start_str),
                                                      self.alpha_to_num(mid_str),
                                                      int(end_str),
                                                      True
                                                      )

                    # Sequence of numbers
                    elif self.is_number(start_str) and self.is_number(mid_str) and self.is_number(end_str):
                        return self.sequence_step(float(start_str),
                                                  float(mid_str),
                                                  float(end_str),
                                                  False
                                                  )

                    else:
                        raise ValueError("Syntax error: start..end..step must be either all alphabetic or all numeric")

        except Exception as e:
            print(f"Erreur : {e}")
            return None

        return result
