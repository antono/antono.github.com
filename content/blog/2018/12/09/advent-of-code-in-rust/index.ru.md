+++
title = "Advent of Code на Rust"
date = 2018-12-09T17:35:42Z
updated = 2022-04-15T12:13:00Z

[taxonomies]
tags = ["rust"]

[extra]
lang = "ru"
teletype = "https://blog.antono.info/rysyH35JN"
+++
![](750cae79-3911-480a-aebb-32aaa4d35549.jpeg)

*Фото: [Paul VanDerWerf](https://www.flickr.com/photos/pavdw/) ([CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)), кадрировано.*

---

## Мотивация

Один [умный человек](https://github.com/onesk) подбил меня поучаствовать в [Advent of Code](https://adventofcode.com/).

Здесь я буду описывать своё путешествие в мир языка Rust. Задача этих постов — лучше разобраться в Rust, записывая всё, до чего додумался. Когда пишешь публично, ответственности больше: приходится дважды подумать и почитать побольше документации перед публикацией, чтобы выглядеть не так глупо, как есть на самом деле.

С Rust я знаком на базовом уровне — делал для себя небольшие эксперименты. Из теории — где-то год назад читал интересные мне главы [The Rust Book](https://doc.rust-lang.org/book/).

В этом посте я опишу всё, что сделал, чтобы начать. В следующих, скорее всего, будет меньше инструкций и больше личных наблюдений о Rust.

---

## Структура проекта

Сначала я поставил Rust с помощью [rustup](https://rustup.rs/). Одна простая команда — и всё, что нужно, на месте.

Затем сгенерировал новый проект замечательным инструментом [cargo](https://doc.rust-lang.org/cargo/):

```console
cargo new aoc2018
cd aoc2018
tree .
.
├── Cargo.toml
└── src
    └── main.rs

1 directory, 2 files
```

Cargo — встроенный в Rust пакетный менеджер и система сборки. Умеет он больше, чем другие пакетные менеджеры, с которыми я работал (gem, bundler, npm, pip). Вот неполный список того, что cargo может сделать за вас:

- Сгенерировать новый проект
- Собрать проект и прогнать тесты
- Управлять зависимостями проекта, указанными в Cargo.toml
- Опубликовать ваш пакет на [crates.io](https://crates.io/)
- Отформатировать код

В других языках для всего перечисленного есть отдельные инструменты, но подход команды Rust позволяет очень легко начать, без мороки со всеми этими разрозненными деталями.

Сгенерированный по умолчанию код — это программа «Hello World», и запустить её проще простого:

```console
cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/aoc2018`
Hello, world!
```

Дальше я поменяю структуру проекта так, чтобы на каждую задачу собирался отдельный исполняемый файл.

[Раздел о структуре проекта](https://doc.rust-lang.org/cargo/guide/project-layout.html) в Cargo Book говорит, что исполняемые файлы должны лежать в src/bin/\*.rs.

Перестраиваем проект:

```console
cd src
mkdir bin
mv main.rs bin/1.rs
cd ../../
cargo run
   Compiling aoc2018 v0.1.0 (file:///private/tmp/aoc2018)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `/private/tmp/aoc2018/target/debug/1`
Hello, world!
```

## Задача №1

Пора браться за код.

Если коротко: на входе список чисел, по одному на строку, каждое со знаком плюс или минус. Ответ — их сумма. Входные данные выглядят так:

```text
+13
+9
+8
+1
-15
+10
...
```

Я вставил эти данные в inputs/1.txt в корне проекта. Все входные данные я собираюсь складывать в эту папку, так что хочу написать универсальную функцию для чтения этих файлов. Читать документацию по API мне лень, но гугл подсказывает [хороший пример из Rust Book](https://doc.rust-lang.org/1.30.0/book/second-edition/ch12-02-reading-a-file.html).

Подгоняю пример под себя:

```rust
use std::fs::File;
use std::io::prelude::*;

fn read_puzzle_input(number: u8) -> String {
    let mut input =
        File::open(format!("./inputs/{}.txt", number))
            .expect("Puzzle input not found...");
    let mut text = String::new();

    input
        .read_to_string(&mut text)
        .expect("cannot read input file");

    return text;
}
```

Так. Теперь нужно пройтись по строкам, распарсить их и сложить. К счастью, у String в Rust есть встроенный [метод *lines()*](https://doc.rust-lang.org/std/string/struct.String.html#method.lines). Он возвращает [итератор Lines](https://doc.rust-lang.org/std/str/struct.Lines.html), который можно использовать в циклах:

```rust
fn main() {
    let input = read_puzzle_input(1);

    for line in input.lines() {
        println!("{}", result);
    }
}
```

Это было легко. Пора парсить числа. Первой мыслью было брать из каждой строки знак в нулевой позиции, а остаток строки разбирать как целое число. Потом с помощью [ключевого слова match](https://doc.rust-lang.org/rust-by-example/flow_control/match.html) либо прибавлять его к какой-нибудь переменной, либо вычитать. Но когда я взялся за парсинг целых, оказалось, что в Rust есть метод [str::parse](https://doc.rust-lang.org/std/primitive.str.html#method.parse), который превращает строки в значения других типов. Даже проще, чем я думал!

```rust
fn main() {
    let input = read_puzzle_input(1);
    let mut result: i32 = 0;

    for line in input.lines() {
        let num = line.parse::<i32>().unwrap();
        result += num;
    }

    println!("{}", result);
}
```

Запускаем:

```console
 cargo run
   Compiling aoc2018 v0.1.0 (file:///Users/antono/Code/rust/aoc2018)
    Finished dev [unoptimized + debuginfo] target(s) in 0.92 secs
     Running `target/debug/1`
493
```

Работает. Ответ принят, и у меня первая звёздочка в челлендже.

Отлично!

Если кому интересно, [код лежит на GitHub](https://github.com/antono/aoc2018).

---

## Что надо разобрать

Кое-что в коде я пока не могу себе толком объяснить.

File::open() без .expect() даёт ошибку компиляции

```rust
File::open(filename).expect("error message");
```

Функция parse без вызова .unwrap() тоже даёт ошибку компиляции.

```rust
line.parse::<i32>().unwrap();
```

С File всё вроде понятно, но зачем мне prelude?

```rust
use std::fs::File;
use std::io::prelude::*;
```

Ответы опишу в следующих постах.

---

[Дисклеймер](@/blog/2018/12/09/aoc-posts-disclaimer/index.ru.md)
