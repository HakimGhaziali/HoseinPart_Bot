from Libraries import *

# Telegram information
BOT_TOKEN = "5800957597:AAF9esO34js7pIsSeObIhyVcYcKhl3pk5z0"
API_HASH = "beac4e1065b2f36778b0c0e7321b80ad"
API_ID = 3631552
MAIN_ADMIN_ID = 638486692
IMPORTANT_REQUESTS_ADMIN_ID = 1148327615
ADMIN_IDS = [MAIN_ADMIN_ID, IMPORTANT_REQUESTS_ADMIN_ID]
SELLER_LINK_USERNAME = "https://t.me/Hoseinparts"
CHANNEL_ID = -1002075623082
GROUP_ID = -1001403812583

# Files
MAXIMUM_POPULAR_NUMBER = 5
DATABASE_FILE = "Database.db"
POPULAR_FILE = "Popular.json"
EXCEL_FILE = "Result.xlsx"
NEW_LINE = "\n"

# Objects
api_app = Client("Api", API_ID, API_HASH, bot_token=BOT_TOKEN)
client_app = Client("Client", API_ID, API_HASH)


# Tools
def apps():
    compose(
        [
            api_app,
            client_app,
        ]
    )


json_data = {
    "menuID": 87,
    "pagelenth": 999999999,
    "order_column": 1,
    "order_dir": "desc",
    "startRecord": 0,
    "condition": "$App$",
}

loop = asyncio.get_event_loop()
cursor = loop.run_until_complete(aiosqlite.connect(DATABASE_FILE))


async def execute(query: str, parameters: tuple, selection: str) -> aiosqlite.Cursor:
    match selection:
        case "all":
            return await (await cursor.execute(query, parameters)).fetchall()
        case "one":
            return await (await cursor.execute(query, parameters)).fetchone()
        case _:
            await cursor.execute(query, parameters)
    await cursor.commit()


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute("CREATE TABLE offer_price_modification(percent INT NOT NULL);", None, None))
    loop.run_until_complete(execute("INSERT INTO offer_price_modification(percent) VALUES(?);", (0,), None))
except aiosqlite.OperationalError as exist_table:
    print(str(exist_table).capitalize())

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute("CREATE TABLE important_users(user_id INT NOT NULL);", None, None))
except aiosqlite.OperationalError as exist_table:
    print(str(exist_table).capitalize())

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute("CREATE TABLE descriptions(technical_code VARCHAR NOT NULL, description TEXT);", None, None))
except aiosqlite.OperationalError as exist_table:
    print(str(exist_table).capitalize())

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute("CREATE TABLE importants(technical_code VARCHAR NOT NULL);", None, None))
except aiosqlite.OperationalError as exist_table:
    print(str(exist_table).capitalize())

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute("CREATE TABLE messages(date DATE, count INT NOT NULL);", None, None))
except aiosqlite.OperationalError as exist_table:
    print(str(exist_table).capitalize())

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute("CREATE TABLE similars(technical_code VARCHAR NOT NULL, group_id INT NOT NULL);", None, None))
except aiosqlite.OperationalError as exist_table:
    print(str(exist_table).capitalize())

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute("CREATE TABLE users(user_id INT NOT NULL);", None, None))
except aiosqlite.OperationalError as exist_table:
    print(str(exist_table).capitalize())


# Messages
FOUNDED_TECHNICAL_CODE_FORWARD_FROM = f"کد فنی درخواستی کاربر با برند زیر در انبار موجود میباشد:\n\n{emoji.LEFT_ARROW_CURVING_RIGHT}"
UPDATED_OFFER_PRICE_PERCENT_MODIFICATION = f"درصد اصلاح قیمت پیشنهادی با موفقیت آپدیت شد.\n\n{emoji.CHECK_MARK_BUTTON}"
HELP = f"برای استفاده از ربات حسین پارت کافیه کد فنی های خودت رو بفرستی.\n\n{emoji.JAPANESE_SYMBOL_FOR_BEGINNER}"
NOT_EXIST_USER = f"پیام شما به دلیل وجود نداشتن کاربری که از ربات استفاده کنه ارسال نشد.\n\n{emoji.CROSS_MARK}"
FOUNDED_TECHNICAL_CODE = f"کد فنی مورد نظر شما با برند زیر در انبار موجود میباشد:\n\n{emoji.CHECK_MARK_BUTTON}"
INVALID_MESSAGE = f"برای استفاده از این دستور باید متن مورد نظر خود را وارد کنید.\n\n{emoji.CROSS_MARK}"
TECHNICAL_CODE_REQUESTED = f"کاربری درخواست کد فنی کرده که ما در انبار موجود داریم:\n\n{emoji.MEMO}"
CANT_ADMIN = f"شما نمیتوانید این عملیات را روی ادمین ها اعمال کنید.\n\n{emoji.CROSS_MARK}"
POPULAR_NOT_EXIST_FILE = f"فایل کد فنی های معروف وجود ندارد.\n\n{emoji.CROSS_MARK}"
POPULAR_FILE_EMPTY = f"فایل کد فنی های معروف خالی میباشد.\n\n{emoji.CROSS_MARK}"
INVALID_COMMAND = f"دستور وارد شده به درستی استفاده نشده.\n\n{emoji.CROSS_MARK}"
INVALID_USER = f"کاربر مورد نظر شما معتبر نمیباشد.\n\n{emoji.CROSS_MARK}"
FOUNDED_POPULAR = "کد فنی هایی در لیست کد فنی های معروف یافت شد:\n\n"
OFF = f"ربات با موفقیت خاموش شد.\n\n{emoji.CHECK_MARK_BUTTON}"
ON = f"ربات با موفقیت روشن شد.\n\n{emoji.CHECK_MARK_BUTTON}"
MESSAGE_DATE_COUNTS = "تعداد تمام پیام ها تاریخ ها:\n\n"
SIMILARS = "تمام شناسه گروه های کد فنی های مشابه:\n\n"
ADMIN_MESSAGE = "پیام از طرف حسین پارت:\n\n"
IMPORTANT_USERS = "تمام کاربر های مهم:\n"

# Special lambda functions
get_full_name = lambda message: f"{message.from_user.first_name}{'' if message.from_user.last_name is None else f' {message.from_user.last_name}'}"
modify_number = lambda price: "{:,.0f}".format(round(int(price) / 10000, -1))
search_length = lambda text: len(text) if 7 <= len(text) <= 10 else 10
text_cleaner = lambda text: re.sub(r"[^A-Za-z0-9]+", "", text.upper())

# Text lambda functions
important_requested = lambda user_id, proccess_type, count: f"کاربری با آیدی عددی {user_id} درخواست {proccess_type} کد فنی زیر را{f' به تعداد {count} عدد' if count else ''} کرده است.\n\nوضعیت: {'در انتظار قیمت دهی' if proccess_type == 'قیمت' else 'در انتظار رسیدگی'}\n\n{emoji.MEMO}"
user_messaged = lambda message, user_type: f"کاربری {user_type} با آیدی عددی {message.from_user.id} به نام {get_full_name(message)} پیام زیر را برای ربات ارسال کرد:\n\n{message.text}\n\n{emoji.MAGNIFYING_GLASS_TILTED_RIGHT}"
reject_invoice = lambda technical_code, brand, count, reason: f"دلیل لغو فاکتور کد فنی {technical_code} با برند {brand} به تعداد {count} عدد:\n\n{reason}\n\n{emoji.DIAMOND_WITH_A_DOT}"
arguments_required = lambda minimum, count: f"برای استفاده از این دستور باید {'حداقل' if minimum else 'حداکثر' } {count} شناسه را وارد کنید.\n\n{emoji.CROSS_MARK}"
access_invoice = lambda technical_code, brand, count: f"کد فنی {technical_code} با برند {brand} به تعداد {count} عدد فاکتور شد.\n\n{emoji.CHECK_MARK_BUTTON}"
existation = lambda validation, x, y: f"{x} مورد نظر شما اکنون در لیست {x} های {y} وجود {'دارد' if validation else 'ندارد'}.\n\n{emoji.CROSS_MARK}"
active_status = lambda validation: f"ربات در حال حاضر {'روشن' if validation else 'خاموش'} میباشد.\n\n{emoji.DIAMOND_WITH_A_DOT}"
updated = lambda process_type, x, y: f"{x} مورد نظر شما در لیست {x} های {y} {process_type} شد.\n\n{emoji.CHECK_MARK_BUTTON}"
message_date_count = lambda date, count: f"تعداد پیام ها در تاریخ {date}، {count} عدد میباشد.\n\n{emoji.CHECK_MARK_BUTTON}"
offer_price_percnet = lambda percent: f"اصلاح قیمت پیشنهادی {percent} درصد است.\n\n{emoji.CHECK_MARK_BUTTON}"
sended_message = lambda count: f"پیام شما به {count} کاربر ارسال شد.\n\n{emoji.CHECK_MARK_BUTTON}"
searched_similar = lambda technical_code: f"کد فنی های مشابه کد فنی {technical_code}:\n\n"
searched_description = lambda technical_code: f"توضیحات کد فنی {technical_code}:\n\n"
searched_group = lambda group_id: f"کد فنی های مشابه شناسه گروه {group_id}:\n\n"
empty = lambda x, y: f"متاسفانه هیچ {x} {y} وجود ندارد.\n\n{emoji.CROSS_MARK}"
all_technical_code = lambda x: f"تمام کد فنی های {x}:\n\n"
# Buttons
ADMIN_TECHNICAL_CODE_INFORMATOIN_HEADER = [InlineKeyboardButton("کد فنی", "None"), InlineKeyboardButton("برند", "None"), InlineKeyboardButton("آخرین قیمت", "None"), InlineKeyboardButton("قیمت پیشنهادی", "None")]
IMPORTANT_TECHNICAL_CODE_INFORMATOIN_HEADER = [InlineKeyboardButton("کد فنی", "None"), InlineKeyboardButton("برند", "None"), InlineKeyboardButton("قیمت", "None"), InlineKeyboardButton("وضعیت", "None")]
TECHNICAL_CODE_INFORMATOIN_HEADER = [InlineKeyboardButton("کد فنی", "None"), InlineKeyboardButton("برند", "None")]
ORDER_VIA_TELEGRAM = [InlineKeyboardButton("استعلام قیمت از طریق تلگرام", url=SELLER_LINK_USERNAME)]
JUST_VIEW = "این دکمه صرفا برای مشاهده است"

# Alerts
COMPLETE_PREVIOUS_INVOICING_REQUEST = "درخواست فاکتور قبلی را تکمیل کنید"
ENTER_TECHNICAL_CODE_COUNT = "تعداد مورد نیاز خود را ریپلای و ارسال کنید"
NOTHING_PRICE_TECHNICAL_CODE = "کد فنی مورد نظر شما فاقد قیمت میباشد"
PRICED_TECHNICAL_CODE = "کد فنی مورد نظر شما دارای قیمت میباشد"
REJECTED_REASON = "دلیل رد کردن درخواست را ریپلای و ارسال کنید"
CANCELED_TECHNICAL_CODE_REQUEST = "درخواست شما لغو شد"
REQUEST_SENDED = f"درخواست شما با موفقیت ارسال شد"
REQUEST_HANDLED = "درخواست با موفقیت رسیدگی شد"


# Classes
class ImportantUser:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.NOT_EXISTANCE = "NOT_EXISTANCE"
        self.EXISTANCE = "EXISTANCE"
        self.SUCCESS = "SUCCESS"
        self.EMPTY = "EMPTY"

    @staticmethod
    async def all():
        important_users = await execute("SELECT user_id FROM important_users;", None, "all")
        if important_users:
            important_users = [user[0] for user in important_users]
            return important_users
        else:
            return "EMPTY"

    async def add(self):
        important_users = await self.all()
        if important_users == "EMPTY":
            important_users = []
        if self.user_id in important_users:
            return self.EXISTANCE
        else:
            await execute("INSERT INTO important_users(user_id) VALUES(?);", (self.user_id,), None)
            return self.SUCCESS

    async def delete(self):
        important_users = await self.all()
        if important_users == self.EMPTY:
            return self.EMPTY
        elif self.user_id in important_users:
            await execute("DELETE FROM important_users WHERE user_id=?;", (self.user_id,), None)
            return self.SUCCESS
        elif self.user_id not in important_users:
            return self.NOT_EXISTANCE


class User:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.EMPTY = "EMPTY"
        self.SUCCESS = "SUCCESS"

    async def all(self):
        users = await execute("SELECT user_id FROM users;", None, "all")
        if users:
            users = [user[0] for user in users]
            return users
        else:
            return self.EMPTY

    async def add(self):
        users = await self.all()
        if users == "EMPTY":
            users = []
        if self.user_id not in users and self.user_id not in ADMIN_IDS:
            await execute("INSERT INTO users(user_id) VALUES(?);", (self.user_id,), None)
            return self.SUCCESS


class Description:
    def __init__(self, technical_code: str) -> None:
        self.technical_code = technical_code.upper()
        self.NOT_EXISTANCE = "NOT_EXISTANCE"
        self.EXISTANCE = "EXISTANCE"
        self.SUCCESS = "SUCCESS"
        "EMPTY"

    @staticmethod
    async def all(convert_to_text: bool = False):
        technical_codes = await execute("SELECT technical_code FROM descriptions;", None, "all")
        if technical_codes:
            technical_codes = [technical_code[0] for technical_code in technical_codes]
            if convert_to_text:
                return all_technical_code("توضیح داده شده") + NEW_LINE.join(technical_codes) + f"\n\n{emoji.CHECK_MARK_BUTTON}"
            else:
                return technical_codes
        else:
            return "EMPTY"

    async def add(self, description: str):
        technical_codes = await self.all()
        if technical_codes == "EMPTY":
            technical_codes = []
        if self.technical_code in technical_codes:
            return self.EXISTANCE
        else:
            await execute("INSERT INTO descriptions(technical_code, description) VALUES(?,?);", (self.technical_code, description), None)
            return self.SUCCESS

    async def update(self, description: str):
        technical_codes = await self.all()
        if technical_codes == "EMPTY":
            return "EMPTY"
        else:
            if self.technical_code in technical_codes:
                await execute("UPDATE descriptions SET description=? WHERE technical_code=?;", (description, self.technical_code), None)
                return self.SUCCESS
            else:
                return self.NOT_EXISTANCE

    async def search(self, convert_to_text: bool = False):
        technical_codes = await self.all()
        if technical_codes == "EMPTY":
            return "EMPTY"
        else:
            if self.technical_code in technical_codes:
                description = await execute("SELECT description FROM descriptions WHERE technical_code=?;", (self.technical_code,), "one")
                description = description[0]
                if convert_to_text:
                    return searched_description(self.technical_code) + description + f"\n\n{emoji.CHECK_MARK_BUTTON}"
                else:
                    return description
            else:
                return self.NOT_EXISTANCE

    async def delete(self):
        technical_codes = await self.all()
        if technical_codes == "EMPTY":
            return "EMPTY"
        else:
            if self.technical_code in technical_codes:
                await execute("DELETE FROM descriptions WHERE technical_code=?;", (self.technical_code,), None)
                return self.SUCCESS
            else:
                return self.NOT_EXISTANCE


class Important:
    def __init__(self, technical_code: str) -> None:
        self.technical_code = technical_code.upper()
        self.NOT_EXISTANCE = "NOT_EXISTANCE"
        self.EXISTANCE = "EXISTANCE"
        self.SUCCESS = "SUCCESS"
        "EMPTY"

    @staticmethod
    async def all(convert_to_text: bool = False):
        technical_codes = await execute("SELECT technical_code FROM importants;", None, "all")
        if technical_codes:
            technical_codes = [technical_code[0] for technical_code in technical_codes]
            if convert_to_text:
                return all_technical_code("مهم") + NEW_LINE.join(technical_codes) + f"\n\n{emoji.CHECK_MARK_BUTTON}"
            else:
                return technical_codes
        else:
            return "EMPTY"

    @staticmethod
    async def get(technical_codes: dict):
        importants = {}
        if technical_codes:
            all_importants = await Important.all()
            for technical_code in technical_codes.copy().keys():
                if technical_code in all_importants:
                    importants[technical_code] = technical_codes[technical_code]
                    technical_codes.pop(technical_code)
        return importants

    async def add(self):
        technical_codes = await self.all()
        if technical_codes == "EMPTY":
            technical_codes = []
        if self.technical_code in technical_codes:
            return self.EXISTANCE
        else:
            await execute("INSERT INTO importants(technical_code) VALUES(?);", (self.technical_code,), None)
            return self.SUCCESS

    async def delete(self):
        technical_codes = await self.all()
        if technical_codes == "EMPTY":
            return "EMPTY"
        else:
            if self.technical_code in technical_codes:
                await execute("DELETE FROM importants WHERE technical_code=?;", (self.technical_code,), None)
                return self.SUCCESS
            else:
                return self.NOT_EXISTANCE


class SimilarGroup:
    def __init__(self, group_id: int) -> None:
        self.group_id = group_id
        self.NOT_EXISTANCE = "NOT_EXISTANCE"
        self.EXISTANCE = "EXISTANCE"
        self.SUCCESS = "SUCCESS"
        "EMPTY"

    @staticmethod
    async def all(conver_to_text: bool = False):
        group_ids = await execute("SELECT group_id FROM similars;", None, "all")
        if group_ids:
            group_ids = list({group_id[0] for group_id in group_ids})
            if conver_to_text:
                return SIMILARS + NEW_LINE.join([str(item) for item in group_ids]) + f"\n\n{emoji.CHECK_MARK_BUTTON}"
            else:
                return group_ids
        else:
            return "EMPTY"

    async def add(self, technical_code: str, technical_code_one: str):
        technical_code_one = technical_code_one.upper()
        technical_code = technical_code.upper()
        technical_code_informations = {}
        group_ids = await self.all()
        if group_ids == "EMPTY":
            group_ids = []
        for item in [technical_code, technical_code_one]:
            technical_code_informations[item] = await execute("SELECT group_id FROM similars WHERE technical_code=?;", (item,), "one")
        match list(technical_code_informations.values()).count(None):
            case 2:
                group_id = random.randrange(10**9, 10**10)
                while group_id in group_ids:
                    group_id = random.randrange(10**9, 10**10)
                for key, value in technical_code_informations.items():
                    if value == None:
                        await execute("INSERT INTO similars(technical_code, group_id) VALUES(?, ?);", (key, group_id), None)
                return self.SUCCESS
            case 1:
                group_id = list(technical_code_informations.values())
                group_id.remove(None)
                group_id = group_id[0][0]
                for key, value in technical_code_informations.items():
                    if value == None:
                        await execute("INSERT INTO similars(technical_code, group_id) VALUES(?, ?);", (key, group_id), None)
                return self.SUCCESS
            case 0:
                return self.EXISTANCE

    async def search(self, convert_to_text: bool = False):
        group_ids = await self.all()
        if group_ids == "EMPTY":
            return "EMPTY"
        else:
            if self.group_id in group_ids:
                technical_codes = await execute("SELECT technical_code FROM similars WHERE group_id=?;", (self.group_id,), "all")
                technical_codes = [technical_code[0] for technical_code in technical_codes]
                if convert_to_text:
                    return searched_group(self.group_id) + NEW_LINE.join(technical_codes) + f"\n\n{emoji.CHECK_MARK_BUTTON}"
                else:
                    return technical_codes
            else:
                return self.NOT_EXISTANCE

    async def delete(self):
        group_ids = await self.all()
        if group_ids == "EMPTY":
            return "EMPTY"
        else:
            if self.group_id in group_ids:
                await execute("DELETE FROM similars WHERE group_id=?;", (self.group_id,), None)
                return self.SUCCESS
            else:
                return self.NOT_EXISTANCE


class Similar:
    def __init__(self, technical_code: str) -> None:
        self.technical_code = technical_code.upper()
        self.NOT_EXISTANCE = "NOT_EXISTANCE"
        self.EXISTANCE = "EXISTANCE"
        self.SUCCESS = "SUCCESS"
        "EMPTY"

    @staticmethod
    async def all(convert_to_text: bool = False):
        group_ids = await SimilarGroup.all()
        if group_ids == "EMPTY":
            return "EMPTY"
        else:
            data = {}
            for group_id in group_ids:
                technical_codes = await execute("SELECT technical_code FROM similars WHERE group_id=?;", (group_id,), "all")
                technical_codes = [technical_code[0] for technical_code in technical_codes]
                data[group_id] = technical_codes
            if convert_to_text:
                text = all_technical_code("مشابه")
                for group_id, technical_codes in data.items():
                    text += f"{group_id}:\n\n{', '.join(technical_codes)}\n\n"
                text += f"{emoji.CHECK_MARK_BUTTON}"
                return text
            else:
                return data

    @staticmethod
    async def get(text:str):
        similars = await Similar.all()
        all_technical_codes = await finder(text, search_length(text))
        if similars != "EMPTY":
            for technical_codes in similars.values():
                for technical_code in technical_codes:
                    if technical_code in text:
                        for technical_code_one in technical_codes:
                            searched_technical_code = await finder(technical_code_one, 10)
                            all_technical_codes.update(searched_technical_code)
        return all_technical_codes

    async def delete(self):
        technical_codes = await self.all()
        technical_codes = list(itertools.chain.from_iterable(technical_codes.values()))
        if technical_codes == "EMPTY":
            return "EMPTY"
        else:
            if self.technical_code in technical_codes:
                await execute("DELETE FROM similars WHERE technical_code=?;", (self.technical_code,), None)
                return self.SUCCESS
            else:
                return self.NOT_EXISTANCE

    async def search(self, convert_to_text: bool = False):
        technical_codes = await self.all()
        if technical_codes == "EMPTY":
            return "EMPTY"
        else:
            group_id = await execute("SELECT group_id FROM similars WHERE technical_code=?;", (self.technical_code,), "one")
            if group_id:
                group_id = group_id[0]
                group_object = SimilarGroup(group_id)
                similars = await group_object.search()
                similars.remove(self.technical_code)
                if convert_to_text:
                    return searched_similar(self.technical_code) + NEW_LINE.join(similars) + f"\n\nشناسه گروه: {group_id}\n\n{emoji.MEMO}"
                else:
                    return similars
            else:
                return self.NOT_EXISTANCE


class MessageDateCount:
    "NOT_EXISTANCE"
    "SUCCESS"
    "EMPTY"

    @staticmethod
    async def all(convert_to_text: bool = False):
        message_counts = await execute("SELECT date, count FROM messages;", None, "all")
        if message_counts:
            if convert_to_text:
                message_counts = [f"{item[0]} {item[1]}" for item in message_counts]
                return MESSAGE_DATE_COUNTS + NEW_LINE.join(message_counts) + f"\n\n{emoji.CHECK_MARK_BUTTON}"
            else:
                return dict(message_counts)
        else:
            return "EMPTY"

    async def add(self):
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        message_counts = await self.all()
        if message_counts == "EMPTY":
            message_counts = []
        if today not in message_counts:
            await execute("INSERT INTO messages(date, count) VALUES(?, 0);", (today,), None)
        previous_count = await execute("SELECT count FROM messages WHERE date=?;", (today,), "one")
        previous_count = previous_count[0]
        new_count = previous_count + 1
        await execute("UPDATE messages SET count=? WHERE date=?;", (new_count, today), None)
        return "SUCCESS"

    async def get(self, date: str, convert_to_text: bool = False):
        message_counts = await self.all()
        if message_counts == "EMPTY":
            return "EMPTY"
        else:
            if date in message_counts:
                message_count = await execute("SELECT count FROM messages WHERE date=?;", (date,), "one")
                message_count = message_count[0]
                if convert_to_text:
                    return message_date_count(date, message_count)
                else:
                    return dict(date, message_count)
            else:
                return "NOT_EXISTANCE"


class OfferPriceModification:
    "SUCCESS"

    @staticmethod
    async def get():
        percent = await execute("SELECT percent FROM offer_price_modification;", None, "one")
        return percent[0]

    @staticmethod
    async def update(percent):
        await execute("UPDATE offer_price_modification SET percent=?;", (percent,), None)
        return "SUCCESS"


# Functions
async def return_to_requester(technical_codes: dict, message: Message, admin_id: int):
    full_name = get_full_name(message)
    user_id = message.from_user.id
    if technical_codes:
        reply_markup = [[InlineKeyboardButton(full_name, "None")], ADMIN_TECHNICAL_CODE_INFORMATOIN_HEADER]
        for technical_code, informations in technical_codes.items():
            for item in informations:
                brand, count, last_sale_price, offer_price = item.split("_")
                modified_last_sale_price = modify_number(last_sale_price) if modify_number(last_sale_price) != "0" else None
                modified_offer_price = modify_number(offer_price) if modify_number(offer_price) != "0" else None
                row_buttons = [
                    InlineKeyboardButton(technical_code, f"RTC@{user_id}_{technical_code}_{brand}_{count}_0"),
                    InlineKeyboardButton(brand, f"TCI@{technical_code}_{brand}_{count}"),
                    InlineKeyboardButton(modified_last_sale_price if modified_last_sale_price else emoji.CROSS_MARK, f"RTC@{user_id}_{technical_code}_{brand}_{count}_{last_sale_price}"),
                    InlineKeyboardButton(modified_offer_price if modified_offer_price else emoji.CROSS_MARK, f"RTC@{user_id}_{technical_code}_{brand}_{count}_{offer_price}"),
                ]
                reply_markup.append(row_buttons)
        reply_markup = InlineKeyboardMarkup(reply_markup)
        await api_app.send_message(admin_id, TECHNICAL_CODE_REQUESTED, reply_markup=reply_markup)


async def populars(technical_code: str = None, convert_to_text: bool = False):
    if os.path.isfile(POPULAR_FILE):
        file = open(POPULAR_FILE, "r")
        technical_codes = json.load(file)
        file.close()
        if technical_codes:
            data = dict(sorted({technical_code: number for technical_code, number in technical_codes.items() if number >= MAXIMUM_POPULAR_NUMBER}.items(), key=lambda x: x[1], reverse=True))
            if technical_code:
                technical_code = technical_code.upper()
                data = dict(filter(lambda item: item[0].startswith(technical_code), data.items()))
                if convert_to_text:
                    return FOUNDED_POPULAR + NEW_LINE.join([f"{technical_code[0]} {technical_code[1]}" for technical_code in data.items()]) + f"\n\n{emoji.CHECK_MARK_BUTTON}"
                else:
                    return data
            else:
                if convert_to_text:
                    return all_technical_code("معروف") + NEW_LINE.join([f"{technical_code[0]} {technical_code[1]}" for technical_code in data.items()]) + f"\n\n{emoji.CHECK_MARK_BUTTON}"
                else:
                    return data
        else:
            return "EMPTY_FILE"
    else:
        return "NOT_EXISTANCE_FILE"


async def header_generator(session: aiohttp.ClientSession, data: dict):
    headers = {"accept": "*/*", "Content-Type": "application/json"}
    async with session.post("http://wsrest.hoseinparts.ir/token", headers=headers, json=data) as response:
        token = (await response.json())["token"]
        headers["Authorization"] = f"Bearer {token}"
        return headers


async def finder(text: str, length: int):
    data = {"menuID": 87, "pagelenth": 999999999, "order_column": 1, "order_dir": "desc", "startRecord": 0, "condition": "$App$"}
    percent = await OfferPriceModification.get()
    async with aiohttp.ClientSession() as session:
        headers = await header_generator(session, {"password": "U$MKBSVPAIr3DMA(", "userName": "wsuser"})
        async with session.post("http://wsrest.hoseinparts.ir/ShowList", headers=headers, json=data) as response:
            data = json.loads((await response.json())["result"].replace("'", '"'))["Data"]
            property_codes = [item["PropertyCode"].upper() for item in data]
            brands = [item["Brand"].capitalize() for item in data]
            stocks = [int(item["Stock"]) for item in data]
            last_sale_prices = [int(item["LastSalePrice"]) for item in data]
            offer_prices = [int(item["OfferPrice"]) for item in data]
            rows = list(zip(property_codes, brands, stocks, last_sale_prices, offer_prices))
            technical_codes = {}
            text = text.upper()
            for row in rows:
                last_sale_price = row[3]
                property_code = row[0]
                offer_price = row[4]
                if percent != 0:
                    offer_price = int(offer_price + offer_price * (percent / 100))
                brand = row[1]
                count = row[2]
                if len(property_code) == 10:
                    if property_code[0:length] in text and int(count) > 0:
                        if property_code in technical_codes:
                            technical_codes[property_code].add(f"{brand}_{count}_{last_sale_price}_{offer_price}")
                        else:
                            technical_codes[property_code] = {f"{brand}_{count}_{last_sale_price}_{offer_price}"}
            return technical_codes


async def founded_technical_code(technical_codes: dict, message: Message):
    user_id = message.from_user.id
    important_users = await ImportantUser.all()
    forward_from = message.forward_from
    reply_markup = [TECHNICAL_CODE_INFORMATOIN_HEADER]
    text = FOUNDED_TECHNICAL_CODE
    if important_users == "EMPTY":
        important_users = []
    if user_id in ADMIN_IDS:
        reply_markup = [ADMIN_TECHNICAL_CODE_INFORMATOIN_HEADER]
        if forward_from:
            forward_from_id = forward_from.id
            text = FOUNDED_TECHNICAL_CODE_FORWARD_FROM
    elif user_id in important_users:
        reply_markup = [IMPORTANT_TECHNICAL_CODE_INFORMATOIN_HEADER]
    for technical_code, data in technical_codes.items():
        for information in data:
            brand, count, last_sale_price, offer_price = information.split("_")
            modified_last_sale_price = modify_number(last_sale_price) if modify_number(last_sale_price) != "0" else None
            modified_offer_price = modify_number(offer_price) if modify_number(offer_price) != "0" else None
            if forward_from and user_id in ADMIN_IDS:
                row_buttons = [
                    InlineKeyboardButton(technical_code, f"RTC@{forward_from_id}_{technical_code}_{brand}_{count}_0"),
                    InlineKeyboardButton(brand, f"TCI@{technical_code}_{brand}_{count}"),
                    InlineKeyboardButton(modified_last_sale_price if modified_last_sale_price else emoji.CROSS_MARK, f"RTC@{forward_from_id}_{technical_code}_{brand}_{count}_{last_sale_price}"),
                    InlineKeyboardButton(modified_offer_price if modified_offer_price else emoji.CROSS_MARK, f"RTC@{forward_from_id}_{technical_code}_{brand}_{count}_{offer_price}"),
                ]
            else:
                if user_id in ADMIN_IDS:
                    row_buttons = [
                        InlineKeyboardButton(technical_code, f"None"),
                        InlineKeyboardButton(brand, f"TCI@{technical_code}_{brand}_{count}"),
                        InlineKeyboardButton(modified_last_sale_price if modified_last_sale_price else emoji.CROSS_MARK, "None"),
                        InlineKeyboardButton(modified_offer_price if modified_offer_price else emoji.CROSS_MARK, "None"),
                    ]
                elif user_id in important_users:
                    row_buttons = [
                        InlineKeyboardButton(technical_code, f"None"),
                        InlineKeyboardButton(brand, f"TCI@{technical_code}_{brand}_{count}"),
                        InlineKeyboardButton(modified_offer_price if modified_offer_price else "استعلام قیمت", f"P@{technical_code}_{brand}_{count}_{offer_price}" if offer_price == "0" else "None"),
                        InlineKeyboardButton("فاکتور", f"I@{technical_code}_{brand}_{offer_price}"),
                    ]
                else:
                    row_buttons = [
                        InlineKeyboardButton(technical_code, f"None"),
                        InlineKeyboardButton(brand, f"TCI@{technical_code}_{brand}_{count}"),
                    ]
            reply_markup.append(row_buttons)
    if forward_from and user_id in ADMIN_IDS:
        first_name = forward_from.first_name
        last_name = forward_from.last_name
        full_name = f"{first_name}{'' if last_name is None else f' {last_name}'}"
        reply_markup = [[InlineKeyboardButton(full_name, "None")]] + reply_markup
    elif user_id not in (ADMIN_IDS + important_users):
        reply_markup.append(ORDER_VIA_TELEGRAM)
    await message.reply_text(text, True, reply_markup=InlineKeyboardMarkup(reply_markup))
