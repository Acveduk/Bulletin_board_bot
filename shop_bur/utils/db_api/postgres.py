import asyncpg


async def add_user_in_database(user_id: int, username: str, name: str):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )
    sql_command = f'SELECT 1 FROM users WHERE user_id = $1'
    select = await connect.fetch(sql_command, user_id)
    if len(select):
        await connect.close()
        return False
    else:
        sql_command = f'INSERT INTO users(user_id, username, name) VALUES ($1, $2, $3)'
        await connect.execute(sql_command, user_id, username, name)
        await connect.close()
        return True


async def check_date(date):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )
    sql_command = f'SELECT date_n FROM date_now'
    select = await connect.fetch(sql_command)
    if select[0]["date_n"] >= date:
        await connect.close()
    else:
        sql_command = f'UPDATE date_now SET date_n=$1'
        await connect.execute(sql_command, date)
        sql_command = f'UPDATE users SET check_num=0'
        await connect.execute(sql_command)
        await connect.close()


async def check_user(user_id: int):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'SELECT 1 FROM ban WHERE user_id = $1'

    select = await connect.fetch(sql_command, user_id)
    await connect.close()

    return len(select)


async def check_balance(user_id: int):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'SELECT money, check_num FROM users WHERE user_id = $1'

    select = await connect.fetch(sql_command, user_id)
    await connect.close()

    return select


async def add_money_user(user_id: int, money: int):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'UPDATE users SET money=$1 WHERE user_id=$2'
    await connect.execute(sql_command, money, user_id)
    await connect.close()


async def update_user_money_check(user_id: int, money: int, check_num: int):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'UPDATE users SET money=$1 WHERE user_id=$2'
    await connect.execute(sql_command, money, user_id)
    sql_command = f'UPDATE users SET check_num=$1 WHERE user_id=$2'
    await connect.execute(sql_command, check_num, user_id)
    await connect.close()


async def add_ad(user_id: int, media: str, text: str, check_media: str):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'INSERT INTO create_ad(user_id, media, text, check_media) VALUES ($1, $2, $3, $4)'
    await connect.execute(sql_command, user_id, media, text, check_media)
    await connect.close()


async def del_ad(user_id: int):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'DELETE FROM create_ad WHERE user_id=$1'
    await connect.execute(sql_command, user_id)
    await connect.close()


async def check_ad(user_id: int):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'SELECT media, text, check_media FROM create_ad WHERE user_id = $1'

    select = await connect.fetch(sql_command, user_id)
    await connect.close()

    return select


async def add_pay(user_id: int, money: int, bill_id: str):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'INSERT INTO pay_id(user_id, money, bill_id) VALUES ($1, $2, $3)'
    await connect.execute(sql_command, user_id, money, bill_id)
    await connect.close()


async def get_pay(bill_id: str):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'SELECT 1 FROM pay_id WHERE bill_id = $1'

    select = await connect.fetch(sql_command, bill_id)
    await connect.close()
    return len(select)


async def get_money(bill_id: str):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'SELECT money FROM pay_id WHERE bill_id = $1'

    select = await connect.fetch(sql_command, bill_id)
    await connect.close()
    return select


async def del_pay(bill_id: str):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'DELETE FROM pay_id WHERE bill_id = $1'
    await connect.execute(sql_command, bill_id)
    await connect.close()


async def del_pay2(user_id: int):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )
    sql_command = f'SELECT 1 FROM pay_id WHERE user_id = $1'
    select = await connect.fetch(sql_command, user_id)
    if len(select):
        sql_command = f'DELETE FROM pay_id WHERE user_id = $1'
        await connect.execute(sql_command, user_id)
        await connect.close()
    else:
        await connect.close()


async def add_user_ban(user_id):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f"SELECT 1 FROM ban WHERE user_id = $1"

    select = await connect.fetch(sql_command, user_id)

    if len(select):
        return False
    else:
        sql_command = f"INSERT INTO ban(user_id) VALUES ($1)"
        await connect.execute(sql_command, user_id)
        await connect.close()
        return True


async def del_user_ban(user_id):
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f"SELECT 1 FROM ban WHERE user_id = $1"

    select = await connect.fetch(sql_command, user_id)

    if len(select):
        sql_command = f"DELETE FROM ban WHERE user_id = $1"
        await connect.execute(sql_command, user_id)
        await connect.close()
        return True
    else:
        return False


async def select_all_user():
    connect = await asyncpg.connect(database='byr', user='postgres',
                                     )

    sql_command = f'SELECT user_id FROM users'

    select = await connect.fetch(sql_command)
    await connect.close()
    b = []
    for k in range(len(select)):
        b.append(select[k]['user_id'])

    return b
