from Tools import *

"""
The meaning of DTC is Descriptions Technical Code
The meaning of ITC is Important Technical Codes
The meaning of OPP is Group Offer Price Percent
The meaning of STC is Similar Technical Codes
The meaning of IU is Important User
The meaning of GI is Group Id
"""

"""
The meaning of RTC is Request Technical Code
The meaning of TCI is Technical Code Information
The meaning of IRR is Invoicing reject reason
The meaning of IA is Invoicing Accepted
The meaning of IR is Invoice Rejected
The meaning of P_ is Pricing
The meaning of P is Price
The meaning of I_ is Invoicing
The meaning of I is Invoice
"""


# Filters
ACTIVE_VALIDATION = True
active_validation = filters.create(lambda _, __, active: ACTIVE_VALIDATION == True)


# Handlers
@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.command("on"))
async def BNLLXGZJEM(client: Client, message: Message):
    global ACTIVE_VALIDATION
    ACTIVE_VALIDATION = True
    await message.reply_text(ON, True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.command("off"))
async def RKWHFSQOCN(client: Client, message: Message):
    global ACTIVE_VALIDATION
    ACTIVE_VALIDATION = False
    await message.reply_text(OFF, True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.command("status"))
async def ZUPBZQECXR(client: Client, message: Message):
    await message.reply_text(active_status(ACTIVE_VALIDATION), True)


@client_app.on_message(filters.text & filters.chat(GROUP_ID) & active_validation)
async def DVOSNGDELR(client: Client, message: Message):
    message_count_object = MessageDateCount()
    await message_count_object.add()
    text = text_cleaner(message.text)
    technical_codes = await Similar.get(text)
    if technical_codes:
        importants = await Important.get(technical_codes)
        await return_to_requester(technical_codes, message, MAIN_ADMIN_ID)
        await return_to_requester(importants, message, IMPORTANT_REQUESTS_ADMIN_ID)


@api_app.on_message(filters.private & filters.text & filters.command("start") & active_validation)
async def QZEAGAURCF(client: Client, message: Message):
    user_id = message.from_user.id
    user_object = User(user_id)
    await user_object.add()
    await message.reply_text(HELP, True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.command("all_itc") & active_validation)
async def VMHKZMSZKA(client: Client, message: Message):
    importants = await Important.all(True)
    if importants == "EMPTY":
        await message.reply_text(empty("کد فنی", "مهمی"), True)
    else:
        await message.reply_text(importants, True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.command("all_stc") & active_validation)
async def TGSUXDPLPJ(client: Client, message: Message):
    similars = await Similar.all(True)
    if similars == "EMPTY":
        await message.reply_text(empty("کد فنی", "مشابهی"), True)
    else:
        try:
            await message.reply_text(similars, True)
        except MessageTooLong:
            similars = await Similar.all()
            DataFrame.from_dict({"شناسه گروه": list(similars.keys()), "کد فنی ها": list(similars.values())}).to_excel(EXCEL_FILE, index=False)
            await message.reply_document(EXCEL_FILE, True)
            os.remove(EXCEL_FILE)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.command("all_gi") & active_validation)
async def XHCQSTLOOR(client: Client, message: Message):
    group_ids = await SimilarGroup.all(True)
    if group_ids == "EMPTY":
        await message.reply_text(empty("شناسه گروه", "مشابهی"), True)
    else:
        await message.reply_text(group_ids, True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.command("all_iu") & active_validation)
async def FZNSNLHGVE(client: Client, message: Message):
    important_users = await ImportantUser.all()
    if important_users == "EMPTY":
        await message.reply_text(empty("کاربر", "مهمی"), True)
    else:
        text = IMPORTANT_USERS
        for item in important_users:
            user = await client.get_users(item)
            full_name = f"{user.first_name}{'' if user.last_name is None else f' {user.last_name}'}"
            text += f"\n{item}: {full_name}"
        text += NEW_LINE * 2 + emoji.CHECK_MARK_BUTTON
        await message.reply_text(text, True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.command("all_dtc") & active_validation)
async def PXFRLSKCCL(client: Client, message: Message):
    descriptions = await Description.all(True)
    if descriptions == "EMPTY":
        await message.reply_text(empty("کد فنی", "توضیح داده شده ای"), True)
    else:
        await message.reply_text(descriptions, True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/message") & active_validation)
async def MGTWNTREGP(client: Client, message: Message):
    users = await User.all()
    text = message.text.strip("/message ")
    if text:
        if len(users) != 0:
            for user_id in users:
                await api_app.send_message(user_id, ADMIN_MESSAGE + text, True)
            await message.reply_text(sended_message(len(users)), True)
        else:
            await message.reply_text(NOT_EXIST_USER, True)
    else:
        await message.reply_text(INVALID_MESSAGE, True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/add_iu") & active_validation)
async def ILHVFZEDJS(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        user_id = arguments[0]
        if user_id.isdigit():
            user_id = int(user_id)
            if user_id in ADMIN_IDS:
                await message.reply_text(CANT_ADMIN, True)
            else:
                try:
                    await client.get_users(user_id)
                    important_user_object = ImportantUser(user_id)
                    add_validation = await important_user_object.add()
                    match add_validation:
                        case "EXISTANCE":
                            await message.reply_text(existation(True, "کاربر", "مهم"), True)
                        case "SUCCESS":
                            await message.reply_text(updated("اضافه", "کاربر", "مهم"), True)
                except:
                    await message.reply_text(INVALID_USER, True)
        else:
            await message.reply_text(INVALID_USER, True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/del_iu") & active_validation)
async def TJPHRIYQPF(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        user_id = arguments[0]
        if user_id.isdigit():
            user_id = int(user_id)
            important_user_object = ImportantUser(user_id)
            delete_validation = await important_user_object.delete()
            match delete_validation:
                case "EMPTY":
                    await message.reply_text(empty("کاربر", "مهمی"), True)
                case "NOT_EXISTANCE":
                    await message.reply_text(existation(False, "کاربر", "مهم"), True)
                case "SUCCESS":
                    await message.reply_text(updated("حذف", "کاربر", "مهم"), True)
        else:
            await message.reply_text(INVALID_USER, True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/add_dtc") & active_validation)
async def LERMEIKSHD(client: Client, message: Message):
    technical_code, description = message.text.strip("/add_dtc ").split(" ", 1)
    description_object = Description(technical_code)
    add_validation = await description_object.add(description)
    match add_validation:
        case "EXISTANCE":
            await message.reply_text(existation(True, "کد فنی", "توضیح داده شده"), True)
        case "SUCCESS":
            await message.reply_text(updated("اضافه", "کد فنی", "توضیح داده شده"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/update_dtc") & active_validation)
async def ZZRBMSIFKT(client: Client, message: Message):
    arguments = message.text.strip("/update_dtc ").split(" ", 1)
    if len(arguments) < 2:
        await message.reply_text(arguments_required(True, "دو"), True)
    else:
        technical_code, description = arguments
        description_object = Description(technical_code)
        update_validation = await description_object.update(description)
        match update_validation:
            case "EMPTY":
                await message.reply_text(empty("کد فنی", "توضیح داده شده ای"), True)
            case "NOT_EXISTANCE":
                await message.reply_text(existation(False, "کد فنی", "توضیح داده شده"), True)
            case "SUCCESS":
                await message.reply_text(updated("آپدیت", "کد فنی", "توضیح داده شده"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/del_dtc") & active_validation)
async def JUNVUZJSUH(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        technical_code = arguments[0]
        description_object = Description(technical_code)
        delete_validation = await description_object.delete()
        match delete_validation:
            case "EMPTY":
                await message.reply_text(empty("کد فنی", "توضیح داده شده ای"), True)
            case "NOT_EXISTANCE":
                await message.reply_text(existation(False, "کد فنی", "توضیح داده شده"), True)
            case "SUCCESS":
                await message.reply_text(updated("حذف", "کد فنی", "توضیح داده شده"), True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/add_itc") & active_validation)
async def BMXOHMELHD(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        technical_code = arguments[0]
        important_object = Important(technical_code)
        add_validation = await important_object.add()
        match add_validation:
            case "EXISTANCE":
                await message.reply_text(existation(True, "کد فنی", "مهم"), True)
            case "SUCCESS":
                await message.reply_text(updated("اضافه", "کد فنی", "مهم"), True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/del_itc") & active_validation)
async def HRSTVQYIQH(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        technical_code = arguments[0]
        important_object = Important(technical_code)
        delete_validation = await important_object.delete()
        match delete_validation:
            case "EMPTY":
                await message.reply_text(empty("کد فنی", "مهمی"), True)
            case "NOT_EXISTANCE":
                await message.reply_text(existation(False, "کد فنی", "مهم"), True)
            case "SUCCESS":
                await message.reply_text(updated("حذف", "کد فنی", "مهم"), True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/add_stc") & active_validation)
async def ZOHIWUAYNW(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 2:
        technical_code, technical_code_one = arguments
        group_object = SimilarGroup(None)
        add_validation = await group_object.add(technical_code, technical_code_one)
        match add_validation:
            case "EXISTANCE":
                await message.reply_text(existation(True, "کد فنی", "مشابه"), True)
            case "SUCCESS":
                await message.reply_text(updated("اضافه", "کد فنی", "مشابه"), True)
    elif len(arguments) > 2:
        await message.reply_text(arguments_required(False, "دو"), True)
    elif len(arguments) < 2:
        await message.reply_text(arguments_required(True, "دو"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/del_stc") & active_validation)
async def OECYKIBKIP(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        technical_code = arguments[0]
        similar_object = Similar(technical_code)
        delete_validation = await similar_object.delete()
        match delete_validation:
            case "EMPTY":
                await message.reply_text(empty("کد فنی", "مشابهی"), True)
            case "NOT_EXISTANCE":
                await message.reply_text(existation(False, "کد فنی", "مشابه"), True)
            case "SUCCESS":
                await message.reply_text(updated("حذف", "کد فنی", "مشابه"), True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/del_gi") & active_validation)
async def XHXQJSGZFU(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        group_id = arguments[0]
        if group_id.isdigit():
            group_id = int(group_id)
            group_object = SimilarGroup(group_id)
            delete_validation = await group_object.delete()
            match delete_validation:
                case "EMPTY":
                    await message.reply_text(empty("شناسه گروه", "تعریف شده ای"), True)
                case "NOT_EXISTANCE":
                    await message.reply_text(existation(False, "شناسه گروه", "تعریف شده"), True)
                case "SUCCESS":
                    await message.reply_text(updated("حذف", "شناهه گروه", "تعریف شده"), True)
        else:
            await message.reply_text(INVALID_COMMAND, True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/popular_tc") & active_validation)
async def HAEFJITCEC(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    popular_technical_codes = await populars(None, True)
    match popular_technical_codes:
        case "EMPTY_FILE":
            await message.reply_text(POPULAR_FILE_EMPTY, True)
        case "NOT_EXISTANCE_FILE":
            await message.reply_text(POPULAR_NOT_EXIST_FILE, True)
        case _:
            match len(arguments):
                case 0:
                    try:
                        await message.reply_text(popular_technical_codes, True)
                    except MessageTooLong:
                        popular_technical_codes = await populars(None, False)
                        DataFrame({"کد فنی معروف": list(popular_technical_codes.keys()), "تعداد": list(popular_technical_codes.values())}).to_excel(EXCEL_FILE, index=False)
                        await message.reply_document(EXCEL_FILE, True)
                        os.remove(EXCEL_FILE)
                case 1:
                    technical_code = arguments[0]
                    popular_technical_codes = await populars(technical_code, True)
                    try:
                        await message.reply_text(popular_technical_codes, True)
                    except MessageTooLong:
                        popular_technical_codes = await populars(technical_code, False)
                        DataFrame({"کد فنی معروف": list(popular_technical_codes.keys()), "تعداد": list(popular_technical_codes.values())}).to_excel(EXCEL_FILE, index=False)
                        await message.reply_document(EXCEL_FILE, True)
                        os.remove(EXCEL_FILE)
                case _:
                    await message.reply_text(INVALID_COMMAND, True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/search_dtc") & active_validation)
async def ICOEKPJMWY(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        technical_code = arguments[0]
        description_object = Description(technical_code)
        search_validation = await description_object.search(True)
        match search_validation:
            case "EMPTY":
                await message.reply_text(empty("کد فنی", "توضیح داده شده ای"), True)
            case "NOT_EXISTANCE":
                await message.reply_text(existation(False, "کد فنی", "توضیح داده شده"), True)
            case _:
                await message.reply_text(search_validation, True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/mdc") & active_validation)
async def QZWGWCXHKV(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        date = arguments[0]
        message_count_object = MessageDateCount()
        get_validation = await message_count_object.get(date, True)
        match get_validation:
            case "EMPTY":
                await message.reply_text(empty("تعداد پیام", "ذخیره شده ای"), True)
            case "NOT_EXISTANCE":
                await message.reply_text(existation(False, "تاریخ", "تعداد پیام"), True)
            case _:
                await message.reply_text(get_validation, True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/search_stc") & active_validation)
async def AOHYDPTYZY(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        technical_code = arguments[0]
        similar_object = Similar(technical_code)
        search_validation = await similar_object.search(True)
        match search_validation:
            case "EMPTY":
                await message.reply_text(empty("کد فنی", "مشابهی"), True)
            case "NOT_EXISTANCE":
                await message.reply_text(existation(False, "کد فنی", "مشابه"), True)
            case _:
                await message.reply_text(search_validation, True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/search_gi") & active_validation)
async def SXYHLUQKAK(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        group_id = arguments[0]
        if group_id.isdigit():
            group_id = int(group_id)
            group_object = SimilarGroup(group_id)
            search_validation = await group_object.search(True)
            match search_validation:
                case "EMPTY":
                    await message.reply_text(empty("شناسه گروه", "تعریف شده ای"), True)
                case "NOT_EXISTANCE":
                    await message.reply_text(existation(False, "شناسه گروه", "تعریف شده"), True)
                case _:
                    await message.reply_text(search_validation, True)
        else:
            await message.reply_text(INVALID_COMMAND, True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.regex("^/update_opp") & active_validation)
async def IWJMQPYHBI(client: Client, message: Message):
    arguments = [argument for argument in message.text.split()[1:]]
    if len(arguments) == 1:
        percent = arguments[0]
        try:
            percent = int(percent)
            update_validation = await OfferPriceModification.update(percent)
            match update_validation:
                case "SUCCESS":
                    await message.reply_text(UPDATED_OFFER_PRICE_PERCENT_MODIFICATION, True)
        except ValueError:
            await message.reply_text(INVALID_COMMAND, True)
    elif len(arguments) > 1:
        await message.reply_text(arguments_required(False, "یک"), True)
    elif len(arguments) < 1:
        await message.reply_text(arguments_required(True, "یک"), True)


@api_app.on_message(filters.private & filters.text & filters.user(ADMIN_IDS) & filters.command("get_opp") & active_validation)
async def XZEKTNPDAX(client: Client, message: Message):
    percent = await OfferPriceModification.get()
    await message.reply_text(offer_price_percnet(percent), True)


@api_app.on_message(filters.private & filters.text & active_validation)
async def GOXBOCAJCP(client: Client, message: Message):
    text = text_cleaner(message.text)
    user_id = message.from_user.id
    user_object = User(user_id)
    await user_object.add()
    important_users = await ImportantUser.all()
    if important_users == "EMPTY":
        important_users = []
    full_name = get_full_name(message)
    try:
        button_index = None
        if user_id in ADMIN_IDS:
            callback_data = message.reply_to_message.reply_markup.inline_keyboard[0][0].callback_data
        else:
            reply_markup = message.reply_to_message.reply_markup
            callback_data = None
            for row_buttons in reply_markup.inline_keyboard:
                intended_button_callback_data = row_buttons[3].callback_data
                if intended_button_callback_data.startswith("I_@"):
                    button_index = reply_markup.inline_keyboard.index(row_buttons)
                    callback_data = intended_button_callback_data
                    break
        proccess_type = callback_data.split("@")[0]
        data = callback_data.split("@")[1].split("_") if len(callback_data.split("@")) == 2 else None
        match proccess_type:
            case "P_":
                user_id, message_id, technical_code, brand = data
                if text.isdigit():
                    price = modify_number(int(text) * 10000)
                    message_id = int(message_id)
                    user_id = int(user_id)
                    intended_message = await client.get_messages(user_id, message_id)
                    reply_markup = intended_message.reply_markup
                    for row_buttons in reply_markup.inline_keyboard:
                        intended_button_callback_data = row_buttons[1].callback_data
                        if technical_code in intended_button_callback_data and brand in intended_button_callback_data:
                            button_index = reply_markup.inline_keyboard.index(row_buttons)
                            reply_markup.inline_keyboard[button_index][3].callback_data = f"I@{technical_code}_{brand}_{int(text) * 10000}"
                            reply_markup.inline_keyboard[button_index][2].text = price
                            await intended_message.edit_reply_markup(reply_markup)
                            break
                    text = message.reply_to_message.text
                    reply_markup = message.reply_to_message.reply_markup
                    reply_markup.inline_keyboard[0][0].callback_data = "None"
                    await message.reply_to_message.edit(text.replace("در انتظار قیمت دهی", "قیمت دهی شده"), reply_markup=reply_markup)
            case "I_":
                technical_code, brand, price = data
                if text.isdigit():
                    count = int(text)
                    callback_data = [
                        f"{user_id}_{message.reply_to_message_id}_{technical_code}_{brand}_{count}",
                        f"TCI@{technical_code}_{brand}_{count}",
                    ]
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(full_name, "None")],
                            TECHNICAL_CODE_INFORMATOIN_HEADER,
                            [
                                InlineKeyboardButton(technical_code, callback_data[1]),
                                InlineKeyboardButton(brand, callback_data[1]),
                            ],
                            [
                                InlineKeyboardButton(
                                    "لغو",
                                    f"IRR@{callback_data[0]}",
                                ),
                                InlineKeyboardButton(
                                    "تایید",
                                    f"IA@{callback_data[0]}",
                                ),
                            ],
                        ]
                    )
                    await client.send_message(MAIN_ADMIN_ID, important_requested(user_id, "فاکتور", count), reply_markup=reply_markup)
                    reply_markup = message.reply_to_message.reply_markup
                    reply_markup.inline_keyboard[button_index][3].callback_data = "None"
                    reply_markup.inline_keyboard[button_index][3].text = "در انتظار"
                    await message.reply_to_message.edit_reply_markup(reply_markup)
            case "IR":
                intended_user_id, intended_message_id, technical_code, brand, count = data
                intended_message_id = int(intended_message_id)
                intended_user_id = int(intended_user_id)
                intended_message = await client.get_messages(intended_user_id, intended_message_id)
                intended_message_chat_id = intended_message.chat.id
                intended_message_reply_markup: InlineKeyboardMarkup = intended_message.reply_markup
                for row_buttons in intended_message_reply_markup.inline_keyboard:
                    intended_button_callback_data = row_buttons[1].callback_data
                    if technical_code in intended_button_callback_data and brand in intended_button_callback_data:
                        button_index = intended_message_reply_markup.inline_keyboard.index(row_buttons)
                        intended_message_reply_markup.inline_keyboard[button_index][3].text = emoji.CROSS_MARK
                        await intended_message.edit_reply_markup(intended_message_reply_markup)
                        text = reject_invoice(technical_code, brand, count, message.text)
                        await client.send_message(intended_message_chat_id, text, reply_to_message_id=intended_message_id)
                        break
                    text = message.reply_to_message.text
                    reply_markup = message.reply_to_message.reply_markup
                    await message.reply_to_message.edit(text.replace("در انتظار رسیدگی", "لغو شده"), reply_markup=reply_markup)
    except:
        text = text_cleaner(message.text)
        technical_codes = await Similar.get(text)
        if technical_codes:
            await founded_technical_code(technical_codes, message)
        else:
            await message.reply_text(existation(False, "کد فنی", "انبار"), True)
    if user_id not in ADMIN_IDS:
        user_type = "ویژه" if user_id in important_users else "معمولی"
        await client.send_message(CHANNEL_ID, user_messaged(message, user_type))


@api_app.on_callback_query(active_validation)
async def CVHIHIAJLA(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    callback_data = callback.data
    message = callback.message
    callback_id = callback.id
    message_id = message.id
    full_name = get_full_name(callback)
    proccess_type = callback_data.split("@")[0]
    data = callback_data.split("@")[1].split("_") if len(callback_data.split("@")) == 2 else None
    important_users = await ImportantUser.all()
    if important_users == "EMPTY":
        important_users = []
    if proccess_type == "None" or proccess_type == "P_":
        await client.answer_callback_query(callback_id, JUST_VIEW)
    elif proccess_type == "TCI":
        technical_code, brand, count = data
        description_object = Description(technical_code)
        description = await description_object.search()
        alert_text = ("" if user_id in ADMIN_IDS else "empty description") if description == "EMPTY" or description == "NOT_EXISTANCE" else f"description: {description}"
        if user_id in ADMIN_IDS:
            alert_text += f"\ncount: {count}"
        await client.answer_callback_query(callback_id, alert_text, True)
    elif proccess_type == "RTC":
        user_id, technical_code, brand, count, price = data
        user_id = int(user_id)
        description_object = Description(technical_code)
        description = await description_object.search()
        if description == "EMPTY" or description == "NOT_EXISTANCE":
            description = False
        if price == "0":
            await client_app.send_message(user_id, f"{technical_code} | {brand}{f'{NEW_LINE*2}توضیحات: {description}{NEW_LINE*2}{emoji.MEMO}' if description else ''}")
        else:
            await client_app.send_message(user_id, f"{technical_code} | {brand} | {modify_number(price)}{f'{NEW_LINE*2}توضیحات: {description}{NEW_LINE*2}{emoji.MEMO}' if description else ''}")
        reply_markup = message.reply_markup
        for row_buttons in reply_markup.inline_keyboard:
            for button in row_buttons:
                if button.callback_data == f"TCI@{technical_code}_{brand}_{count}":
                    reply_markup.inline_keyboard.remove(row_buttons)
                    break
        if len(reply_markup.inline_keyboard) == 2:
            reply_markup.inline_keyboard = [reply_markup.inline_keyboard[0]]
            await message.edit(f"{REQUEST_HANDLED}.\n\n{emoji.CHECK_MARK_BUTTON}", reply_markup=reply_markup)
        else:
            await message.edit_reply_markup(reply_markup)
        await client.answer_callback_query(callback_id, REQUEST_HANDLED)
    elif proccess_type == "P":
        technical_code, brand, count, price = data
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(full_name, f"P_@{user_id}_{message_id}_{technical_code}_{brand}")],
                TECHNICAL_CODE_INFORMATOIN_HEADER,
                [
                    InlineKeyboardButton(technical_code, f"TCI@{technical_code}_{brand}_{count}"),
                    InlineKeyboardButton(brand, f"TCI@{technical_code}_{brand}_{count}"),
                ],
            ]
        )
        await client.send_message(MAIN_ADMIN_ID, important_requested(user_id, "قیمت", False), reply_markup=reply_markup)
        reply_markup = message.reply_markup
        for row_buttons in reply_markup.inline_keyboard:
            intended_button_callback_data = row_buttons[1].callback_data
            if technical_code in intended_button_callback_data and brand in intended_button_callback_data:
                button_index = reply_markup.inline_keyboard.index(row_buttons)
                reply_markup.inline_keyboard[button_index][2].text = "در انتظار"
                reply_markup.inline_keyboard[button_index][2].callback_data = "None"
                await message.edit_reply_markup(reply_markup)
                break
        await client.answer_callback_query(callback_id, REQUEST_SENDED)
    elif proccess_type == "I":
        technical_code, brand, price = data
        reply_markup = message.reply_markup
        request_validation = True
        for row_buttons in reply_markup.inline_keyboard:
            intended_button_callback_data = row_buttons[3].callback_data
            if intended_button_callback_data.startswith("I_@"):
                request_validation = False
                break
        if request_validation:
            if price == "0":
                await client.answer_callback_query(callback_id, NOTHING_PRICE_TECHNICAL_CODE)
            else:
                for row_buttons in reply_markup.inline_keyboard:
                    intended_button_callback_data = row_buttons[1].callback_data
                    if technical_code in intended_button_callback_data and brand in intended_button_callback_data:
                        button_index = reply_markup.inline_keyboard.index(row_buttons)
                        reply_markup.inline_keyboard[button_index][3].callback_data = reply_markup.inline_keyboard[button_index][3].callback_data.replace("I", "I_")
                        reply_markup.inline_keyboard[button_index][3].text = "در حال پردازش"
                        await message.edit_reply_markup(reply_markup)
                        await client.answer_callback_query(callback_id, ENTER_TECHNICAL_CODE_COUNT, True)
                        break
        else:
            await client.answer_callback_query(callback_id, COMPLETE_PREVIOUS_INVOICING_REQUEST)
    elif proccess_type == "I_":
        reply_markup = message.reply_markup
        for row_buttons in reply_markup.inline_keyboard:
            intended_button_callback_data = row_buttons[3].callback_data
            if intended_button_callback_data.startswith("I_@"):
                button_index = reply_markup.inline_keyboard.index(row_buttons)
                reply_markup.inline_keyboard[button_index][3].callback_data = intended_button_callback_data.replace("I_", "I")
                reply_markup.inline_keyboard[button_index][3].text = "درخواست فاکتور"
                await message.edit_reply_markup(reply_markup)
                await client.answer_callback_query(callback_id, CANCELED_TECHNICAL_CODE_REQUEST)
    elif proccess_type == "IA" or proccess_type == "IRR":
        intended_user_id, intended_message_id, technical_code, brand, count = data
        intended_message_id = int(intended_message_id)
        intended_user_id = int(intended_user_id)
        intended_message = await client.get_messages(intended_user_id, intended_message_id)
        intended_message_chat_id = intended_message.chat.id
        intended_message_reply_markup: InlineKeyboardMarkup = intended_message.reply_markup
        match proccess_type:
            case "IA":
                button = emoji.CHECK_MARK_BUTTON
                text = access_invoice(technical_code, brand, count)
            case "IRR":
                reply_markup = message.reply_markup
                reply_markup.inline_keyboard = reply_markup.inline_keyboard[:-1]
                reply_markup.inline_keyboard[0][0].callback_data = f"IR@{'_'.join(data)}"
                await message.edit_reply_markup(reply_markup)
                await client.answer_callback_query(callback_id, REJECTED_REASON, True)
        if proccess_type != "IRR":
            for row_buttons in intended_message_reply_markup.inline_keyboard:
                intended_button_callback_data = row_buttons[1].callback_data
                if technical_code in intended_button_callback_data and brand in intended_button_callback_data:
                    button_index = intended_message_reply_markup.inline_keyboard.index(row_buttons)
                    intended_message_reply_markup.inline_keyboard[button_index][3].text = button
                    await intended_message.edit_reply_markup(intended_message_reply_markup)
                    await client.send_message(intended_message_chat_id, text, reply_to_message_id=intended_message_id)
                    break
            text = message.text
            reply_markup = message.reply_markup
            reply_markup.inline_keyboard = reply_markup.inline_keyboard[:-1]
            await message.edit(text.replace("در انتظار رسیدگی", "تایید شده"), reply_markup=reply_markup)


# Start the bot
if __name__ == "__main__":
    if not ACTIVE_VALIDATION:
        print("Remember to start the bot in telegram!")
    asyncio.run(apps())
