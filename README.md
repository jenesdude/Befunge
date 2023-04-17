# Befunge
Интерпретатор для эзотерического языка Befunge

Автор: Смагин Максим, КБ-401 (МЕН491015).

Задача: Реализация интерпретатора языка Befunge

Примеры использования: в папку Scripts добавлены несколько скриптов на языке Befunge.
cat.txt — программа, повторяющая вводимый текст
loop.txt — бесконечный цикл.
hello_world.txt — каноничный "Hello world"

Синтаксис основан на версии, изложенной по адресу https://esolangs.org/wiki/Befunge для Befunge-93.

К следующей версии планируется реализация следующего:
 * все ошибки обрабатываются как Exception'ы
 * покрытие кода тестами на 80% (включая тесты на I/O) с помощью библиотеки pytest