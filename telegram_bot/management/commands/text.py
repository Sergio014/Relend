text_dict = {
    'en': {
        'buyer': 'You have purchased {account.name} from this user: <a href="tg://user?id={owner.telegram_id}">{owner.user.username}</a>?',
        'owner': "This user <a href='tg://user?id={buyer.telegram_id}'>{buyer.user.username}</a> wants to purchase your account named {account.name}. User rating: {status}. Please remember that you need to negotiate the purchase with the buyer personally. I'm only created to notify you about users who are interested in buying your account.",
        'sold_message': 'Congratulations, your account has been sold successfully!',
        'account_blocked': 'Your account has been blocked due to poor behavior',
    },
    'ua': {
        'buyer': 'Ви купили {account.name} у цього користувача: <a href="tg://user?id={owner.telegram_id}">{owner.user.username}</a>',
        'owner': "Ваш акаунт {account.name} хоче придбати цей користувач: <a href='tg://user?id={buyer.telegram_id}'>{buyer.user.username}</a> Рейтинг користувача: {status}. Нагадую, що про покупку з користувачем ви домовляєтесь особисто, я створений тільки для того, щоб оповіщати вас про бажаючих купити ваш акаунт.",
        'sold_message': 'Вітаю, ваш акаунт успішно продано :)',
        'account_blocked': 'Ваш акаунт був заблокований через погану поведінку',
    },
    'ru': {
        'buyer': 'Вы купили {account.name} у этого пользователя: <a href="tg://user?id={owner.telegram_id}">{owner.user.username}</a>?',
        'owner': "Ваш акаунт {account.name} хочет купить этот пользователь: <a href='tg://user?id={buyer.telegram_id}'>{buyer.user.username}</a>. Рейтинг пользователя: {status}. Напоминаю, что по покупке с пользователем вы договариваетесь лично, я создан только для того, чтобы оповещать вас о желающих купить ваш аккаунт.",
        'sold_message': 'Поздравляем, ваш аккаунт успешно продан!',
        'account_blocked': 'Ваш аккаунт был заблокирован из-за плохого поведения',
    }
}
