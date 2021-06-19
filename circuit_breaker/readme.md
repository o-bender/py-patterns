# Circuit Breaker
Паттерн кеширует неудачный ответ от ресурса.

## Зачем?
Зачем это нужно? Если можно просто вернуть ошибку и все дела.
Можно, но есть проблемы:
1. Если ресурс запрашиваемый долго отвечает (т.е. принимает соединение, но ответ 
   генерирует слишком долго из-за, к примеру, повышенной нагрузки), то ваш 
   сервис будет возвращать ошибку клиенту так же долго.
2. Если ваш ресурс долго отвечает, это выглядит как "задумчивость", а это знак
   для клиента, что надо нажать на кнопку "обновить".
3. В тот момент как проблемный сервис восстановиться нагрузка на него возрастёт 
   в несколько раз: обычные запросы + запросы "обновить". 

## Задача
Есть сервис условно "упавший" под нагрузкой в 10 запросов. Время на его 
восстановление 5 секунд. 