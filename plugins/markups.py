import os
import shutil
from typing import List

from disk import Path
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply
from pyrogram.errors import MessageNotModified, ReplyMarkupInvalid
from functions.functions import get_server_details

path = Path(os.getcwd())
files_num = path.get_num_files()

start_and_help = InlineKeyboardMarkup([[InlineKeyboardButton(text='Creator ð¦¾', url='https://t.me/MosheNew')],
                                       [
                                           InlineKeyboardButton(text='Source Code ð',
                                                                url='https://github.com/moshe-coh/Terminal-Bot')
                                       ]])

refresh_space = InlineKeyboardMarkup([[InlineKeyboardButton(text='Refresh ð«', callback_data='space')]])


base_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('ð Show Files', callback_data='ShowFiles'),
        InlineKeyboardButton('ð Show Folders', callback_data='ShowFolders')

    ],
    [
        InlineKeyboardButton('â Close', callback_data='close')
    ]
])


def folder_markup():
    directorys = path.directories
    keyboard: List[List[InlineKeyboardButton]] = []

    for folder in directorys:
        keyboard.append(
            [InlineKeyboardButton(f"ð {folder.name}", callback_data=f"folder={str(folder.name)}")]
        )
    keyboard.append([
        InlineKeyboardButton("â©ï¸Back To Menu", callback_data="BackToMenu")
    ])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def files_markup():
    files = path.files
    keyboard: List[List[InlineKeyboardButton]] = []

    for file in files:
        keyboard.append(
            [InlineKeyboardButton(f"{'ð'} {file.full_name}", callback_data=f"file={str(file.full_name)}")]
        )
    keyboard.append([
        InlineKeyboardButton("â©ï¸Back To Menu", callback_data="BackToMenu")
    ])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def file_markup(file):
    keyboard = [[InlineKeyboardButton("â Delete", callback_data=f"delete={file}")],
                [InlineKeyboardButton("ð Download File", callback_data=f"download={file}")],
                [InlineKeyboardButton("âï¸Rename", callback_data=f"rename={file}")],
                [InlineKeyboardButton("â©ï¸Back To Menu", callback_data="BackToMenu")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def folders_markup(folder):
    keyboard = [[InlineKeyboardButton("â Delete", callback_data=f"fdelete={folder}")],
                [InlineKeyboardButton("âï¸Rename", callback_data=f"rename={folder}")],
                [InlineKeyboardButton("â©ï¸Back To Menu", callback_data="BackToMenu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


@Client.on_callback_query()
async def callback(_, cb: CallbackQuery):
    data = cb.data
    if data == "ShowFolders":
        try:
            await cb.message.edit_text(
                f"**The Current Path:** `{path.absolute_path}`\n**Total Files And Folders is:** {files_num}"
                f"\nð Here is your folders:", reply_markup=folder_markup())
        except ReplyMarkupInvalid:
            await cb.answer("you have no folders here, yet.", show_alert=True)
    elif data == "ShowFiles":
        try:
            await cb.message.edit_text(
                f"**The Current Path:** `{path.absolute_path}`\n**Total Files And Folders is:** {files_num}"
                f"\nð Here is your Files:", reply_markup=files_markup())
        except ReplyMarkupInvalid:
            await cb.answer("you have no files here, yet.", show_alert=True)
    elif data == "BackToMenu":
        await cb.message.edit_text('what you want to show?', reply_markup=base_markup)
    elif data == "close":
        await cb.message.delete()
    elif data.startswith('file'):
        none, file_name = data.split("=")
        await cb.message.edit_text(f"**File:** `{file_name}`\n**Path:** `{path.absolute_path}`",
                                   reply_markup=file_markup(file_name))
    elif data.startswith("folder"):
        none, folder_name = data.split("=")
        await cb.message.edit_text(f"**The Current Path:** `{path.absolute_path}`\n"
                                   f"**Total Files And Folders is:** {files_num}",
                                   reply_markup=folders_markup(folder_name))
    elif data.startswith('delete'):
        none, name = data.split("=")
        try:
            os.remove(name)
            await cb.message.edit_text(f"File {name} Deleted!", reply_markup=files_markup())
        except Exception as e:
            await cb.message.edit_text(f"Can't To delete this file...\n\n{str(e)}")
    elif data.startswith('rename'):
        none, name = cb.data.split("=")
        try:
            new_name = await _.ask(cb.message.chat.id, 'Send me the new name:', filters=filters.reply,
                                   reply_markup=ForceReply(), timeout=300)
            os.rename(name, new_name.text)
            await cb.message.edit_text(f"Renamed successfully", reply_markup=files_markup())
        except TimeoutError:
            pass
        except Exception as e:
            await cb.message.edit_text(f"Can't rename this file...\n\n{str(e)}")

    elif data.startswith("download"):
        none, name = cb.data.split("=")
        try:
            await cb.answer("File will download soon. please wait...")
            await cb.message.reply_document(name)
        except Exception as e:
            await cb.message.edit_text(f"Can't download this file...\n\n{str(e)}")
    elif data.startswith('fdelete'):
        none, folder_name = data.split("=")
        shutil.rmtree(folder_name)
        await cb.message.edit_text(f"folder {folder_name} successfully deleted", reply_markup=base_markup)
    elif data == "space":
        await cb.message.edit_text('Checking Again... â³')

        try:
            await cb.message.edit_text(get_server_details(), reply_markup=refresh_space)
        except MessageNotModified:
            pass
