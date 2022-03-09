Yatube
=====

Yatube - социальная сеть для публикации личных дневников.

Каждый автор, может создать свою страничку, выбрать для нее имя и уникальный адрес. Авторы могут создавать текстовые сообщения, прикреплять и ним картинки. Сообщения выводятся на аккаунты авторов, в общую ленту новостей, так же можно отправлять сообщения в разные тематические сообщества. У авторов есть возможность редактировать свои сообщения после публикации.

Пользователи могут заходить на страницы авторов, читать их записи, подписываться, комментировать. Для пользователей, помимо общей ленты сообщений, доступна лента только с сообщениями авторов, на которых они подписаны.
##
### 1. В проект добавлены кастомные страницы ошибок:
-   404 page_not_found
-   403 permission_denied_view

Написан тест, проверяющий, что страница 404 отдает кастомный шаблон.

### 2. С помощью sorl-thumbnail выведены иллюстрации к постам:
-   в шаблон главной страницы,
-   в шаблон профайла автора,
-   в шаблон страницы группы,
-   на отдельную страницу поста.

**Написаны тесты, которые проверяют:**
-   при выводе поста с картинкой изображение передаётся в словаре  `context`
    -   на главную страницу,
    -   на страницу профайла,
    -   на страницу группы,
    -   на отдельную страницу поста;
-   при отправке поста с картинкой через форму  **PostForm**  создаётся запись в базе данных;

### 3. Создана система комментариев
Написана система комментирования записей. На странице поста под текстом записи выводится форма для отправки комментария, а ниже — список комментариев. Комментировать могут только авторизованные пользователи. Работоспособность модуля протестирована.

### 4. Кеширование главной страницы
Список постов на главной странице сайта хранится в кэше и обновляется раз в 20 секунд.
Написан тест для проверки кеширования главной страницы. 

### 5. Добавлена система подписки на авторов
Написана система подписки на авторов, а так же отдельная лента постов с подписками.
написаны тесты, проверяющие работу нового сервиса:
-   Авторизованный пользователь может подписываться на других пользователей и удалять их из подписок.
-   Новая запись пользователя появляется в ленте тех, кто на него подписан и не появляется в ленте тех, кто не подписан.

Установка и запуск
----------


Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/serezhs/hw05_final.git
```

```
cd hw05_final
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:
```
cd yatube
```
```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```