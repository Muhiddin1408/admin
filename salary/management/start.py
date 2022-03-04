from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import CallbackContext

from ..models import Workers


start_letter = "Assalom alaykum Radius.uz kompaniyasining Ish haqi buyicha telegram botiga xush kelibsiz!"
start_button = ReplyKeyboardMarkup([[KeyboardButton('🔛Boshlash')]], resize_keyboard=True, one_time_keyboard=True)
salary_button = ReplyKeyboardMarkup([[KeyboardButton('Ish haqi'), KeyboardButton('Bonus+')],
                                    [KeyboardButton('Jarima'),KeyboardButton('Avans'),],
                                    [KeyboardButton('Qoldiq')]], resize_keyboard=True, one_time_keyboard=True)

def worders_list():
    lists = []
    managers = Workers.objects.all()
    for i in managers:
        lists.append(int(i.telegram_id))
    return lists


def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user = update.message.from_user.username
    if user_id in worders_list():
        update.message.reply_text(start_letter, reply_markup=start_button)
    else:
        update.message.reply_text('Siz Radius.uz kompaniyasida ishlamaysiz yoki hali ruyxatdan utmagansiz!')


def begin(update, context):
    user_id = update.message.from_user.id
    msg = update.message.text
    if user_id in worders_list():
        if msg == '🔛Boshlash':
            update.message.reply_text('Siz qaysi turdagi ish haqini kurmoqchisiz!', reply_markup=salary_button)
        elif msg == 'Ish haqi':
            salary = Workers.objects.get(telegram_id=user_id).salary
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {salary} so\'m', reply_markup=salary_button)
        elif msg == 'Bonus+':
            bons = Workers.objects.get(telegram_id=user_id).bons
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {bons} so\'m', reply_markup=salary_button)
        elif msg == 'Jarima':
            fine = Workers.objects.get(telegram_id=user_id).fine
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {fine} so\'m', reply_markup=salary_button)
        elif msg == 'Avans':
            give = Workers.objects.get(telegram_id=user_id).give
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {give} so\'m', reply_markup=salary_button)
        elif msg == 'Qoldiq':
            give = Workers.objects.get(telegram_id=user_id).residue
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {give} so\'m', reply_markup=salary_button)
