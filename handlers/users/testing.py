from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Command

from loader import dp

from states import Test


@dp.message_handler(Command("test"))
async def enter_test(message: types.Message):
    await message.answer("Тестирование началось")
    await message.answer("Вопрос 1. Можешь написать 'Да'")
    await Test.Q1.set()
    # await Test.first()


@dp.message_handler(state=Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer1=answer)

    # await state.update_data(
    #     {
    #         "answer1":answer
    #     }
    # )

    # async with state.proxy() as data:
    #     data["answer1"] = answer
    await message.answer("Вопрос 2. Можешь написать 'Нет'")
    await Test.Q2.set()


@dp.message_handler(state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    await message.answer("End Test")

    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = message.text

    await message.answer(f"Answers: \n"
                         f"1:{answer1}\n"
                         f"2:{answer2}")
    await state.finish()
