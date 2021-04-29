# Aggregator
Паттерн объединяет результаты работы нескольких сервисов. Для сокращения количества
кода и простоты восприятия сервисы представлены эндпоинтами. 
В примере есть 4 сервиса:
1. Агрегатор - aggregator_handler
2. Сервис хранящий карты - card_service_handler
3. Сервис журнала транзакций по картам - card_operations_log
4. Сервис рекламных предложений - card_advert_log

## Зачем?
Зачем это нужно? Если всё, то же самое можно переместить на фронт?
Можно, и всё зависит от:
1. Кол-ва условных фронтов на которых придётся производить агрегацию. Т.е.
   если есть браузер, мобильное приложение, ещё любой клиент. То на каждом
   придётся совершать 3 запроса, следить за их выполнением и т.п.
2. Помимо уменьшения кол-ва кода и трудозатрат на потребителях Aggregator позволит
   создать единую точку ответственности. В код которой можно будет быстро внести
   изменения. И эти изменения сразу станут доступны для всех клиентов.

## Задача
Есть задача получать данные по карте из каждого из этих сервисов. На пример
фронтенд должен отобразить информацию о карте, последние транзакции и рекламу 
кредитов.
Варианты решения:
1. Можно отправить три запроса к разным сервисам. 
2. Если все сервисы за API gateway, то запрос превратиться к 3 эднпоинтам.
3. Паттерн агрегатор. Забегая вперёд, многие API gateway предоставляют паттерн Aggregator.

Таким образом при запросе ендпоинта Aggregator-а. Aggregator совершает 3 запроса
к необходимым сервисам. И в случае недоступности какого-то из сервисов возвращает 
частичную информацию или сообщение о недоступности (этот пункт зависит 
исключительно от бизнес-требований).