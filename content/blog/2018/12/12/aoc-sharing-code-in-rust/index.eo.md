+++
title = "AOC: Reuzado de kodo en Rust"
date = 2018-12-12T10:56:19Z
updated = 2018-12-12T11:12:21Z

[taxonomies]
tags = ["rust", "aoc"]

[extra]
lang = "eo"
teletype = "https://blog.antono.info/rkoLYw01V"
+++
Post la unua enigmo de Advent of Code mi trovis funkcion, kiun indas reuzi:

```
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

Mi intencas movi tiun funkcion al aparta dosiero kaj poste iel reuzi ĝin en [ĉiuj miaj solvoj](https://github.com/antono/aoc2018). Rapida guglado kondukas al la ĉapitro „[Using Modules to Reuse and Organize Code](https://doc.rust-lang.org/1.30.0/book/second-edition/ch07-00-modules.html)“ de The Rust Book.

> Kio okazas, se vi havas tro da funkcioj? Rust havas modulsistemon, kiu ebligas reuzi kodon en ordigita maniero.

Bonege! Du gravaj aferoj jam el la unua paĝo:

- Defaŭlte funkcioj, tipoj, konstantoj kaj moduloj estas privataj. La ŝlosilvorto `pub` igas eron publika kaj do videbla ekster ĝia nomspaco.
- La ŝlosilvorto `use` enkondukas modulojn, aŭ la difinojn ene de moduloj, en la videblecan amplekson (scope), por ke estu pli facile referenci ilin.

Rust permesas sufiĉe flekseblan aranĝon de moduloj, kaj ekzistas kelkaj reguloj pri ilia organizado. Por mia simpla kazo mi faris nur jenajn paŝojn:

1. Movis la funkcion al aparta dosiero \`src/utils.rs\`
2. aldonis antaŭ la funkcio la ŝlosilvorton pub: pub fn read_puzzle_input...
3. kaj aldonis etan fragmenton al Cargo.toml:

```
[lib]
name = "utils"
path = "src/utils.rs"
```

Nun, por uzi funkciojn el tiu biblioteko, mi devas aldoni deklaron de la kesto (crate) komence de mia dosiero kaj antaŭmeti la nomspacon utils al la funkcivoko:

```
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

[La kodo](https://github.com/antono/aoc2018).

---

[Averto](@/blog/2018/12/09/aoc-posts-disclaimer/index.eo.md)
