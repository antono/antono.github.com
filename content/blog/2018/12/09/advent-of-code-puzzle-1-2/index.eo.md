+++
title = "Advent of Code: enigmo 1.2"
date = 2018-12-09T22:52:40Z
updated = 2022-04-15T11:55:32Z

[taxonomies]
tags = ["rust"]

[extra]
lang = "eo"
teletype = "https://blog.antono.info/rkbphGsyE"
+++
![](00327ce5-8ff5-4ef9-9f8e-39a7c2e193fd.jpeg)

*Foto de [Kevin Utting](https://www.flickr.com/photos/tallkev/) ([CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)), tondita.*

---

Mi solvas la duan parton de la unua tago de la defio [Advent of Code](https://adventofcode.com/). La enigmo baziĝas sur [la unua parto de la unua tago](@/blog/2018/12/09/advent-of-code-in-rust/index.eo.md).

La tasko estas:

> Vi rimarkas, ke la aparato ripetas la saman liston de frekvencoŝanĝoj denove kaj denove. Por kalibri la aparaton, vi devas trovi la unuan frekvencon, kiun ĝi atingas dufoje.

Do ni rigardu la solvon [el la unua parto](@/blog/2018/12/09/advent-of-code-in-rust/index.eo.md):

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

La tasko ŝajnas facila: mi nur kolektu la rezultojn kaj trovu la unuan ripeton! La unua ideo estas uzi tabelon kaj ĉe ĉiu iteracio kontroli, ĉu ĝi jam enhavas la nunan rezulton. Sed serĉo en tabelo havas komplikecon O(n), kaj tio malrapidigos la kodon, se necesos tre multaj iteracioj. Haktabelo eble pli taŭgas ĉi tie, kun alira komplikeco O(1). Tamen haŝtabelo devas teni ian valoron por ĉiu ŝlosilo, kio ne necesas por mia tasko. Do mi bezonas ian kolekton kun malmultekostaj enmetoj kaj kontroloj de aneco. Ni vidu, kion Rust proponas en sia norma biblioteko: [kolektoj](https://doc.rust-lang.org/beta/std/collections/).

Rust havas 4 ĉefajn kategoriojn de kolektoj:

- Sekvencoj: [`Vec`](https://doc.rust-lang.org/beta/std/vec/struct.Vec.html), [`VecDeque`](https://doc.rust-lang.org/beta/std/collections/struct.VecDeque.html), [`LinkedList`](https://doc.rust-lang.org/beta/std/collections/struct.LinkedList.html)
- Mapoj: [`HashMap`](https://doc.rust-lang.org/beta/std/collections/struct.HashMap.html), [`BTreeMap`](https://doc.rust-lang.org/beta/std/collections/struct.BTreeMap.html)
- Aroj: [`HashSet`](https://doc.rust-lang.org/beta/std/collections/struct.HashSet.html), [`BTreeSet`](https://doc.rust-lang.org/beta/std/collections/struct.BTreeSet.html)
- Diversaj: [`BinaryHeap`](https://doc.rust-lang.org/beta/std/collections/struct.BinaryHeap.html)

La dokumentaro estas sufiĉe bona kaj klarigas la avantaĝojn kaj malavantaĝojn de ĉiu tipo…

> [Uzu la `Set`-varianton de iu ajn el ĉi tiuj `Map`-oj, kiam:](https://doc.rust-lang.org/beta/std/collections/#use-the-set-variant-of-any-of-these-maps-when)

> Vi nur volas memori, kiujn ŝlosilojn vi jam vidis.

> Ne ekzistas signifoplena valoro asociinda al viaj ŝlosiloj.

> Vi simple volas aron.

Ŝajnas ĝuste tio, kion mi bezonas. Estas [BTreeSet](https://doc.rust-lang.org/beta/std/collections/struct.BTreeSet.html) kaj [HashSet](https://doc.rust-lang.org/beta/std/collections/struct.HashSet.html). Mi kredas, ke la dua estas malpli multekosta por enmetoj, do mi uzos ĝin.

```rust
fn part_two() {
    let input = read_puzzle_input(1);
    let mut result: i32 = 0;
    let mut seen_freqs: HashSet<i32> = HashSet::new();

    seen_freqs.insert(result);

    for line in input.lines() {
        let num = line.parse::<i32>().unwrap();
        result += num;

        if !seen_freqs.insert(result) {
            println!("Repeating frequency: {}", result);
            break
        }
    }
}
```

Esence la sama laboro kiel antaŭe, sed ĉi-foje ĉiu rezulto estas enmetata en [HashSet](https://doc.rust-lang.org/beta/std/collections/struct.HashSet.html). La metodo insert redonas la bulean valoron false, se la valoro jam estas en la aro.

Mi rulas tion kaj ricevas nenian eligon.

Nekredeble! Mi aldonas sencimigan eligon (po unu rezulto en linio) kaj komparas per ŝelaj iloj:

```shell
cargo run > nums.txt
wc -l nums.txt
989 nums.txt
uniq nums.txt > nums2.txt
wc -l nums2.txt
989 nums2.txt
```

Ŝajnas, ke la nombro de unikaj valoroj estas la sama: neniuj ripetoj. Mi atente relegas la taskon kaj vidas ion, kion mi preteratentis la unuan fojon:

> Notu, ke via aparato eble devos ripeti sian liston de frekvencoŝanĝoj multfoje, antaŭ ol trovi ripetiĝantan frekvencon, kaj ke ripeto povas troviĝi meze de la traktado de la listo.

Bone. Tio signifas, ke mi devas trairi la liniojn denove kaj atendi ripetiĝantan nombron. Sed input.lines() redonas la strukturon Lines, kiu estas iteratoro, do atinginte la finon de la sekvenco, ĝi haltos. Mia unua ideo estis konverti la iteratoron al listo kaj poste uzi la bonan malnovan senfinan ciklon kun manipulado de indeksoj + rompi la ciklon, tuj kiam la valoro troviĝas. Tamen, fosinte en la dokumentaro pri iteratoroj, mi trovis manieron rekomencigi iteratoron: [std::iter::iterator#cycle](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.cycle). input.lines() redonas [strukturon Lines, kiu realigas la trajton (trait) Iterator](https://doc.rust-lang.org/std/str/struct.Lines.html). Tio verŝajne signifas, ke mi povas uzi cycle() por senfine trairi la valorojn.

Mi aldonas vokon de .cycle() al Lines:

```rust
fn part_two() {
    let input = read_puzzle_input(1);
    let mut result: i32 = 0;
    let mut seen_freqs: HashSet<i32> = HashSet::new();

    seen_freqs.insert(result);

    for line in input.lines().cycle() {
        let num = line.parse::<i32>().unwrap();
        result += num;

        if !seen_freqs.insert(result) {
            println!("Repeating frequency: {}", result);
            break
        }
    }
}
```

Rulado de la kodo:

```
cargo run
   Compiling aoc2018 v0.1.0 (file:///Users/antono/Code/rust/aoc2018)
    Finished dev [unoptimized + debuginfo] target(s) in 0.62 secs
     Running `target/debug/1`
Sum of freq adjustments: 493
Repeating frequency: 413
```

Sendo de la rezulto:

> Jen la ĝusta respondo! Vi estas je unu ora stelo pli proksima al riparo de la tempofluo.

La kodo estas puŝita al GitHub.

---

## Lecionoj

- Legu la postulojn atente :)
- Kapabloj pri Unikso-ŝelo ankoraŭ utilas
- Ĉio, kion mi bezonas scii [pri iteratoroj en Rust, sur unu paĝo](https://doc.rust-lang.org/std/iter/index.html)

---

[Averto](@/blog/2018/12/09/aoc-posts-disclaimer/index.eo.md)
