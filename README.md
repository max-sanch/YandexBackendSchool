# Тестовое задание для школы бэкенд-разработки


* [Инструкции](#guides)
    * [Запуск приложения](#launch-app)
        * [На Windows](#Windows)
        * [На Linux](#Linux)
    * [Тестирование](#tests)

## <a name="guides"></a> Инструкции

### <a name="launch-app"></a>Запуск приложения

Для запуска приложения вам необходимы `Docker` и `docker-compose`

#### <a name="Windows"></a>На Windows

1) Установите _Line Separator_ у файла `entrypoint.sh` на значение _LF_

2) Находясь в директории проекта введите:

	    docker-compose up --build

#### <a name="Linux"></a>На Linux

1) Дайте права файлу `entrypoint.sh`:

        sudo chmod +x entrypoint.sh
    
2) Находясь в директории проекта введите:

	    sudo docker-compose up --build

### <a name="tests"></a>Тестирование

Находясь в директории проекта введите:

	docker-compose --file docker-compose-test.yml up --build