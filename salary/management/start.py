from datetime import datetime, time
# import datetime,time
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update, InlineKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto
from telegram.ext import CallbackContext

from ..models import Workers, Date


start_letter = "Assalom alaykum Radius.uz kompaniyasining Ish haqi buyicha telegram botiga xush kelibsiz!"
start_button = ReplyKeyboardMarkup([[KeyboardButton('Boshlash')],
                                    [KeyboardButton('Ish haqqi haqidagi malumot')]], resize_keyboard=True, one_time_keyboard=True)
end_button = ReplyKeyboardMarkup([[KeyboardButton('Tugatish')],
                                 [KeyboardButton('Ish haqqi haqidagi malumot')]], resize_keyboard=True, one_time_keyboard=True)
salary_button = ReplyKeyboardMarkup([[KeyboardButton('Ish haqi'), KeyboardButton('Bonus+')],
                                    [KeyboardButton('Jarima'), KeyboardButton('Avans'), ],
                                    [KeyboardButton('Qoldiq')]], resize_keyboard=True, one_time_keyboard=True)


def worders_list():
    lists = []
    managers = Workers.objects.all()
    for i in managers:
        lists.append(int(i.telegram_id))
    return lists


def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
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
        if msg == 'Boshlash' and step.step == 0:
            update.message.reply_text('Rasm yuboring')
            Workers.objects.filter(telegram_id=user_id).update(step=1)
            Workers.objects.filter(telegram_id=user_id).update(type='Boshlash')

        elif msg == 'Tugatish' and step.step == 3:
            update.message.reply_text('Rasm yuboring')

            Workers.objects.filter(telegram_id=user_id).update(step=4)
            Workers.objects.filter(telegram_id=user_id).update(type='Tugatish')

        elif step.step == 1:
            a = datetime.now()
            Workers.objects.filter(telegram_id=user_id).update(step=2)
            Workers.objects.filter(telegram_id=user_id).update(image=photo[0].file_id)
            Workers.objects.filter(telegram_id=user_id).update(clock_in=a.strftime('%H:%M'))
            Workers.objects.filter(telegram_id=user_id).update(month=a.strftime('%Y.%m.%d'))

            update.message.reply_text('Adminga yuborish uchun Yuborish tugmasini bosing!',
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Yuborish!')]],
                                                                       resize_keyboard=True, one_time_keyboard=True))

        elif step.step == 4:
            Workers.objects.filter(telegram_id=user_id).update(step=5)
            Workers.objects.filter(telegram_id=user_id).update(image=photo[0].file_id)
            Workers.objects.filter(telegram_id=user_id).update(clock_out=datetime.now().strftime('%H:%M'))
            obj = Workers.objects.get(telegram_id=user_id)

            def time_diff(clock_out, clock_in):

                in_ = str(clock_out).split(":")
                in_d = int(in_[0])*60*60+int(in_[1])*60
                out_ = str(clock_in).split(":")
                out_d = int(out_[0])*60*60+int(out_[1])*60
                dt = abs(out_d - in_d)

                if dt >= 3600:
                    hours = dt//3600

                    mint = dt % 3600//60
                else:
                    hours = 0
                    mint = dt % 3600//60
                hours = str(hours)
                mint = str(mint)
                out = hours+":"+mint
                return out
            m = str(obj.month).split('.')
            b = int(m[1])
            if b == 1:
                type_m = 'yanvar'
            elif b == 2:
                type_m = 'fevral'
            elif b == 3:
                type_m = 'mart'
            elif b == 4:
                type_m = 'aprel'
            elif b == 5:
                type_m = 'may'
            elif b == 6:
                type_m = 'iyun'
            elif b == 7:
                type_m = 'iyul'
            elif b == 8:
                type_m = 'avgust'

            elif b == 9:
                type_m = 'sentiyabr'
            elif b == 10:
                type_m = 'oktiyabr'

            elif b == 11:
                type_m = 'noyabr'
            elif b == 12:
                type_m = 'dekabr'
            a = int(m[2])

            data = Date.objects.create(
                worker=obj,
                clock_in=obj.clock_in,
                clock_out=obj.clock_out,
                work=time_diff(obj.clock_out, obj.clock_in),
                month=a,
                type_month=type_m)
            data.save()
            update.message.reply_text('Adminga yuborish uchun Yuborish tugmasini bosing!',
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Yuborish!')]],
                                                                       resize_keyboard=True, one_time_keyboard=True))

        elif step.step == 2 and msg == 'Yuborish!':
            Workers.objects.filter(telegram_id=user_id).update(step=3)

            context.bot.send_media_group(chat_id='990254417', media=[InputMediaPhoto(f'{step.image}',
                                                                                     caption=f"Xodim: {step.full_name}\nType: {step.type}\nVaqt: {datetime.now().strftime('%H:%M')}")])

            update.message.reply_text("Xabar adminga yuborildi",
                                      reply_markup=end_button)
        elif step.step == 5 and msg == 'Yuborish!':
            Workers.objects.filter(telegram_id=user_id).update(step=0)

            context.bot.send_media_group(chat_id='990254417', media=[InputMediaPhoto(f'{step.image}',
                                                                                     caption=f"Xodim: {step.full_name}\nType: {step.type}\nVaqt: {datetime.now().strftime('%H:%M')}")])

            update.message.reply_text("Xabar adminga yuborildi",
                                      reply_markup=start_button)

        elif msg == 'Ish haqqi haqidagi malumot':

            update.message.reply_text('Siz qaysi turdagi ish haqini kurmoqchisiz!', reply_markup=salary_button)

        elif msg == 'Ish haqi' and step.step == 0:
            salary = Workers.objects.get(telegram_id=user_id).salary
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {salary} so\'m', reply_markup=start_button)
        elif msg == 'Ish haqi' and step.step != 0:
            salary = Workers.objects.get(telegram_id=user_id).salary
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {salary} so\'m', reply_markup=end_button)
        elif msg == 'Bonus+' and step.step == 0:
            bons = Workers.objects.get(telegram_id=user_id).bons
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {bons} so\'m', reply_markup=start_button)
        elif msg == 'Bonus+' and step.step != 0:
            bons = Workers.objects.get(telegram_id=user_id).bons
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {bons} so\'m', reply_markup=end_button)
        elif msg == 'Jarima' and step.step == 0:
            fine = Workers.objects.get(telegram_id=user_id).fine
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {fine} so\'m', reply_markup=start_button)
        elif msg == 'Jarima' and step.step != 0:
            fine = Workers.objects.get(telegram_id=user_id).fine
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {fine} so\'m', reply_markup=end_button)
        elif msg == 'Avans' and step.step == 0:
            give = Workers.objects.get(telegram_id=user_id).give
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {give} so\'m', reply_markup=start_button)
        elif msg == 'Avans' and step.step != 0:
            give = Workers.objects.get(telegram_id=user_id).give
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {give} so\'m', reply_markup=end_button)
        elif msg == 'Qoldiq' and step.step == 0:
            give = Workers.objects.get(telegram_id=user_id).residue
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {give} so\'m', reply_markup=start_button)
        elif msg == 'Qoldiq' and step.step != 0:
            give = Workers.objects.get(telegram_id=user_id).residue
            name = Workers.objects.get(telegram_id=user_id).full_name
            update.message.reply_text(f'{name}ning ish haqingiz {give} so\'m', reply_markup=end_button)


def inline(update: Update, context: CallbackContext):
    data = update.callback_query.data
    user_id = update.callback_query.from_user.id
    if data == 'send':

        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text="",
                                 reply_markup=start_button)
    elif data == "back":
        update.callback_query.message.delete()
        Workers.objects.filter(telegram_id=user_id).update(step=0)
        context.bot.delete_message(chat_id=update.callback_query.from_user.id,
                                   message_id=update.callback_query.message.message_id - 1)
