from aiogram.dispatcher.filters.state import StatesGroup, State


class StartUserStatesGroup(StatesGroup):
    start = State()


class CreateUserProfileStatesGroup(StatesGroup):
    create_init = State()
    name = State()
    age = State()
    city = State()
    description = State()
    photo = State()
    finish = State()
    agreement = State()


class PeopleSearch(StatesGroup):
    start = State()
    search = State()
