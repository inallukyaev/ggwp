import logging, ephem
from glob import glob
from random import choice
import settings

from emoji import emojize
from telegram import ReplyKeyboardMarkup,KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler , RegexHandler , Filters




logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                    level = logging.INFO,
                    filename="li.log"
                    )


def greet_user(bot, update, user_data):
    smile = get_user_smile(user_data)
    user_data["smile"] = smile 
    text = "Привет {}".format(smile)
    contact_button = KeyboardButton("Прислать Контакты", request_contact=True)
    location_button = KeyboardButton("Прислать Кординаты ", request_location=True)
    my_keyboard = ReplyKeyboardMarkup([["Прислать кота", "Сменить аватарку","Прислать собаку"],
                                        [contact_button , location_button]
                                        ]
                                        )
    update.message.reply_text(text,reply_markup=  get_keyboard())

def talk_to_me(bot,update,user_data):
    smile = get_user_smile(user_data)
    user_text = "Привет, {} {}! Ты написал:  {}".format(update.message.chat.first_name,user_data["smile"] , 
                    update.message.text) 
    logging.info("Firstname: %s, User:  %s , Chat id: %s , Message: %s ",update.message.chat.first_name,    update.message.chat.last_name , 
                                update.message.chat.id , update.message.text ,) 
    update.message.reply_text(user_text , reply_markup= get_keyboard())

def send_cat_picture(bot, update,user_data):
    cat_list = glob ("images/cat*jp*g")
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id = update.message.chat_id, photo=open(cat_pic,"rb"),reply_markup= get_keyboard())
    

def send_dog_picture(bot,update,user_data):
    dog_list = glob ("dogs/dog*jp*g")
    dog_pic = choice(dog_list)
    bot.send_photo(chat_id = update.message.chat_id, photo = open(dog_pic,"rb"),reply_markup= get_keyboard())


        

def get_contact(bot,update, user_data):
    print(update.message.contact)
    update.message.reply_text("Готово:{}".format(get_user_smile(user_data),reply_markup= get_keyboard()))
 

def get_location(bot,update, user_data):
    print(update.message.location)
    update.message.reply_text("Готово:{}".format(get_user_smile(user_data),reply_markup= get_keyboard()))
   


def get_user_smile(user_data):
    if "smile" in user_data:
        return user_data["smile"]
    else :
        user_data["smile"] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data["smile"]
   
def change_avatar (bot,update,user_data):
    if "smile" in user_data:
        del user_data["smile"]
    smile = get_user_smile(user_data)
    update.message.reply_text("Готово:{}".format(smile),reply_markup=get_keyboard())


def get_keyboard():
    contact_button = KeyboardButton("Прислать Контакты", request_contact=True)
    location_button = KeyboardButton("Прислать Кординаты ", request_location=True)
    my_keyboard = ReplyKeyboardMarkup([["Прислать кота", "Сменить аватарку","Прислать собаку"],
                                        [contact_button , location_button]
                                        ],resize_keyboard= True
                                        )
    return my_keyboard

   
 
         
def main():
    mybot = Updater(settings.API_KEY,request_kwargs=settings.PROXY)

    logging.info("Бот запускается")
    

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("dog", send_dog_picture, pass_user_data=True))
    
    dp.add_handler(RegexHandler("^(Прислать кота)$", send_cat_picture ,  pass_user_data=True))
    dp.add_handler(RegexHandler("^(Сменить аватарку)$", change_avatar ,  pass_user_data=True))
    dp.add_handler(RegexHandler("^(Прислать собаку)$", send_dog_picture ,  pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text,talk_to_me, pass_user_data= True))
    dp.add_handler(MessageHandler(Filters.contact , get_contact , pass_user_data= True))
    dp.add_handler(MessageHandler(Filters.location , get_location , pass_user_data= True))
    
    
    mybot.start_polling()
    mybot.idle()


main()
