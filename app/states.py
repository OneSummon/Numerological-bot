from aiogram.fsm.state import State, StatesGroup

class Reg(StatesGroup):
    name = State()
    phone = State()

class Enter(StatesGroup):
    num_of_destiny = State()
    num_of_personal_year = State()
    
    username_for_NoD = State()
    username_for_NoPY = State()

    count_tokens_for_NoD = State()
    count_tokens_for_NoPY = State()
    
class RefilBalance(StatesGroup):
    choice_analysis = State()
    choice_sum = State()