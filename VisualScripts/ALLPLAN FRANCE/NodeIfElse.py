""" Script for NodeIfElse
"""
from __future__ import annotations

from typing import Any

from NodeUtil.NodeBase     import NodeBase
from NodeUtil.NodeInitData import NodeInitData


NodeBase.trace_node_name('NodeIfElse')


def create_node(init_data: NodeInitData) -> NodeIfElse:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of NodeIfElse
    """

    return NodeIfElse(init_data)


class NodeIfElse(NodeBase):
    """ Definition of class NodeIfElse
    """

    def _create_output(self) -> None:
        """ If/Else statement
        """
        self._set_init_node_output(self.build_ele.Result)

        test = self.build_ele.Condition.value
        on_true = self.build_ele.OnTrue.value
        on_false = self.build_ele.OnFalse.value

        if isinstance(test, int) and test not in (0, 1):
            self.error = "Condition must a boolean or 0 / 1 integer"
            return

        self.build_ele.Result.value = self.process_condition(test, on_true, on_false)


    def process_condition(self,
                          test:     Any,
                          on_true:  Any,
                          on_false: Any) -> Any | list:
        """ Processing if else condition

        Args:
            test:     condition
            on_true:  result if condition is true
            on_false: result if condition is false

        Returns:
            result of condition
        """
        # Test as a list
        if isinstance(test, list):
            # OnTrue
            if on_true is None or (isinstance(on_true, list) and len(on_true) == 0):
                on_true = [None]
            elif not isinstance(on_true, list):
                on_true = [on_true]
            # OnFalse
            if on_false is None or (isinstance(on_false, list) and len(on_false) == 0):
                on_false = [None]
            elif not isinstance(on_false, list):
                on_false = [on_false]

            test_length = len(test)
            on_true_length = len(on_true)
            on_false_length = len(on_false)
            max_length = max(test_length, on_true_length, on_false_length)

            if test_length < max_length:
                test += [test[-1]] * (max_length - test_length)
            if on_true_length < max_length:
                on_true += [on_true[-1]] * (max_length - on_true_length)
            if on_false_length < max_length:
                on_false += [on_false[-1]] * (max_length - on_false_length)

            result = []
            for i in range(max_length):
                result.append(on_true[i] if bool(test[i]) else on_false[i])

            if max_length == 1:
                return result[0]

            return result

        # Test as a single value
        return on_true if bool(test) else on_false
