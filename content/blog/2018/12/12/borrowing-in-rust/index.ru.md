+++
title = "Заимствование в Rust"
date = 2018-12-12T13:32:45Z
updated = 2018-12-18T23:07:19Z

[taxonomies]
tags = ["rust", "aoc"]

[extra]
lang = "ru"
teletype = "https://blog.antono.info/rJlqpIRJ4"
+++
![](82fbe53d-9aae-4cdf-b1fc-5ce5800367a2.jpeg)

Решаю на Rust [вторую задачку Advent of Code](https://adventofcode.com/2018/day/2). Задачка довольно простая. Входные данные выглядят так:

```text
mvgowxqubnhaefjslkjlrptzyi
pvgowlqubnhaefmslkjdrpteyi
ovgowoqubnhaefmslkjnrptzyi
cvgowxqubnrxefmslkjdrptzyo
cvgowxqubnhaefmsokjdrprzyf
cvgowxqubnhjeflslkjgrptzyi
...
```

Задание:

> ...подсчитайте, сколько ID **содержат какую-нибудь букву ровно два раза**, и отдельно — сколько **содержат какую-нибудь букву ровно три раза**. **Перемножив эти два числа**, вы получите \[ответ\]...

На псевдокоде решение выглядело бы примерно так:

```python
for line in input
   counters = count_letters(line)

seen_two_letters = 0
seen_three_letters = 0

for counter in counters
   if counter.values.includes(2)
      seen_two_letters += 1
   if counter.values.include(3)
      seen_three_letters += 1

print seen_two_letters * seen_three_letters
```

Теперь на Rust. Особо не заморачиваясь с оптимизацией, буду хранить количество каждого символа в строке в векторе из [HashMap](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Потом пройдусь по ним и посчитаю хеши, у которых среди значений есть 2 или 3.

```rust
extern crate utils;
use std::collections::HashMap;

fn part_one() {
    let input = utils::read_puzzle_input(2);

    for line in input.lines() {
        let mut counters: HashMap<char, u8> = HashMap::new();

        for chr in line.chars() {
            match counters.get(&chr).cloned() {
                Some(count) => counters.insert(chr, count + 1),
                None => counters.insert(chr, 1),
            };
        }
    }
}
```

Запускаем:

```console
➜  aoc2018 git:(master) ✗ cargo run --bin 2
   Compiling aoc2018 v0.1.0 (file:///Users/antono/Code/rust/aoc2018)
error[E0502]: cannot borrow `counters` as mutable because it is
also borrowed as immutable
  --> src/bin/2.rs:57:32
   |
56 |             match counters.get(&chr) {
   |                   -------- immutable borrow occurs here
57 |                 Some(count) => counters.insert(chr, count + 1),
   |                                ^^^^^^^^ mutable borrow occurs here
58 |                 None => counters.insert(chr, 1),
59 |             };
   |             - immutable borrow ends here

error[E0502]: cannot borrow `counters` as mutable because it is
also borrowed as immutable
  --> src/bin/2.rs:58:25
   |
56 |             match counters.get(&chr) {
   |                   -------- immutable borrow occurs here
57 |                 Some(count) => counters.insert(chr, count + 1),
58 |                 None => counters.insert(chr, 1),
   |                         ^^^^^^^^ mutable borrow occurs here
59 |             };
   |             - immutable borrow ends here

error: aborting due to 2 previous errors

For more information about this error, try `rustc --explain E0502`.
error: Could not compile `aoc2018`.

To learn more, run the command again with --verbose.
```

Перечитываю в Rust Book главы про [владение](https://doc.rust-lang.org/1.11.0/book/ownership.html) и [заимствование](https://doc.rust-lang.org/1.11.0/book/references-and-borrowing.html). С владением мне всё вроде бы понятно. А вот с заимствованием, тем более изменяемым, — не очень. Чтобы заимствовать правильно, надо соблюдать несколько правил:

> Во-первых, любое заимствование должно длиться не дольше, чем область видимости владельца. *Во-вторых, у вас может быть либо один, либо другой из этих двух видов заимствований, но не оба одновременно:* одна или несколько ссылок (`&T`) на ресурс либо **ровно одна изменяемая ссылка** (`&mut T`).

Выходит, проблема в том, что я заимствовал хеш-таблицу counters и на чтение, и на запись сразу. HashMap#get возвращает Option со ссылкой на значение (которое лежит в куче). А counter.insert() в то же самое время заимствует данные хеша как изменяемые, чтобы их поменять (всё в той же куче). Rust такого не допускает — ради безопасности памяти и чтобы не было состояния гонки:

> Владение — это способ, которым Rust достигает своей главной цели: безопасности памяти.

Один из способов не заимствовать значение из хеша на чтение — просто его скопировать. В документации к Option нашёлся полезный метод [.cloned()](https://doc.rust-lang.org/std/option/enum.Option.html#method.cloned).

> Превращает `Option<&T>` в `Option<T>`, клонируя содержимое Option.

Буду вызывать его, когда достаю значение из хеша:

```rust
fn part_one() {
    let input = utils::read_puzzle_input(2);

    for line in input.lines() {
        let mut counters: HashMap<char, u8> = HashMap::new();

        for chr in line.chars() {
            match counters.get(&chr).cloned() {
                Some(count) => counters.insert(chr, count + 1),
                None => counters.insert(chr, 1),
            };
        }

        println!("{:?}", counters.values());
    }
}
```

Запускаем:

```console
cargo run --bin 2
   Compiling aoc2018 v0.1.0 (file:///Users/antono/Code/rust/aoc2018)
    Finished dev [unoptimized + debuginfo] target(s) in 0.62 secs
     Running `target/debug/2`
[1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1]
[1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1]
[1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2]
[1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
[1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1]
...
```

Заработало. Смущает только, что приходится каждый раз копировать значение, лишь бы не заимствовать его на чтение. Один умный человек подсказал мне [HashMap#entry()](https://doc.rust-lang.org/std/collections/struct.HashMap.html#method.entry): он отдаёт Entry, через который значение в хеше можно менять прямо на месте. У самого Entry куча полезных методов. [Entry#and_modify()](https://doc.rust-lang.org/std/collections/hash_map/enum.Entry.html#method.and_modify) — ровно то, что мне нужно. Пример из документации:

```rust
use std::collections::HashMap;

let mut map: HashMap<&str, u32> = HashMap::new();

map.entry("poneyland")
   .and_modify(|e| { *e += 1 })
   .or_insert(42);

assert_eq!(map["poneyland"], 42);
```

Ух ты! Переделываю свой код вот с такого:

```rust
   for line in input.lines() {
        let mut counters: HashMap<char, u8> = HashMap::new();

        for chr in line.chars() {
            match counters.get(&chr).cloned() {
                Some(count) => counters.insert(chr, count + 1),
                None => counters.insert(chr, 1),
            };
        }
   }
```

на такой:

```rust
    for line in input.lines() {
        let mut counters: HashMap<char, u8> = HashMap::new();

        for chr in line.chars() {
            counters
                .entry(chr)
                .and_modify(|count| { *count += 1})
                .or_insert(1);
        }
    }
```

Так. Пора добивать задачку AOC. Буквы во всех ID я посчитал. Теперь осталось посчитать вот что:

> *...подсчитайте, сколько ID **содержат какую-нибудь букву ровно два раза**, и отдельно — сколько **содержат какую-нибудь букву ровно три раза**. **Перемножив эти два числа**, вы получите \[ответ\]...*

```python
# pseudocode

seen_two_letters = 0
seen_three_letters = 0

for counter in counters
   if counter.values.includes(2)
      seen_two_letters += 1
   if counter.values.include(3)
      seen_three_letters += 1

print seen_two_letters * seen_three_letters
```

Переводим на Rust:

```rust
extern crate utils;
use std::collections::HashMap;

fn part_one() {
    let input = utils::read_puzzle_input(2);
    let mut seen_two_letters_count = 0;
    let mut seen_three_letters_count = 0;

    for line in input.lines() {
        let mut counter: HashMap<char, u8> = HashMap::new();

        for chr in line.chars() {
            counter
                .entry(chr)
                .and_modify(|count| { *count += 1})
                .or_insert(1);
        }

        if counter.values().find(|v| { **v == 2 }).is_some() {
            seen_two_letters_count += 1;
        }

        if counter.values().find(|v| { **v == 3 }).is_some() {
            seen_three_letters_count += 1;
        }
    }

    println!("{}", seen_three_letters_count * seen_two_letters_count);
}
```

Запускаем:

```console
➜  aoc2018 git:(master) ✗ cargo run --bin 2
   Compiling aoc2018 v0.1.0 (file:///Users/antono/Code/rust/aoc2018)
    Finished dev [unoptimized + debuginfo] target(s) in 0.62 secs
     Running `target/debug/2`
5368
```

Ответ принят!

> Ваш ответ: `5368`. Первая половина задачки решена! За неё вы получаете одну золотую звезду: \*

---

[Дисклеймер](@/blog/2018/12/09/aoc-posts-disclaimer/index.ru.md)
