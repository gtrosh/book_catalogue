# Каталог книг

## Использование в режиме без подтверждения регистрации по адресу электронной почты:
В файле ```settings.py``` найти настройки Djoser:
  ```
  DJOSER = {
    'USER_ID_FIELD': 'username',
    'LOGIN_FIELD': 'email',
    'ACTIVATION_URL': 'account-activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}
  ```
Для использования приложения без подтверждения регистрации пользователя по электронной почте необходимо удалить / закомментировать строчки:
```
    'ACTIVATION_URL': 'account-activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
```
Также можно закомментировать путь ```path('account-activate/<uid>/<token>', ActivateUser.as_view())``` в файле ```book_catalogue_project/urls.py```.

## Использование в режиме с подтверждением регистрации по адресу электронной почты:
В настоящее время в приложении указаны настройки электронной почты для локального тестирования.
Для "боевого" использования потребуется:
1. Удалить строчку ```EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"``` в файле `settings.py`
2. Вместо этого можно добавить следующие настройки почты с использованием SMTP (как наиболее распространенный способ настройки почты):
   ```
   # settings.py
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com' # заменить на ваш SMTP-сервер
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'your_email_address@gmail.com' # заменить на ваш адрес электронной почты
    EMAIL_HOST_PASSWORD = 'your_email_password' # заменить на ваш пароль для электронной почты

   # в настройках Djoser к имеющемуся коду добавить:
   DJOSER = {
       'EMAIL': {
        'activation': 'djoser.email.ActivationEmail', # для новых пользователей при активации аккаунта
        'confirmation': 'djoser.email.ConfirmationEmail', # для существующих пользователей при изменении адреса электронной почты
    },
   }
  ```
