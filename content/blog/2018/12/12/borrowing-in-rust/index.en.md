+++
title = "Borrowing in Rust"
date = 2018-12-12T13:32:45Z
updated = 2018-12-18T23:07:19Z
aliases = ["/rJlqpIRJ4/"]

[taxonomies]
tags = ["rust", "aoc"]

[extra]
lang = "en"
teletype = "https://blog.antono.info/rJlqpIRJ4"
+++
![](82fbe53d-9aae-4cdf-b1fc-5ce5800367a2.jpeg)

Doing [puzzle #2 of advent of code](https://adventofcode.com/2018/day/2) challenge in Rust. The puzzle is pretty simple. Input looks like this:

```text
mvgowxqubnhaefjslkjlrptzyi
pvgowlqubnhaefmslkjdrpteyi
ovgowoqubnhaefmslkjnrptzyi
cvgowxqubnrxefmslkjdrptzyo
cvgowxqubnhaefmsokjdrprzyf
cvgowxqubnhjeflslkjgrptzyi
...
```

The task is:

> ...count the number that have an ID **containing exactly two of any letter** and then separately count those with **exactly three of any letter**. You can **multiply those two counts together** to get \[an answer\]...

Pseudocode solution would look like:

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

Let's do it in rust. Without much optimization i going to use vector fo [HashMap](https://doc.rust-lang.org/std/collections/struct.HashMap.html)s to store char counts for each line. Then iterate over them and count hashes having 2 or 3 among values.

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

Running the code:

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

Re-reading topic on [ownership](https://doc.rust-lang.org/1.11.0/book/ownership.html) and [borrowing](https://doc.rust-lang.org/1.11.0/book/references-and-borrowing.html) from Rust Book. The concept of ownership looks clear to me. Borrowing and mutable borrowing was not. For proper borrowing one should obey some rules:

> First, any borrow must last for a scope no greater than that of the owner. *Second, you may have one or the other of these two kinds of borrows, but not both at the same time:* one or more references (`&T`) to a resource, **exactly one mutable reference** (`&mut T`).

So the problem is that i borrowed counters hash map for both reading and writing. Since HashMap#get returns an Option with reference to the value (stored in heap). At the same time counter.insert() borrowing hash data as mutable in order to modify hash data (in heap). Rust denies this in order to guarantee memory safety and avoid race conditions:

> Ownership is how Rust achieves its largest goal, memory safety.

So one of approaches is to avoid borrowing hash value for reading is just copy the value. Documentation for Option gives helpful [.cloned()](https://doc.rust-lang.org/std/option/enum.Option.html#method.cloned) method.

> Maps an `Option<&T>` to an `Option<T>` by cloning the contents of the option.

I'll use the method when getting hash value:

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

Running the code:

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

It worked. The only thing is i doing copy of value each time i need to avoid read only borrowing. One smart person suggested me to use [HashMap#entry()](https://doc.rust-lang.org/std/collections/struct.HashMap.html#method.entry) in order to get hash Entry for in place modification. Entry itself has a lot of useful methods. [Entry#and_modify()](https://doc.rust-lang.org/std/collections/hash_map/enum.Entry.html#method.and_modify) looks exactly what i need. Examples from docs:

```rust
use std::collections::HashMap;

let mut map: HashMap<&str, u32> = HashMap::new();

map.entry("poneyland")
   .and_modify(|e| { *e += 1 })
   .or_insert(42);

assert_eq!(map["poneyland"], 42);
```

Wow. I'll change my code a from this:

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

to this:

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

Ok. Time to finish the AOC puzzle. I counted all letters in all ids. Now i need count:

> *...count the number that have an ID **containing exactly two of any letter** and then separately count those with **exactly three of any letter**. You can **multiply those two counts together** to get \[an answer\]...*

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

Converting to rust:

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

Running:

```console
➜  aoc2018 git:(master) ✗ cargo run --bin 2
   Compiling aoc2018 v0.1.0 (file:///Users/antono/Code/rust/aoc2018)
    Finished dev [unoptimized + debuginfo] target(s) in 0.62 secs
     Running `target/debug/2`
5368
```

The number accepted!

> Your puzzle answer was `5368`. The first half of this puzzle is complete! It provides one gold star: \*

---

[Disclaimer](@/blog/2018/12/09/aoc-posts-disclaimer/index.en.md)
