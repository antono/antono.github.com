+++
title = "AOC: Enigmo 2.2 en Rust"
date = 2018-12-14T23:45:07Z
updated = 2022-04-15T11:56:10Z

[taxonomies]
tags = ["rust"]

[extra]
lang = "eo"
teletype = "https://blog.antono.info/aoc-2018-puzzle-2.2-rust"
+++
La enigo estas [la sama kiel por 2.1](https://github.com/antono/aoc2018/blob/master/inputs/2.txt). Ĉi-foje mi devas trovi identigilojn, kiuj diferencas per unu litero en la sama pozicio:

> La identigiloj abcde kaj axcye estas proksimaj, sed ili diferencas per du signoj (la dua kaj la kvara). Tamen la identigiloj fghij kaj fguij diferencas per ĝuste unu signo, la tria (h kaj u). Tiuj devas esti la ĝustaj skatoloj.

> Kiuj literoj estas komunaj al la identigiloj de la du ĝustaj skatoloj?

Por kompari la identigilojn, mi laŭvice anstataŭigas po unu signo en ĉiu el ili per 0 (kiu ne apartenas al la originala alfabeto) kaj uzas la rezultojn de la anstataŭigo kiel ŝlosilojn de haŝtabelo, konservante la originalajn identigilojn kiel valorojn de la ŝlosilo.

Pseŭdokodo de la solvo:

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

Solvo en Rust:

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

Rulado de la kodo:

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

> Kiuj literoj estas komunaj al la identigiloj de la du ĝustaj skatoloj?

Mi forigas la 0-on el la ŝlosilo: „cvgywxqubnuaefmsljdrpfzyi“. Kaj sendas.

> Via respondo al la enigmo estis `cvgywxqubnuaefmsljdrpfzyi`. Ambaŭ partoj de ĉi tiu enigmo estas solvitaj! Ili donas du orajn stelojn: \*\*

[La kodo](https://github.com/antono/aoc2018)

---

[Averto](@/blog/2018/12/09/aoc-posts-disclaimer/index.eo.md)
