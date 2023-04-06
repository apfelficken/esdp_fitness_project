from aiogram.dispatcher.filters.state import StatesGroup, State


class StartTrainingState(StatesGroup):
    group = State()
    link = State()
    send_invite = State()
