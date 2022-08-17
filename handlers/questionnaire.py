from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from main import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db
from keyboards import client_keyboard
from dictionary import YES_SET, NO_SET, DONT_KNOW_SET, STOP_SET, CENSURE_SET
from datetime import datetime
import string
import gspread

gc = gspread.service_account(filename='movebot-359618-6eadda2de784.json')

class FSMQuestion(StatesGroup):
    client_name = State()
    client_phone = State()
    check_special = State()
    cargo = State()
    veight = State()
    kind_loading = State()
    check_pallets = State()
    pallets_count = State()
    pallets_dimensions = State()
    cargo_dimensions = State()
    add_carcas = State()
    addres_loading = State()
    addres_docs = State()
    addres_docs_extended = State()
    addres_unloading = State()
    date_loading = State()
    date_unloading = State()
    custom = State()
    custom_export = State()
    export_declaration = State()
    custom = State()
    custom_import = State()
    insurance = State()
    insurance_cost = State()
    attention = State()
    check_data_1 = State()
    check_data_2 = State()
    check_data_3 = State()


#Начало опроса. Запрашиваем имя клиента.
async def begin(message: types.Message, state: FSMContext):
    await message.answer('Здравствуйте9! Я Ваш личный помощник по организации перевозок. Для того, чтобы мы могли обработать заказ, и сделать максимально выгодное предложение, мне необходимо задать несколько вопросов. Для начала скажите пожалуйста как я могу к Вам обращаться?', reply_markup=ReplyKeyboardRemove())
    async with state.proxy() as data:
        data['db_current_datetime'] = datetime.now().strftime("%d/%m/%Y, %H:%M:%S:%f'")[:-3]
        data['db_client_name'] = '-'
        data['db_client_phone'] = '-'
        data['db_check_special'] = '-'
        data['db_cargo'] = '-'
        data['db_veight'] = '-'
        data['db_kind_loading'] = '-'
        data['db_check_pallets'] = '-'
        data['db_pallets_count'] = '-'
        data['db_pallets_dimensions'] = '-'
        data['db_cargo_dimensions'] = '-'
        data['db_add_carcas'] = '-'
        data['db_addres_loading'] = '-'
        data['db_addres_docs'] = '-'
        data['db_addres_unloading'] = '-'
        data['db_date_loading'] = '-'
        data['db_date_unloading'] = '-'
        data['db_custom'] = '-'
        data['db_custom_export'] = '-'
        data['db_export_declaration'] = '-'
        data['db_custom_import'] = '-'
        data['db_insurance_cost'] = '-'
        data['db_attention'] = '-'
    await FSMQuestion.client_name.set()

#Получаем имя клиента. Запрашиваем телефон клиента.
async def function_client_name(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 30:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.client_name.set()
        else:
            async with state.proxy() as data:
                data['db_client_name'] = message.text
            await message.answer(data['db_client_name']+', по какому номеру телефона мы можем с Вами связаться? Указывайте пожалуйста номер телефона в международном формате.', reply_markup=client_keyboard.contact_kb)
            await FSMQuestion.client_phone.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.client_name.set()

#Получаем телефон клиента. Запрашиваем тип транспорта.
async def function_client_phone(message: types.Message, state: FSMContext):
#    if message.content_type == 'contact':
    if message.contact:
        async with state.proxy() as data:
            data['db_client_phone'] = message.contact.phone_number
        await message.answer(data['db_client_name']+', cкажите пожалуйста, для перевозки груза необходимы какие-то особые условия? Возможно груз является негабаритным, опасным, или скоропортящимся? Либо для его перевозки необходимо соблюдение температурного режима, наличие специальных разрешений, или какой-либо узкоспециализированный транспорт?', reply_markup=client_keyboard.choice_kb)
        await FSMQuestion.check_special.set()
    elif message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 20:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.client_phone.set()
        else:
            async with state.proxy() as data:
                data['db_client_phone'] = message.text
            await message.answer(data['db_client_name']+', cкажите пожалуйста, для перевозки груза необходимы какие-то особые условия? Возможно груз является негабаритным, опасным, или скоропортящимся? Либо для его перевозки необходимо соблюдение температурного режима, наличие специальных разрешений, или какой-либо узкоспециализированный транспорт?', reply_markup=client_keyboard.choice_kb)
            await FSMQuestion.check_special.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.client_phone.set()

#Клиент выбирает типа транспорта - стандартный (STANDART) или специальный (SPECIAL). Если не знает, то (DONT_KNOW).
#Если SPECIAL или DONT_KNOW - сохраняем БД и завершаем. Если STANDART - запрашиваем вид груза.
async def function_check_special(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in DONT_KNOW_SET:
            async with state.proxy() as data:
                data['db_check_special'] = 'DONT_KNOW'
                sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Idv2_R_zxhqo6j9SIY0oBIyJQskL46jo-vw3TKp-YI8/edit#gid=0')
                worksheet = sh.sheet1
                transaction = [data['db_current_datetime'], data['db_client_name'], data['db_client_phone'], data['db_check_special'], data['db_cargo'], data['db_veight'], data['db_kind_loading'], data['db_check_pallets'], data['db_pallets_count'], data['db_pallets_dimensions'], data['db_cargo_dimensions'], data['db_add_carcas'], data['db_addres_loading'], data['db_addres_docs'], data['db_addres_unloading'], data['db_date_loading'], data['db_date_unloading'], data['db_custom_export'], data['db_export_declaration'], data['db_custom_import'], data['db_insurance_cost'], data['db_attention']]
                worksheet.append_row(transaction)
            await message.answer('Спасибо за Ваш запрос, '+data['db_client_name']+'! Наш менеджер свяжется с Вами в ближайшее время для уточнения информации. До свидания!', reply_markup=client_keyboard.start_kb)
            await sqlite_db.sql_add_command(state)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in YES_SET:
            async with state.proxy() as data:
                data['db_check_special'] = 'SPECIAL'
                sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Idv2_R_zxhqo6j9SIY0oBIyJQskL46jo-vw3TKp-YI8/edit#gid=0')
                worksheet = sh.sheet1
                transaction = [data['db_current_datetime'], data['db_client_name'], data['db_client_phone'], data['db_check_special'], data['db_cargo'], data['db_veight'], data['db_kind_loading'], data['db_check_pallets'], data['db_pallets_count'], data['db_pallets_dimensions'], data['db_cargo_dimensions'], data['db_add_carcas'], data['db_addres_loading'], data['db_addres_docs'], data['db_addres_unloading'], data['db_date_loading'], data['db_date_unloading'], data['db_custom_export'], data['db_export_declaration'], data['db_custom_import'], data['db_insurance_cost'], data['db_attention']]
                worksheet.append_row(transaction)
            await message.answer('Спасибо за Ваш запрос, '+data['db_client_name']+'! Наш менеджер свяжется с Вами в ближайшее время для уточнения информации. До свидания!', reply_markup=client_keyboard.start_kb)
            await sqlite_db.sql_add_command(state)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in NO_SET:
            async with state.proxy() as data:
                data['db_check_special'] = 'STANDART'
            await message.answer('Опишите пожалуйста коротко, какой именно груз Вам необходимо перевезти?', reply_markup=ReplyKeyboardRemove())
            await FSMQuestion.cargo.set()
        else:
            async with state.proxy() as data:
                await message.answer(data['db_client_name']+', повторяю вопрос - для перевозки груза необходимы какие-то особые условия? Возможно груз является негабаритным, опасным, или скоропортящимся? Либо для его перевозки необходимо соблюдение температурного режима, наличие специальных разрешений, или какой-либо узкоспециализированный транспорт?', reply_markup=client_keyboard.choice_kb)
                await FSMQuestion.check_special.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.check_special.set()

#Получаем вид грузза. Запрашиваем массу груза.
async def function_cargo(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 100:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.cargo.set()
        else:
            async with state.proxy() as data:
                data['db_cargo'] = message.text
            await message.answer('Какова масса груза брутто? (Вместе с тарой)')
            await FSMQuestion.veight.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.cargo.set()

#Получаем массу грузза. Запрашиваем вид погрузки.
async def function_veight(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 10:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.veight.set()
        else:
            async with state.proxy() as data:
                data['db_veight'] = message.text
            await message.answer('Укажите пожалуйста способ погрузки (верхняя, боковая, задняя). Вы так же можете указать несколько типов погрузки, или даже все.')
            await FSMQuestion.kind_loading.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.veight.set()

#Получаем способ загрузки. Выясняем опалечен ли груз.
async def function_kind_loading(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 30:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.kind_loading.set()
        else:
            async with state.proxy() as data:
                data['db_kind_loading'] = message.text
            await message.answer('Ваш груз опалечен?', reply_markup=client_keyboard.choice_kb)
            await FSMQuestion.check_pallets.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.kind_loading.set()

#Клиент отвечает находится ли груз на паллетах (PALLETS), или нет (NOT_PALLETS). Если не знает, то DONT_KNOW.
#Если PALLETS - запрашиваем количество паллет. Если NOT_PALLETS - габариты или объем груза.
async def function_check_pallets(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in DONT_KNOW_SET:
            async with state.proxy() as data:
                data['db_check_pallets'] = 'DONT_KNOW'
                sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Idv2_R_zxhqo6j9SIY0oBIyJQskL46jo-vw3TKp-YI8/edit#gid=0')
                worksheet = sh.sheet1
                transaction = [data['db_current_datetime'], data['db_client_name'], data['db_client_phone'], data['db_check_special'], data['db_cargo'], data['db_veight'], data['db_kind_loading'], data['db_check_pallets'], data['db_pallets_count'], data['db_pallets_dimensions'], data['db_cargo_dimensions'], data['db_add_carcas'], data['db_addres_loading'], data['db_addres_docs'], data['db_addres_unloading'], data['db_date_loading'], data['db_date_unloading'], data['db_custom_export'], data['db_export_declaration'], data['db_custom_import'], data['db_insurance_cost'], data['db_attention']]
                worksheet.append_row(transaction)
            await message.answer('Спасибо за Ваш запрос, '+data['db_client_name']+'! Наш менеджер свяжется с Вами в ближайшее время для уточнения информации. До свидания!', reply_markup=client_keyboard.start_kb)
            await sqlite_db.sql_add_command(state)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in YES_SET:
            async with state.proxy() as data:
                data['db_check_pallets'] = 'PALLETS'
            await message.answer('Сколько всего паллет?', reply_markup=ReplyKeyboardRemove())
            await FSMQuestion.pallets_count.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in NO_SET:
            async with state.proxy() as data:
                data['db_check_pallets'] = 'NOT_PALLETS'
            await message.answer('Каковы габариты или объем Вашего груза? Пожалуйста не забудьте указать единицы измерения', reply_markup=ReplyKeyboardRemove())
            await FSMQuestion.cargo_dimensions.set()
        else:
            async with state.proxy() as data:
                await message.answer(data['db_client_name']+', повторяю вопрос - ваш груз опалечен?', reply_markup=client_keyboard.choice_kb)
                await FSMQuestion.check_pallets.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.check_pallets.set()

#Если PALLETS, то получаем количество паллет. Запрашиваем размеры паллет
async def function_pallets_count(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 10:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.pallets_count.set()
        else:
            async with state.proxy() as data:
                data['db_pallets_count'] = message.text
            await message.answer('Какого размера паллеты? (ДхШхВ)')
            await FSMQuestion.pallets_dimensions.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.pallets_count.set()

#Если PALLETS, то получаем размеры паллет. Запрашиваем дополнительный крепеж
async def function_pallets_dimensions(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 50:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.pallets_dimensions.set()
        else:
            async with state.proxy() as data:
                data['db_pallets_dimensions'] = message.text
            await message.answer(data['db_client_name']+', cообщите, если для крепления груза необходимы дополнительные ремни или обрешетка', reply_markup=client_keyboard.need_or_not_kb)
            await FSMQuestion.add_carcas.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.pallets_dimensions.set()

#Если NOT_PALLETS - получаем габариты или объем груза. Запрашиваем дополнительный крепеж
async def function_cargo_dimensions(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 100:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.cargo_dimensions.set()
        else:
            async with state.proxy() as data:
                data['db_cargo_dimensions'] = message.text
            await message.answer(data['db_client_name']+', cообщите, если для крепления груза необходимы дополнительные ремни или обрешетка', reply_markup=client_keyboard.need_or_not_kb)
            await FSMQuestion.add_carcas.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.cargo_dimensions.set()

#Получаем дополнительный крепеж. Запрашиваем адрес погрузки
async def function_add_carcas(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 100:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.add_carcas.set()
        else:
            async with state.proxy() as data:
                data['db_add_carcas'] = message.text
            await message.answer('По какому адресу забираем груз?', reply_markup=ReplyKeyboardRemove())
            await FSMQuestion.addres_loading.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.add_carcas.set()

#Получаем адрес погрузки. Запрашиваем адрес оформления
async def function_addres_loading(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 100:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.addres_loading.set()
        else:
            async with state.proxy() as data:
                data['db_addres_loading'] = message.text
            await message.answer('Документы на груз получаем в пункте погрузки?', reply_markup=client_keyboard.choice_kb)
            await FSMQuestion.addres_docs.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.addres_loading.set()

#Получаем адрес оформления.
async def function_addres_docs(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in YES_SET:
            async with state.proxy() as data:
                data['db_addres_docs'] = data['db_addres_loading']
            await message.answer('Укажите пожалуйста адрес выгрузки', reply_markup=ReplyKeyboardRemove())
            await FSMQuestion.addres_unloading.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in NO_SET:
            await message.answer('А по какому адресу получаем документы на груз?')
            await FSMQuestion.addres_docs_extended.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in DONT_KNOW_SET:
            async with state.proxy() as data:
                data['db_addres_docs'] = 'DONT_KNOW'
            await message.answer('Укажите пожалуйста адрес выгрузки', reply_markup=ReplyKeyboardRemove())
            await FSMQuestion.addres_unloading.set()
        else:
            async with state.proxy() as data:
                await message.answer(data['db_client_name']+', повторяю вопрос - документы на груз получаем в пункте погрузки?', reply_markup=client_keyboard.choice_kb)
                await FSMQuestion.addres_docs.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.addres_docs.set()

#Если адрес погрузки и адрес оформления не совпадают, то получаем адрес оформления и запрашиваем адрес выгрузки.
async def function_addres_docs_extended(message: types.Message, state: FSMContext):
    if message.text:
        if len(message.text) > 100:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.addres_docs_extended.set()
        else:
            async with state.proxy() as data:
                data['db_addres_docs'] = message.text
            await message.answer('Укажите пожалуйста адрес выгрузки', reply_markup=ReplyKeyboardRemove())
            await FSMQuestion.addres_unloading.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.addres_docs_extended.set()

#Получаем адрес выгрузки. Запрашиваем дату погрузки
async def function_addres_unloading(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 100:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.addres_unloading.set()
        else:
            async with state.proxy() as data:
                data['db_addres_unloading'] = message.text
            await message.answer('Когда груз готов к погрузке?', reply_markup=ReplyKeyboardRemove())
            await FSMQuestion.date_loading.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.addres_unloading.set()

#Получаем дату погрузки. Запрашиваем дату доставки
async def function_date_loading(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 50:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.date_loading.set()
        else:
            async with state.proxy() as data:
                data['db_date_loading'] = message.text
            await message.answer('Когда необходимо доставить груз грузополучателю?')
            await FSMQuestion.date_unloading.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.date_loading.set()

#Получаем дату выгрузки. Запрашиваем таможенное оформление
async def function_date_unloading(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 50:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.date_unloading.set()
        else:
            async with state.proxy() as data:
                data['db_date_unloading'] = message.text
            await message.answer('Необходимо ли таможенное оформление?', reply_markup=client_keyboard.choice_kb)
            await FSMQuestion.custom.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.date_unloading.set()

#Получаем необходимость таможенного оформления. Если нужно - запрашиваем таможню вывоза, если нет - прочие замечания.
async def function_custom(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in YES_SET:
            async with state.proxy() as data:
                data['db_custom'] = 'YES'
            await message.answer('Укажите пожалуйста пункт таможни экспорта', reply_markup=client_keyboard.custom_kb)
            await FSMQuestion.custom_export.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in NO_SET:
            async with state.proxy() as data:
                data['db_custom'] = 'NO'
            await message.answer('Если у Вас есть какие-то прочие замечания, пожелания, или предложения по этой доставке, то напишите их', reply_markup=client_keyboard.no_kb)
            await FSMQuestion.attention.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in DONT_KNOW_SET:
            async with state.proxy() as data:
                data['db_custom'] = 'DONT_KNOW'
            await message.answer('Если у Вас есть какие-то прочие замечания, пожелания, или предложения по этой доставке, то напишите их', reply_markup=client_keyboard.no_kb)
            await FSMQuestion.attention.set()
        else:
            async with state.proxy() as data:
                await message.answer(data['db_client_name']+', повторяю вопрос - необходимо ли таможенное оформление?', reply_markup=client_keyboard.choice_kb)
                await FSMQuestion.custom.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.custom.set()

#Получаем таможню вывоза. Запрашиваем оформление экспортной декларации
async def function_custom_export(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 100:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.custom_export.set()
        else:
            async with state.proxy() as data:
                data['db_custom_export'] = message.text
            await message.answer('Кто оформляет документы для экспорта - грузоотправитель или перевозчик?', reply_markup=client_keyboard.ex_kb)
            await FSMQuestion.export_declaration.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.custom_export.set()

#Получаем условия поставки. Запрашиваем таможню ввоза
async def function_export_declaration(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 50:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.export_declaration.set()
        else:
            async with state.proxy() as data:
                data['db_export_declaration'] = message.text
            await message.answer('Укажите пожалуйста пункт таможни импорта', reply_markup=client_keyboard.custom_kb)
            await FSMQuestion.custom_import.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.export_declaration.set()

#Получаем таможню ввоза. Запрашиваем необходимость страхования
async def function_custom_import(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 100:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.custom_import.set()
        else:
            async with state.proxy() as data:
                data['db_custom_import'] = message.text
            await message.answer('Хотите ли застраховать груз?', reply_markup=client_keyboard.choice_kb)
            await FSMQuestion.insurance.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.custom_import.set()

#Получаем необходимость страхования. Если нужно - запрашиваем сумму страхования, если нет - прочие замечания
async def function_insurance(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in YES_SET:
            await message.answer('На какую сумму?', reply_markup=ReplyKeyboardRemove())
            await FSMQuestion.insurance_cost.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in NO_SET:
            async with state.proxy() as data:
                data['db_insurance_cost'] = 'Без страхования'
            await message.answer('Если у Вас есть какие-то прочие замечания, пожелания, или предложения по этой доставке, то напишите их', reply_markup=client_keyboard.no_kb)
            await FSMQuestion.attention.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in DONT_KNOW_SET:
            async with state.proxy() as data:
                data['db_insurance_cost'] = 'Уточнить необходимость страхования'
            await message.answer('Если у Вас есть какие-то прочие замечания, пожелания, или предложения по этой доставке, то напишите их', reply_markup=client_keyboard.no_kb)
            await FSMQuestion.attention.set()
        else:
            async with state.proxy() as data:
                await message.answer(data['db_client_name']+', повторяю вопрос - хотите ли застраховать груз?', reply_markup=client_keyboard.choice_kb)
                await FSMQuestion.insurance.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.insurance.set()

#Получаем cумму страхования. Запрашиваем прочие замечания
async def function_insurance_cost(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 20:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.insurance_cost.set()
        else:
            async with state.proxy() as data:
                data['db_insurance_cost'] = message.text
            await message.answer('Если у Вас есть какие-то прочие замечания, пожелания, или предложения по этой доставке, то напишите их', reply_markup=client_keyboard.no_kb)
            await FSMQuestion.attention.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.insurance_cost.set()

#Получаем прочие замечания. Начинаем проверку
async def function_attention(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif len(message.text) > 200:
            await message.answer('Ваше сообщение слишком длинное. Сформулируйте пожалуйста покороче.')
            await FSMQuestion.attention.set()
        else:
            async with state.proxy() as data:
                data['db_attention'] = message.text
            if data['db_check_pallets'] == 'PALLETS':
                await message.answer('Итак, '+data['db_client_name']+', давайте проверим все ли я записал верно:\nВаш груз - '+data['db_cargo']+',\nмасса брутто составляет - '+data['db_veight']+',\nвид погрузки - '+data['db_kind_loading']+',\nгруз находится на паллетах - '+data['db_pallets_dimensions']+' в количестве - '+data['db_pallets_count']+'шт.'+',\nдополнительные ремни или обрешетка - '+data['db_add_carcas']+'.\nВсе верно?', reply_markup=client_keyboard.choice_kb)
                await FSMQuestion.check_data_1.set()
            elif data['db_check_pallets'] == 'NOT_PALLETS':
                await message.answer('Итак, '+data['db_client_name']+', давайте проверим все ли я записал верно:\nВаш груз - '+data['db_cargo']+',\nмасса брутто составляет - '+data['db_veight']+',\nвид погрузки - '+data['db_kind_loading']+',\nгруз находится без паллет и занимает в кузове - '+data['db_cargo_dimensions']+',\nдополнительные ремни или обрешетка - '+data['db_add_carcas']+'.\nВсе верно?', reply_markup=client_keyboard.choice_kb)
                await FSMQuestion.check_data_1.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.attention.set()

#Проверка 1
async def function_check_data_1(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in YES_SET:
            async with state.proxy() as data:
                if data['db_addres_docs'] == 'DONT_KNOW':
                    await message.answer('Еще немного:\nгруз забираем в '+data['db_addres_loading']+' '+data['db_date_loading']+',\nи должны доставить груз '+data['db_date_unloading']+' в '+data['db_addres_unloading']+'.\nТаможенное оформление при осуществлении перевозки не требуется, а адрес оформления документов на груз мы уточним у Вас по телефону.\nВсе правильно?', reply_markup=client_keyboard.choice_kb)
                    await FSMQuestion.check_data_3.set()
                else:
                    async with state.proxy() as data:
                        if data['db_custom'] == 'NO':
                            await message.answer('Еще немного:\nгруз забираем в '+data['db_addres_loading']+' '+data['db_date_loading']+',\nдокументы на груз получаем в '+data['db_addres_docs']+',\nи должны доставить груз '+data['db_date_unloading']+' в '+data['db_addres_unloading']+'.\nТаможенное оформление при осуществлении перевозки не требуется.\nВсе правильно?', reply_markup=client_keyboard.choice_kb)
                            await FSMQuestion.check_data_3.set()
                        elif data['db_custom'] == 'DONT_KNOW':
                            await message.answer('Еще немного:\nгруз забираем в '+data['db_addres_loading']+' '+data['db_date_loading']+',\nдокументы на груз получаем в '+data['db_addres_docs']+',\nи должны доставить груз '+data['db_date_unloading']+' в '+data['db_addres_unloading']+'.\nНеобходимость таможенного оформление мы уточним у Вас по телефону\nВсе правильно?', reply_markup=client_keyboard.choice_kb)
                            await FSMQuestion.check_data_3.set()
                        else:
                            await message.answer('Еще немного:\nгруз забираем в '+data['db_addres_loading']+' '+data['db_date_loading']+',\nдокументы на груз получаем в '+data['db_addres_docs']+',\nи должны доставить груз '+data['db_date_unloading']+' в '+data['db_addres_unloading']+'.\nВсе правильно?', reply_markup=client_keyboard.choice_kb)
                            await FSMQuestion.check_data_2.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in NO_SET:
            async with state.proxy() as data:
                await message.answer(data['db_client_name']+', давайте проверим еще раз. Для начала опишите пожалуйста коротко, какой именно груз Вам необходимо перевезти?', reply_markup=ReplyKeyboardRemove())
                await FSMQuestion.cargo.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in DONT_KNOW_SET:
            async with state.proxy() as data:
                await message.answer(data['db_client_name']+', давайте проверим еще раз. Для начала пишите пожалуйста коротко, какой именно груз Вам необходимо перевезти?', reply_markup=ReplyKeyboardRemove())
                await FSMQuestion.cargo.set()
        else:
            async with state.proxy() as data:
                data['db_attention'] = message.text
            if data['db_check_pallets'] == 'PALLETS':
                await message.answer('И все же, '+data['db_client_name']+', необходимо проверить все ли я записал верно:\nВаш груз - '+data['db_cargo']+',\nмасса брутто составляет - '+data['db_veight']+',\nвид погрузки - '+data['db_kind_loading']+',\nгруз находится на паллетах - '+data['db_pallets_dimensions']+' в количестве - '+data['db_pallets_count']+'шт.'+',\nдополнительные ремни или обрешетка - '+data['db_add_carcas']+'.\nВсе верно?', reply_markup=client_keyboard.choice_kb)
                await FSMQuestion.attention.set()
            elif data['db_check_pallets'] == 'NOT_PALLETS':
                await message.answer('И все же, нам необходимо проверить все ли я записал верно:\nВаш груз - '+data['db_cargo']+',\nмасса брутто составляет - '+data['db_veight']+',\nвид погрузки - '+data['db_kind_loading']+',\nгруз находится без паллет и занимает в кузове - '+data['db_cargo_dimensions']+',\nдополнительные ремни или обрешетка - '+data['db_add_carcas']+'.\nВсе верно?', reply_markup=client_keyboard.choice_kb)
                await FSMQuestion.attention.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.check_data_1.set()

#Проверка 2
async def function_check_data_2(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in NO_SET:
            async with state.proxy() as data:
                await message.answer(data['db_client_name']+', давайте проверим еще раз. Для начала сообщите по какому адресу необходимо забрать груз?', reply_markup=ReplyKeyboardRemove())
                await FSMQuestion.addres_loading.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in DONT_KNOW_SET:
            async with state.proxy() as data:
                await message.answer(data['db_client_name']+', давайте проверим еще раз. Для начала сообщите по какому адресу необходимо забрать груз?', reply_markup=ReplyKeyboardRemove())
                await FSMQuestion.addres_loading.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in YES_SET:
            async with state.proxy() as data:
                if data['db_custom'] == 'YES':
                    await message.answer('И последнее:\nтаможня вывоза будет - '+data['db_custom_export']+',\nдокументы на экспорт оформляет - '+data['db_export_declaration']+',\nтаможня ввоза будет - '+data['db_custom_import']+',\nгруз страхуем на сумму - '+data['db_insurance_cost']+'.\nЯ все точно записал?', reply_markup=client_keyboard.choice_kb)
                    await FSMQuestion.check_data_3.set()
                else:
                    await message.answer('Ой! Кажется Вы меня сломали (((')
                    await state.finish()
        else:
            async with state.proxy() as data:
                if data['db_addres_docs'] == 'DONT_KNOW':
                    await message.answer('И все же нам необходимо проверить:\nгруз забираем в '+data['db_addres_loading']+' '+data['db_date_loading']+',\nи должны доставить груз '+data['db_date_unloading']+' в '+data['db_addres_unloading']+'.\nТаможенное оформление при осуществлении перевозки не требуется, а адрес оформления документов на груз мы уточним у Вас по телефону.\nВсе правильно?', reply_markup=client_keyboard.choice_kb)
                    await FSMQuestion.check_data_1.set()
                else:
                    async with state.proxy() as data:
                        if data['db_custom'] == 'NO':
                            await message.answer('И все же нам необходимо проверить:\nгруз забираем в '+data['db_addres_loading']+' '+data['db_date_loading']+',\nдокументы на груз получаем в '+data['db_addres_docs']+',\nи должны доставить груз '+data['db_date_unloading']+' в '+data['db_addres_unloading']+'.\nТаможенное оформление при осуществлении перевозки не требуется.\nВсе правильно?', reply_markup=client_keyboard.choice_kb)
                            await FSMQuestion.check_data_1.set()
                        elif data['db_custom'] == 'DONT_KNOW':
                            await message.answer('И все же нам необходимо проверить:\nгруз забираем в '+data['db_addres_loading']+' '+data['db_date_loading']+',\nдокументы на груз получаем в '+data['db_addres_docs']+',\nи должны доставить груз '+data['db_date_unloading']+' в '+data['db_addres_unloading']+'.\nНеобходимость таможенного оформление мы уточним у Вас по телефону\nВсе правильно?', reply_markup=client_keyboard.choice_kb)
                            await FSMQuestion.check_data_1.set()
                        else:
                            await message.answer('И все же нам необходимо проверить:\nгруз забираем в '+data['db_addres_loading']+' '+data['db_date_loading']+',\nдокументы на груз получаем в '+data['db_addres_docs']+',\nи должны доставить груз '+data['db_date_unloading']+' в '+data['db_addres_unloading']+'.\nВсе правильно?', reply_markup=client_keyboard.choice_kb)
                            await FSMQuestion.check_data_1.set()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.check_data_2.set()

#Проверка 3
async def function_check_data_3(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
            await message.answer('Это было грубо! В следующий раз выбирайте выражения пожалуйста!', reply_markup=client_keyboard.start_kb)
            await message.delete()
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in STOP_SET:
            await message.answer('До свидания!', reply_markup=client_keyboard.start_kb)
            await state.finish()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in NO_SET:
            async with state.proxy() as data:
                if data['db_custom'] == 'YES':
                    await message.answer(data['db_client_name'] + ', давайте проверим еще раз. Для начала подскажите где находится таможня вывоза?', reply_markup=client_keyboard.custom_kb)
                    await FSMQuestion.custom_export.set()
                elif data['db_custom'] == 'NO':
                    await message.answer(data['db_client_name'] + ', давайте проверим еще раз. Для начала сообщите по какому адресу необходимо забрать груз?', reply_markup=ReplyKeyboardRemove())
                    await FSMQuestion.addres_loading.set()
                elif data['db_custom'] == 'DONT_KNOW':
                    await message.answer(data['db_client_name'] + ', давайте проверим еще раз. Для начала сообщите по какому адресу необходимо забрать груз?', reply_markup=ReplyKeyboardRemove())
                    await FSMQuestion.addres_loading.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in DONT_KNOW_SET:
            async with state.proxy() as data:
                if data['db_custom'] == 'YES':
                    await message.answer(data['db_client_name'] + ', давайте проверим еще раз. Для начала подскажите где находится таможня вывоза?', reply_markup=client_keyboard.custom_kb)
                    await FSMQuestion.custom_export.set()
                elif data['db_custom'] == 'NO':
                    await message.answer(data['db_client_name'] + ', давайте проверим еще раз. Для начала сообщите по какому адресу необходимо забрать груз?', reply_markup=ReplyKeyboardRemove())
                    await FSMQuestion.addres_loading.set()
                elif data['db_custom'] == 'DONT_KNOW':
                    await message.answer(data['db_client_name'] + ', давайте проверим еще раз. Для начала сообщите по какому адресу необходимо забрать груз?', reply_markup=ReplyKeyboardRemove())
                    await FSMQuestion.addres_loading.set()
        elif message.text.lower().translate(str.maketrans('', '', string.punctuation)) in YES_SET:
            async with state.proxy() as data:
                await message.answer('Спасибо, '+data['db_client_name']+'! Ваша заявка принята. Наш менеджер свяжется с Вами в ближайшее время с конкретным предложением. Всего хорошего!', reply_markup=client_keyboard.start_kb)
                sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Idv2_R_zxhqo6j9SIY0oBIyJQskL46jo-vw3TKp-YI8/edit#gid=0')
                worksheet = sh.sheet1
                transaction = [data['db_current_datetime'], data['db_client_name'], data['db_client_phone'], data['db_check_special'], data['db_cargo'], data['db_veight'], data['db_kind_loading'], data['db_check_pallets'], data['db_pallets_count'], data['db_pallets_dimensions'], data['db_cargo_dimensions'], data['db_add_carcas'], data['db_addres_loading'], data['db_addres_docs'], data['db_addres_unloading'], data['db_date_loading'], data['db_date_unloading'], data['db_custom_export'], data['db_export_declaration'], data['db_custom_import'], data['db_insurance_cost'], data['db_attention']]
                worksheet.append_row(transaction)
            await sqlite_db.sql_add_command(state)
            await state.finish()
        else:
            async with state.proxy() as data:
                if data['db_custom'] == 'YES':
                    await message.answer('И все же нам необходимо проверить:\nтаможня вывоза будет - '+data['db_custom_export']+',\nдокументы на экспорт оформляет - '+data['db_export_declaration']+',\nтаможня ввоза будет - '+data['db_custom_import']+',\nгруз страхуем на сумму - '+data['db_insurance_cost']+'.\nЯ все точно записал?', reply_markup=client_keyboard.choice_kb)
                    await FSMQuestion.check_data_2.set()
                else:
                    await message.answer('Ой! Кажется Вы меня сломали (((')
                    await state.finish()
    else:
        await message.answer('Я могу принимать только текстовые сообщения. Давайте попробуем еще раз.')
        await FSMQuestion.check_data_3.set()


def register_handlers_questionnaire(dp: Dispatcher):
    dp.register_message_handler(begin, commands=['start', 'старт', 'привет'], state=None)
    dp.register_message_handler(function_client_name, state=FSMQuestion.client_name, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_client_phone, state=FSMQuestion.client_phone, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_check_special, state=FSMQuestion.check_special, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_cargo, state=FSMQuestion.cargo, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_veight, state=FSMQuestion.veight, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_kind_loading, state=FSMQuestion.kind_loading, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_check_pallets, state=FSMQuestion.check_pallets, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_pallets_count, state=FSMQuestion.pallets_count, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_pallets_dimensions, state=FSMQuestion.pallets_dimensions, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_cargo_dimensions, state=FSMQuestion.cargo_dimensions, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_add_carcas, state=FSMQuestion.add_carcas, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_addres_loading, state=FSMQuestion.addres_loading, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_addres_docs, state=FSMQuestion.addres_docs, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_addres_docs_extended, state=FSMQuestion.addres_docs_extended, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_addres_unloading, state=FSMQuestion.addres_unloading, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_date_loading, state=FSMQuestion.date_loading, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_date_unloading, state=FSMQuestion.date_unloading, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_custom, state=FSMQuestion.custom, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_custom_export, state=FSMQuestion.custom_export, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_export_declaration, state=FSMQuestion.export_declaration, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_custom_import, state=FSMQuestion.custom_import, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_insurance, state=FSMQuestion.insurance, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_insurance_cost, state=FSMQuestion.insurance_cost, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_attention, state=FSMQuestion.attention, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_check_data_1, state=FSMQuestion.check_data_1, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_check_data_2, state=FSMQuestion.check_data_2, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(function_check_data_3, state=FSMQuestion.check_data_3, content_types=types.ContentTypes.ANY)
