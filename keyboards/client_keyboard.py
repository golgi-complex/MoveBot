from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_button = KeyboardButton('/start')
yes_button = KeyboardButton('Да')
no_button = KeyboardButton('Нет')
dont_know_button = KeyboardButton('Не знаю')
contact_button = KeyboardButton('Отправить номер телефона', request_contact=True)
dont_need_button = KeyboardButton('Не нужно')
shipper_button = KeyboardButton('Грузоотправитель')
transporter_button = KeyboardButton('Перевозчик')
custom_button = KeyboardButton('На месте')

start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(start_button)
choice_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(yes_button).insert(no_button).insert(dont_know_button)
contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, ).add(contact_button)
need_or_not_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(dont_need_button).insert(dont_know_button)
ex_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(shipper_button).insert(transporter_button)
custom_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(custom_button)
no_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(no_button)
