1. Скачать `[`custom_modules`](https://github.com/CherMet90/custom_python_modules.git)` в домашнюю директорию
2. Проваливаемся в скачанную папку, устанавливаем зависимости `pip install -r requirements.txt`
3. Из папки `custom_modules` запускаем `pip install -e .`
4. Добавить переменные окружения `$NETBOX_URL` и `$NETBOX_TOKEN`  
    4.1 `nano ~/.bashrc`  
    4.2 Добавляем строчки в конец файла, сохраняем, закрываем
    ```
    export NETBOX_URL="http://your_netbox_instance.com"
    export NETBOX_TOKEN="your_netbox_api_token"
    ```
    4.3 Применить новые настройки в текущей сессии терминала (в новых применится автоматом):
    ```
    source ~/.bashrc
    ```
5. Запускаем py-скрипт `netbox_inventory.py` для получения списка всех устройств из Netbox в json-формате
6. Создать защищенное хранилище переменных плейбуков:  
    ```
    ansible-vault create creds.yml
    ```
    7.1 Добавить данные для авторизации на оборудовании:
    ```
    ansible_user: ваш_логин
    ansible_ssh_pass: ваш_пароль
    ```
    7.1.1 Сохранить и выйти: `:qw!`  
    7.1.2 Выйти без сохранения: `:qa!`  
    7.2 Команды для работы с хранилищем:
    ```
    ansible-vault edit creds.yml
    ansible-vault view creds.yml
    ```
7. К целевому списку устройств можно применить желаемый шаблон команд. Запускать из папки с плейбуками:  
`ansible-playbook -i ../inventories/prod/all_devices.yml shri.yml --ask-vault-pass`  
7.1 Отвечаем на несложные вопросы про группу, а позже про интерфейсы  
7.1.1 "must-have" группы, это группы, в которые устройства должны входить обязательно  
7.1.2 в "optional groups" перечисляем группы с логикой `OR`. Даже если логика `OR` не требуется, для корректной работы плейбука необходимо указать хотя бы одну группу как опциональную  