#Repository
Репозитории — это классы или компоненты, которые инкапсулируют логику, 
необходимую для доступа к источникам данных. Они централизуют общие функции
доступа к данным, обеспечивая лучшую ремонтопригодность и отделяя инфраструктуру
или технологии, используемые для доступа к базам данных, от уровня модели 
предметной области.

Т.е. репозиторий — это объект хранящий информацию и предоставляющий интерфейс
для работы с ней. Как и где репозиторий хранит данные это детали реализации и
это выходит за рамки паттерна.

Фактически репозиторий олицетворение полиморфизма.