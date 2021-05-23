# Compiller
Компилятор под Pascal.
<!-- Файлы с примерами: -->
Файлы с примерами:
1) нахождение n чисел Фибоначи (fib.txt)
2) нахождение факториала числа z (fact.txt)
3) нахождение натуральных делителей числа a (div.txt)
4) вывод последовательности нечетных чисел от i до n (sequence.txt)
5) быстрое возведение числа в степень(pow.txt)
6) остальные примеры работы функциональных частей языка (others.txt)
7) вывод квадратного корня числа (sqrt.txt);

<!-- Файлы с примерами: -->
Запуск компонент:
1) лексер (выводит поток лексем): python -m lexer [название файла, например: div.txt]
2) парсер(выводит дерево): python -m Parser [название файла]
3) таблица символов (выводит символьную таблицу):python -m Table [название файла]
4) промежуточный код (выводит промежуточный код пооделеный на блоки) : python -m TAC [название файла]
5) генерация кода LLVMlite (генерирует файл tt.ll): python -m llvmgen [название файла]
6) Компиляция кода посредством LLVMlite: python -m Compiller [название файла]
