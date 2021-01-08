# Перевод документации из JavaDoc в HTML
Автор: Чиркин Александр (группа КБ-201)(chirkin2001@list.ru)

## Установка
```
git clone https://github.com/AleksandrChirkin/javadoc2html
pip3 install -r requirements.txt
```

## Получить справку
```
python3 -m javadoc2html -h
```

## API

Приложение выполняет функции утилиты javadoc2html.

## Пример:
```
python3 -m javadoc2html tests\java
python -m javadoc2html tests\java\TestInterface.java tests\java\TestClass.java
```

# Автор
*Name-users (name.users@mail.ru)* 