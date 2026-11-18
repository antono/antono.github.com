+++
title = "Advent of Code per Rust"
date = 2018-12-09T17:35:42Z
updated = 2022-04-15T12:13:00Z

[taxonomies]
tags = ["rust"]

[extra]
lang = "eo"
teletype = "https://blog.antono.info/rysyH35JN"
+++
![](750cae79-3911-480a-aebb-32aaa4d35549.jpeg)

*Foto de [Paul VanDerWerf](https://www.flickr.com/photos/pavdw/) ([CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)), tondita.*

---

## Instigo

Iu [saĝa homo](https://github.com/onesk) instigis min aliĝi al la defio [Advent of Code](https://adventofcode.com/).

Ĉi tie mi priskribos mian vojaĝon en la programlingvon Rust. La celo de ĉi tiuj blogaĵoj estas pli bone kompreni Rust per tio, ke mi notas miajn ekkomprenojn. Publika verkado igas min pli respondeca: ĝi devigas min dufoje pripensi kaj legi pli da dokumentaro antaŭ ol publikigi, por aspekti malpli stulta ol mi fakte estas.

Mi havas bazan sperton pri Rust — faris kelkajn etajn eksperimentojn por mi mem. Teorie, antaŭ ĉirkaŭ unu jaro mi legis la ĉapitrojn de [The Rust Book](https://doc.rust-lang.org/book/), kiuj interesis min.

Ĉi tiu afiŝo priskribas ĉiujn paŝojn, kiujn mi faris por ekiri. La sekvaj afiŝoj verŝajne enhavos malpli da instrukcioj kaj pli da personaj observoj pri Rust.

---

## Strukturo de la projekto

Unue mi instalis Rust per la ilo [rustup](https://rustup.rs/). Unu simpla komando, kaj mi havas ĉion bezonatan.

Poste mi generis novan projekton per la bonega ilo [cargo](https://doc.rust-lang.org/cargo/):

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

Cargo estas la enkonstruita pakaĵadministrilo kaj muntilo de Rust. Ĝi kapablas pli ol aliaj pakaĵadministriloj, kiujn mi uzis (gem, bundler, npm, pip). Jen nekompleta listo de taskoj, kiujn cargo povas fari por vi:

- Generi novan projekton
- Munti vian projekton kaj ruli testojn
- Administri la dependaĵojn de la projekto, difinitajn en Cargo.toml
- Publikigi vian pakaĵon ĉe [crates.io](https://crates.io/)
- Formati vian kodon

Aliaj lingvoj havas apartajn ilojn por ĉiuj ĉi taskoj, sed la aliro de la Rust-teamo ege faciligas la komencon, sen la tuta ĝeno pri multaj apartaj eroj.

La defaŭlte generita kodo estas programo „Hello World“, kaj ruli ĝin estas tiel facile:

```console
cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/aoc2018`
Hello, world!
```

Nun mi ŝanĝos la strukturon de la projekto, por ke ĉiu enigmo havu sian propran plenumeblan dosieron.

La [sekcio pri strukturo de projekto](https://doc.rust-lang.org/cargo/guide/project-layout.html) en la Cargo Book diras, ke plenumeblaj programoj loĝu en src/bin/\*.rs.

Reorganizo de la projekto:

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

## Enigmo n-ro 1

Jam tempas ekkodi.

Mallonge: vi ricevas liston de nombroj, po unu en linio, ĉiu kun antaŭa plus- aŭ minus-signo. La solvo estas ilia sumo. La enigo aspektas jene:

```text
+13
+9
+8
+1
-15
+10
...
```

Mi metis ĉi tiun enigon en inputs/1.txt en la radiko de la projekto. Ĉiujn enigojn mi metos en tiun dosierujon, do mi volas krei universalan funkcion por legi tiujn dosierojn. Mi estas tro pigra por legi la API-dokumentaron, sed guglo montras [bonan ekzemplon el la Rust Book](https://doc.rust-lang.org/1.30.0/book/second-edition/ch12-02-reading-a-file.html).

Mi alĝustigas la ekzemplon al miaj bezonoj:

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

Bone. Nun mi trairos la liniojn, analizos ilin kaj sumos. Feliĉe String en Rust havas enkonstruitan [metodon *lines()*](https://doc.rust-lang.org/std/string/struct.String.html#method.lines). Ĝi redonas [iteratoron Lines](https://doc.rust-lang.org/std/str/struct.Lines.html), uzeblan en cikloj:

```rust
fn main() {
    let input = read_puzzle_input(1);

    for line in input.lines() {
        println!("{}", result);
    }
}
```

Tio estis facila. Nun pri la analizo de la nombroj. Mia unua ideo estis preni la signon el la pozicio 0 de ĉiu linio kaj analizi la reston de la ĉeno kiel entjeron. Poste, per la [ŝlosilvorto match](https://doc.rust-lang.org/rust-by-example/flow_control/match.html), aŭ aldoni ĝin al iu variablo aŭ subtrahi ĝin de ĝi. Sed kiam mi provis analizi la entjerojn, mi trovis, ke Rust havas la metodon [str::parse](https://doc.rust-lang.org/std/primitive.str.html#method.parse), kiu konvertas ĉenojn al aliaj tipoj. Eĉ pli facile ol mi pensis!

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

Rulado de la kodo:

```console
 cargo run
   Compiling aoc2018 v0.1.0 (file:///Users/antono/Code/rust/aoc2018)
    Finished dev [unoptimized + debuginfo] target(s) in 0.92 secs
     Running `target/debug/1`
493
```

Funkcias. La rezulto estis akceptita, kaj mi ricevis mian unuan stelon en la defio.

Mojose!

Mia [kodo estas publikigita ĉe GitHub](https://github.com/antono/aoc2018), se iun interesas.

---

## Esplorindaĵoj

Kelkajn aferojn en la kodo mi ankoraŭ devas klarigi al mi mem.

File::open() kaŭzas kompilan eraron sen .expect()

```rust
File::open(filename).expect("error message");
```

La funkcio parse kaŭzas kompilan eraron sen voko de .unwrap().

```rust
line.parse::<i32>().unwrap();
```

La uzo de File ŝajnas evidenta, sed kial mi bezonas prelude?

```rust
use std::fs::File;
use std::io::prelude::*;
```

La respondojn mi priskribos en miaj venontaj afiŝoj.

---

[Averto](@/blog/2018/12/09/aoc-posts-disclaimer/index.eo.md)
