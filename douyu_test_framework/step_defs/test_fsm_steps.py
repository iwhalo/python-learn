"""状态机管理功能的步骤定义"""
from pytest_bdd import scenarios, given, when, then, parsers
from douyu_test_framework.core.fsm import FSM, PageState

# 从特性文件加载场景
scenarios('../features/fsm_states.feature')


@given('the FSM is initialized')
def fsm_initialized(fsm):
    """FSM已在conftest中初始化"""
    assert fsm is not None
    return fsm


@given(parsers.parse('I am in {state_name} state'))
def set_fsm_state(fsm, state_name):
    """设置FSM到特定状态"""
    state = PageState[state_name]
    
    # 如果还没在目标状态，直接设置
    # 这是用于测试设置目的
    if fsm.current_state != state:
        fsm.current_state = state
        # 如需要更新历史
        if state not in fsm.history:
            fsm.history.append(state)
    
    return fsm


@when(parsers.parse('I transition to {state_name} state'))
def transition_to_state(fsm, state_name):
    """转换到特定状态"""
    # 将状态名映射到动作
    action_map = {
        'HOME': 'navigate_home',
        'SEARCH_RESULTS': 'search',
        'LIVE_ROOM': 'enter_live_room',
        'CATEGORY': 'select_category',
    }
    
    target_state = PageState[state_name]
    action = action_map.get(state_name, 'navigate_home')
    
    try:
        fsm.transition(action)
    except ValueError as e:
        # 存储异常以便后续断言
        fsm.last_error = str(e)


@when(parsers.parse('I transition back to {state_name} state'))
def transition_back(fsm, state_name):
    """返回到某个状态"""
    fsm.transition('go_home')


@when(parsers.parse('I attempt an invalid transition to {state_name} state'))
def attempt_invalid_transition(fsm, state_name):
    """尝试无效转换"""
    try:
        # 尝试一个应该失败的转换
        fsm.transition('click_login')
        fsm.transition_failed = False
    except ValueError:
        fsm.transition_failed = True


@then(parsers.parse('the current state should be {state_name}'))
def verify_current_state(fsm, state_name):
    """验证当前状态"""
    expected_state = PageState[state_name]
    assert fsm.current_state == expected_state, \
        f"Expected {expected_state.value}, got {fsm.current_state.value}"


@then(parsers.parse('the state history should include "{states}"'))
def verify_state_history(fsm, states):
    """验证状态历史"""
    expected_states = [s.strip() for s in states.split(',')]
    history_names = [s.value for s in fsm.history]
    
    for expected in expected_states:
        assert expected.lower() in history_names, \
            f"State {expected} not found in history {history_names}"


@then(parsers.parse('the previous state should be {state_name}'))
def verify_previous_state(fsm, state_name):
    """验证前一个状态"""
    expected_state = PageState[state_name]
    if len(fsm.history) >= 2:
        previous_state = fsm.history[-2]
        assert previous_state == expected_state, \
            f"Expected previous state {expected_state.value}, got {previous_state.value}"


@then('the transition should fail')
def verify_transition_failed(fsm):
    """验证转换失败"""
    assert hasattr(fsm, 'transition_failed') and fsm.transition_failed, \
        "Transition should have failed"


@then(parsers.parse('the current state should remain {state_name}'))
def verify_state_unchanged(fsm, state_name):
    """验证状态保持不变"""
    expected_state = PageState[state_name]
    assert fsm.current_state == expected_state, \
        f"State should remain {expected_state.value}, got {fsm.current_state.value}"
