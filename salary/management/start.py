from datetime import datetime

from telegram import ReplyKeyboardMarkup, KeyboardButton, Update, InlineKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto
from telegram.ext import CallbackContext

from ..models import Workers, Date


start_letter = "Assalom alaykum Radius.uz kompaniyasining Ish haqi buyicha telegram botiga xush kelibsiz!"
start_button = ReplyKeyboardMarkup([[KeyboardButton('Boshlash'), KeyboardButton('Tugatish')],
                                    [KeyboardButton('Ish haqqi haqidagi malumot')]], resize_keyboard=True, one_time_keyboard=True)
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
        Workers.objects.filter(telegram_id=user_id).update(step=0)
    else:
        update.message.reply_text('Siz Radius.uz kompaniyasida ishlamaysiz yoki hali ruyxatdan utmagansiz!')


def begin(update, context):
    user_id = update.message.from_user.id
    msg = update.message.text
    photo = update.message.photo
    step = Workers.objects.get(telegram_id=user_id)
    if user_id in worders_list():
        if msg=='Boshlash' and step.step == 0:
            update.message.reply_text('Rasm yuboring')
            Workers.objects.filter(telegram_id=user_id).update(step=1)
            Workers.objects.filter(telegram_id=user_id).update(type='Boshlash')

        elif msg=='Tugatish' and step.step == 0:
            update.message.reply_text('Rasm yuboring')

            Workers.objects.filter(telegram_id=user_id).update(step=1)
            Workers.objects.filter(telegram_id=user_id).update(type='Tugatish')



        elif step.step ==1 and Workers.objects.get(telegram_id=user_id).type == 'Boshlash':
            Workers.objects.filter(telegram_id=user_id).update(step=2)
            Workers.objects.filter(telegram_id=user_id).update(start_work=photo[0].file_id)
            print(Workers.objects.get(telegram_id=user_id).full_name)
            date = Date.objects.create(worker=Workers.objects.get(telegram_id=user_id).full_name)
            date.save()
            Date.objects.filter(worker=Workers.objects.get(telegram_id=user_id).full_name)
            update.message.reply_text('Adminga yuborish uchun Yuborish tugmasini bosing!',
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Yuborish!')]],
                                                                       resize_keyboard=True, one_time_keyboard=True))

        elif step.step == 1 and Workers.objects.get(telegram_id=user_id).type == 'Tugatish':
            Workers.objects.filter(telegram_id=user_id).update(step=2)
            Workers.objects.filter(telegram_id=user_id).update(end_work=photo[0].file_id)
            update.message.reply_text('Adminga yuborish uchun Yuborish tugmasini bosing!',
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Yuborish!')]],
                                                                       resize_keyboard=True, one_time_keyboard=True))

        elif step.step == 2 and msg == 'Yuborish!':
            Workers.objects.filter(telegram_id=user_id).update(step=0)

            context.bot.send_media_group(chat_id='990254417', media=[InputMediaPhoto(f'{step.start_work}',
                                                                                     caption=f"Xodim: {step.full_name}\nType: {step.type}\nVaqt: {datetime.now()}")])

            update.message.reply_text("Xabar adminga yuborildi",
                                      reply_markup=start_button)



        elif msg == 'Ish haqqi haqidagi malumot':

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


def inline(update: Update, context : CallbackContext):
    data = update.callback_query.data
    user_id = update.callback_query.from_user.id
    if data=='send':
        obj = Workers.objects.all()


        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text="",
                                 reply_markup=start_button)
    elif data == "back":
        update.callback_query.message.delete()
        Workers.objects.filter(telegram_id=user_id).update(step=0)
        context.bot.delete_message(chat_id=update.callback_query.from_user.id,
                                   message_id=update.callback_query.message.message_id - 1)

