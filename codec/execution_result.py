from enum import Enum


class ExecutionResult(Enum):
    EXECUTION_RESULT_SUCCESS = 'SUCCESS'
    EXECUTION_RESULT_ERROR_SMART_CONTRACT = 'ERROR_SMART_CONTRACT'
    EXECUTION_RESULT_ERROR_INPUT = 'ERROR_INPUT'
    EXECUTION_RESULT_ERROR_UNEXPECTED = 'ERROR_UNEXPECTED'
    EXECUTION_RESULT_STATE_WRITE_IN_A_CALL = 'STATE_WRITE_IN_A_CALL'


def execution_result_decode(execution_result: int) -> ExecutionResult:
    if execution_result == 0:
        raise ValueError('reserved ExecutionResult received')
    elif execution_result == 1:
        return ExecutionResult.EXECUTION_RESULT_SUCCESS
    elif execution_result == 2:
        return ExecutionResult.EXECUTION_RESULT_ERROR_SMART_CONTRACT
    elif execution_result == 3:
        return ExecutionResult.EXECUTION_RESULT_ERROR_INPUT
    elif execution_result == 4:
        return ExecutionResult.EXECUTION_RESULT_ERROR_UNEXPECTED
    elif execution_result == 5:
        return ExecutionResult.EXECUTION_RESULT_STATE_WRITE_IN_A_CALL
    else:
        raise ValueError(f'unsupported ExecutionResult received: {execution_result}')
