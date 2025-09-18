"""用于管理页面状态的有限状态机"""
from enum import Enum
from typing import Dict, Set, Callable, Optional
from playwright.sync_api import Page


class PageState(Enum):
    """斗鱼网站的页面状态"""
    INITIAL = "initial"  # 初始状态
    HOME = "home"  # 首页
    CATEGORY = "category"  # 分类页
    LIVE_ROOM = "live_room"  # 直播间
    SEARCH_RESULTS = "search_results"  # 搜索结果页
    LOGIN = "login"  # 登录页
    ERROR = "error"  # 错误状态


class StateTransition:
    """表示状态转换"""
    def __init__(self, from_state: PageState, to_state: PageState, 
                 action: str, condition: Optional[Callable] = None):
        self.from_state = from_state
        self.to_state = to_state
        self.action = action
        self.condition = condition


class FSM:
    """用于管理页面导航和状态的有限状态机"""
    
    def __init__(self, page: Page, initial_state: PageState = PageState.INITIAL):
        self.page = page
        self.current_state = initial_state
        self.transitions: Dict[str, StateTransition] = {}
        self.state_validators: Dict[PageState, Callable] = {}
        self.history = [initial_state]
        self._setup_transitions()
        
    def _setup_transitions(self):
        """设置有效的状态转换"""
        # 定义所有有效的状态转换
        transitions = [
            StateTransition(PageState.INITIAL, PageState.HOME, "navigate_home"),
            StateTransition(PageState.HOME, PageState.CATEGORY, "select_category"),
            StateTransition(PageState.HOME, PageState.SEARCH_RESULTS, "search"),
            StateTransition(PageState.HOME, PageState.LOGIN, "click_login"),
            StateTransition(PageState.HOME, PageState.LIVE_ROOM, "enter_live_room"),
            StateTransition(PageState.CATEGORY, PageState.LIVE_ROOM, "select_live_room"),
            StateTransition(PageState.CATEGORY, PageState.HOME, "go_home"),
            StateTransition(PageState.SEARCH_RESULTS, PageState.LIVE_ROOM, "select_search_result"),
            StateTransition(PageState.SEARCH_RESULTS, PageState.HOME, "go_home"),
            StateTransition(PageState.LIVE_ROOM, PageState.HOME, "go_home"),
            StateTransition(PageState.LOGIN, PageState.HOME, "successful_login"),
            # 错误状态可以从任何状态转换而来
            StateTransition(PageState.HOME, PageState.ERROR, "error_occurred"),
            StateTransition(PageState.CATEGORY, PageState.ERROR, "error_occurred"),
            StateTransition(PageState.LIVE_ROOM, PageState.ERROR, "error_occurred"),
        ]
        
        for transition in transitions:
            key = f"{transition.from_state.value}_{transition.action}"
            self.transitions[key] = transition
    
    def register_validator(self, state: PageState, validator: Callable[[Page], bool]):
        """为特定状态注册验证函数"""
        self.state_validators[state] = validator
    
    def validate_current_state(self) -> bool:
        """验证当前页面是否匹配当前状态"""
        if self.current_state in self.state_validators:
            validator = self.state_validators[self.current_state]
            return validator(self.page)
        return True
    
    def transition(self, action: str) -> bool:
        """尝试转换到新状态"""
        key = f"{self.current_state.value}_{action}"
        
        if key not in self.transitions:
            raise ValueError(
                f"Invalid transition: {action} from state {self.current_state.value}"
            )
        
        transition = self.transitions[key]
        
        # 检查条件（如果存在）
        if transition.condition and not transition.condition():
            return False
        
        # 执行状态转换
        old_state = self.current_state
        self.current_state = transition.to_state
        self.history.append(self.current_state)
        
        print(f"FSM: Transitioned from {old_state.value} to {self.current_state.value} via '{action}'")
        return True
    
    def can_transition(self, action: str) -> bool:
        """检查从当前状态的转换是否有效"""
        key = f"{self.current_state.value}_{action}"
        return key in self.transitions
    
    def get_current_state(self) -> PageState:
        """获取当前状态"""
        return self.current_state
    
    def get_history(self) -> list:
        """获取状态历史"""
        return self.history.copy()
    
    def reset(self):
        """重置FSM到初始状态"""
        self.current_state = PageState.INITIAL
        self.history = [PageState.INITIAL]
