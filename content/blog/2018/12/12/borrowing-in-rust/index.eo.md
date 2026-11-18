+++
title = "Pruntado en Rust"
date = 2018-12-12T13:32:45Z
updated = 2018-12-18T23:07:19Z

[taxonomies]
tags = ["rust", "aoc"]

[extra]
lang = "eo"
teletype = "https://blog.antono.info/rJlqpIRJ4"
+++
![](82fbe53d-9aae-4cdf-b1fc-5ce5800367a2.jpeg)

Mi solvas per Rust [la duan enigmon de Advent of Code](https://adventofcode.com/2018/day/2). La enigmo estas sufiĉe simpla. La enigo aspektas jene:

```text
mvgowxqubnhaefjslkjlrptzyi
pvgowlqubnhaefmslkjdrpteyi
ovgowoqubnhaefmslkjnrptzyi
cvgowxqubnrxefmslkjdrptzyo
cvgowxqubnhaefmsokjdrprzyf
cvgowxqubnhjeflslkjgrptzyi
...
```

La tasko:

> ...kalkulu, kiom da identigiloj **enhavas iun ajn literon ekzakte dufoje**, kaj aparte kalkulu tiujn, kiuj **enhavas iun ajn literon ekzakte trifoje**. **Multiplikinte tiujn du nombrojn**, vi ricevos \[la respondon\]...

Per pseŭdokodo la solvo aspektus proksimume jene:

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

Nun en Rust. Sen speciala optimumigo mi konservos la nombrojn de signoj en ĉiu linio en vektoro de [HashMap](https://doc.rust-lang.org/std/collections/struct.HashMap.html)-oj. Poste mi trairos ilin kaj kalkulos la haŝtabelojn, kiuj havas 2 aŭ 3 inter siaj valoroj.

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

Mi lanĉas la kodon:

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

Mi relegas en la Rust Book la ĉapitrojn pri [posedo](https://doc.rust-lang.org/1.11.0/book/ownership.html) kaj [pruntado](https://doc.rust-lang.org/1.11.0/book/references-and-borrowing.html). La koncepto de posedo ŝajnis al mi klara. Sed pruntado, des pli ŝanĝebla pruntado, ne tiom. Por ĝuste prunti, oni devas obei kelkajn regulojn:

> Unue, ĉiu prunto devas daŭri ne pli longe ol la videbleca amplekso (scope) de la posedanto. *Due, vi povas havi aŭ unu aŭ la alian el tiuj du specoj de pruntoj, sed ne ambaŭ samtempe:* unu aŭ plurajn referencojn (`&T`) al rimedo, aŭ **ekzakte unu ŝanĝeblan referencon** (`&mut T`).

Do la problemo estas, ke mi pruntis la haŝtabelon counters samtempe por legado kaj por skribado. HashMap#get ja redonas Option kun referenco al la valoro (kiu troviĝas en la amaso, angle *heap*). Samtempe counter.insert() pruntas la datumojn de la haŝtabelo kiel ŝanĝeblajn, por modifi ilin (ankaŭ en la amaso). Rust tion malpermesas por garantii memorsekurecon kaj eviti konkurkondiĉojn (race conditions):

> Posedo estas la maniero, per kiu Rust atingas sian plej grandan celon: memorsekurecon.

Unu el la manieroj eviti pruntadon de la valoro por legado estas simple kopii ĝin. La dokumentaro de Option proponas la utilan metodon [.cloned()](https://doc.rust-lang.org/std/option/enum.Option.html#method.cloned).

> Transformas `Option<&T>` en `Option<T>`, klonante la enhavon de la Option.

Mi uzos tiun metodon, kiam mi prenas valoron el la haŝtabelo:

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

Mi lanĉas la kodon:

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

Funkcias! La sola ĝeno: mi devas ĉiufoje kopii la valoron nur por eviti nurlegan pruntadon. Iu saĝulo konsilis al mi uzi [HashMap#entry()](https://doc.rust-lang.org/std/collections/struct.HashMap.html#method.entry), kiu donas Entry por modifi la valoron en la haŝtabelo surloke. Entry mem havas multajn utilajn metodojn. [Entry#and_modify()](https://doc.rust-lang.org/std/collections/hash_map/enum.Entry.html#method.and_modify) ŝajnas ĝuste tio, kion mi bezonas. Ekzemplo el la dokumentaro:

```rust
use std::collections::HashMap;

let mut map: HashMap<&str, u32> = HashMap::new();

map.entry("poneyland")
   .and_modify(|e| { *e += 1 })
   .or_insert(42);

assert_eq!(map["poneyland"], 42);
```

Ŭaŭ! Mi ŝanĝas mian kodon de ĉi tio:

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

al ĉi tio:

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

Bone. Estas tempo fini la AOC-enigmon. Mi kalkulis ĉiujn literojn en ĉiuj identigiloj. Nun restas kalkuli jenon:

> *...kalkulu, kiom da identigiloj **enhavas iun ajn literon ekzakte dufoje**, kaj aparte kalkulu tiujn, kiuj **enhavas iun ajn literon ekzakte trifoje**. **Multiplikinte tiujn du nombrojn**, vi ricevos \[la respondon\]...*

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

Nun la sama en Rust:

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

Lanĉo:

```console
➜  aoc2018 git:(master) ✗ cargo run --bin 2
   Compiling aoc2018 v0.1.0 (file:///Users/antono/Code/rust/aoc2018)
    Finished dev [unoptimized + debuginfo] target(s) in 0.62 secs
     Running `target/debug/2`
5368
```

La nombro estas akceptita!

> Via respondo estis `5368`. La unua duono de la enigmo estas solvita! Ĝi donas unu oran stelon: \*

---

[Averto](@/blog/2018/12/09/aoc-posts-disclaimer/index.eo.md)
