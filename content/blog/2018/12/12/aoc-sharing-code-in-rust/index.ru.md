+++
title = "AOC: переиспользуем код в Rust"
date = 2018-12-12T10:56:19Z
updated = 2018-12-12T11:12:21Z

[taxonomies]
tags = ["rust", "aoc"]

[extra]
lang = "ru"
teletype = "https://blog.antono.info/rkoLYw01V"
+++
После первой задачки Advent of Code у меня нашлась функция, которую стоит переиспользовать:

```rust
use std::fs::File;
use std::io::prelude::*;

// TODO: Share between puzzles...
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

Хочу вынести её в отдельный файл и как-нибудь переиспользовать во [всех своих решениях](https://github.com/antono/aoc2018). Быстрый гуглёж приводит к главе «[Using Modules to Reuse and Organize Code](https://doc.rust-lang.org/1.30.0/book/second-edition/ch07-00-modules.html)» из The Rust Book.

> Что делать, если функций становится слишком много? В Rust есть система модулей, которая позволяет переиспользовать код, не теряя порядка.

Отлично! Две важные вещи прямо с первой страницы:

- По умолчанию функции, типы, константы и модули приватны. Ключевое слово `pub` делает элемент публичным, а значит, видимым за пределами его пространства имён.
- Ключевое слово `use` вводит в область видимости модули или определения внутри модулей, чтобы на них было проще ссылаться.

Модули в Rust можно раскладывать довольно гибко, и для их организации есть свои правила. В моём простом случае хватило нескольких шагов:

1. Перенёс функцию в отдельный файл \`src/utils.rs\`
2. добавил перед функцией ключевое слово pub: pub fn read_puzzle_input...
3. и дописал небольшой кусочек в Cargo.toml:

```toml
[lib]
name = "utils"
path = "src/utils.rs"
```

Теперь, чтобы пользоваться функциями из этой библиотеки, нужно добавить в начало файла объявление крейта и вызывать функцию через пространство имён utils:

```rust
extern crate utils;

fn part_one() {
    let input = utils::read_puzzle_input(1);
    let mut result: i32 = 0;

    for line in input.lines() {
        let num = line.parse::<i32>().unwrap();
        result += num;
    }

    println!("Sum of freq adjustments: {}", result);
}
```

[Код](https://github.com/antono/aoc2018).

---

[Дисклеймер](@/blog/2018/12/09/aoc-posts-disclaimer/index.ru.md)
