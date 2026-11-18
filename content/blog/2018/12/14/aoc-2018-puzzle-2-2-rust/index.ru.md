+++
title = "AOC: задача 2.2 на Rust"
date = 2018-12-14T23:45:07Z
updated = 2022-04-15T11:56:10Z

[taxonomies]
tags = ["rust"]

[extra]
lang = "ru"
teletype = "https://blog.antono.info/aoc-2018-puzzle-2.2-rust"
+++
Входные данные [те же, что и в 2.1](https://github.com/antono/aoc2018/blob/master/inputs/2.txt). На этот раз нужно найти идентификаторы, которые отличаются ровно одной буквой в одной и той же позиции:

> Идентификаторы abcde и axcye похожи, но отличаются двумя символами (вторым и четвёртым). А вот идентификаторы fghij и fguij отличаются ровно одним символом — третьим (h и u). Это и есть нужные коробки.

> Какие буквы совпадают у идентификаторов двух нужных коробок?

Чтобы сравнить идентификаторы, я по очереди заменяю в каждом из них по одному символу на 0 (его нет в исходном алфавите) и использую результаты замены как ключи хеша, а исходные идентификаторы складываю в значения по этим ключам.

Псевдокод решения:

```rust
ids = get_input_ids
hash = {}

for original_id in ids
  for id_with_1_char_replaced in combinations_with_1_char_replaced(original_id)
    hash[id_with_1_chars_replaced].push(original_id)

solution = hash.values.find { |arr| arr.any? }

def combinations_with_1_char_replaced(original)
    result = []

    original.len.times |idx|
         id_as_array = original.clone()
         id_as_array[idx0] = 0
         result.push(id_as_array.join)

    return result
```

Решение на Rust:

```rust
use std::char;

fn part_two() {
    let input = utils::read_puzzle_input(2);
    let mut results: HashMap<String, Vec<_>> = HashMap::new();
    let mut lines_count = 0;
    let mut ids_count = 0;

    for id in input.lines() {
        let ids = all_valiants_with_1_letter_replaced(id);

        lines_count += 1;

        for id_changed in ids {
            ids_count += 1;
            results.entry(id_changed)
                .and_modify(|vec| vec.push(id.clone()))
                .or_insert(vec!(id));
        }
    }

    let mut res = vec!();

    for (matcher, ids) in &results {
        if ids.len() > 1 {
            res.push((matcher.clone(), ids.clone()));
        }
    }

    println!("{}", "-".repeat(100));

    for tup in &res {
        println!("{:?}", tup);
    }

    println!("{}", "-".repeat(100));

    println!("Res.len: {:?}", res.len());
    println!("Keys: {}", results.keys().len());
    println!("Values: {}", results.values().fold(0, |acc, arr| acc + arr.len()));
    println!("Lines: {}, ids: {}", lines_count, ids_count);
}


fn all_valiants_with_1_letter_replaced(id: &str) -> Vec<String> {
    let mut result: Vec<String> = vec!();
    let id_map = id.chars().collect::<Vec<char>>();
    let size = id.len();

    for idx in 0..size {
        let mut cur_map = id_map.clone();
        cur_map[idx] = '0';
        result.push(cur_map.into_iter().collect());
    }

    return result;
}
```

Запускаем:

```console
➜  aoc2018 git:(master) ✗ cargo run --bin 2
warning: unused manifest key: package.edition
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/2`
----------------------------------------------------------------------------------------------------
("cvgywxqubnuaefmsl0jdrpfzyi", ["cvgywxqubnuaefmsldjdrpfzyi", "cvgywxqubnuaefmslkjdrpfzyi"])
----------------------------------------------------------------------------------------------------
Res.len: 1
Keys: 6499
Values: 6500
Lines: 250, ids: 6500
```

---

> Какие буквы совпадают у идентификаторов двух нужных коробок?

Убираем 0 из ключа хеша: «cvgywxqubnuaefmsljdrpfzyi». Отправляем.

> Ваш ответ: `cvgywxqubnuaefmsljdrpfzyi`. Обе части задачи решены! За них полагаются две золотые звезды: \*\*

[Код](https://github.com/antono/aoc2018)

---

[Дисклеймер](@/blog/2018/12/09/aoc-posts-disclaimer/index.ru.md)
