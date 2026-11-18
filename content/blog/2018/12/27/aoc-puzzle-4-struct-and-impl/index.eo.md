+++
title = "AOC: Enigmo 4: struct kaj impl"
date = 2018-12-27T22:40:36Z
updated = 2022-01-25T14:56:51Z

[taxonomies]
tags = ["rust"]

[extra]
lang = "eo"
teletype = "https://blog.antono.info/r1TJSAGbV"
+++
[AVERTO](@/blog/2018/12/09/aoc-posts-disclaimer/index.eo.md)

Ĉiufoje, [solvante la enigmojn de Advent of Code](https://github.com/antono/aoc2018), mi fosas en iun interesan temon. Ĉi-foje temis pri strukturoj en Rust kaj pri la realigo de metodoj por strukturoj.

Por sekvi la deĵorojn de la gardisto ([vidu la detalojn de la enigmo](https://github.com/antono/aoc2018/blob/master/src/bin/4.rs#L1)) mi enkondukis la strukturon ShiftTimeline:

```rust
struct ShiftTimeline {
    data: Vec<u32>,
}
```

La ideo estis konservi en vektoro la minutojn, dum kiuj la gardisto dormis.

> *Strukturo* (*struct*) estas propra datumtipo, kiu ebligas nomi kaj kunpaki plurajn rilatajn valorojn, kiuj kune formas signifoplenan grupon. Se vi konas objektemajn lingvojn, *strukturo* similas al la datumaj atributoj de objekto. En ĉi tiu ĉapitro ni komparos opojn kun strukturoj kaj montros la diferencojn, montros kiel uzi strukturojn kaj diskutos kiel difini metodojn kaj asociitajn funkciojn por precizigi la konduton ligitan al la datumoj de strukturo. Strukturoj kaj enumeracioj (pritraktitaj en la 6-a ĉapitro) estas la konstrubrikoj por krei novajn tipojn en la fakdomajno de via programo, por plene profiti de la tipkontrolado de Rust dum kompilado.

Komence mi intencis aldoni pliajn kampojn, sed finfine lasis nur unu. Ne multe sencas teni strukturon por unu sola kampo... Sed mi decidis konservi ĝin por grupigi metodojn ĉirkaŭ ĝi. Legante [la libron pri Rust, ĉapitron pri metodoj](https://doc.rust-lang.org/1.30.0/book/second-edition/ch05-03-method-syntax.html):

> *Metodoj* similas al funkcioj: oni deklaras ilin per la ŝlosilvorto `fn` kaj ilia nomo, ili povas havi parametrojn kaj revenan valoron, kaj ili enhavas kodon, kiu ruliĝas, kiam oni vokas ilin de ie alie. Tamen metodoj diferencas de funkcioj per tio, ke ili estas difinitaj en la kunteksto de strukturo, kaj ilia unua parametro ĉiam estas `self`, kiu reprezentas la ekzempleron de la strukturo, por kiu la metodo estas vokata.

Uzante la strukturon ShiftTimeline, mi rimarkis ripetiĝantan kodon por pravalorizi la datumojn:

```rust
let timeline = ShiftTimeline { data: Vec::new() };
```

Do mi realigis simplan pravalorizilon:

```rust
struct ShiftTimeline {
    data: Vec<u32>,
}

impl ShiftTimeline {
    fn new() -> ShiftTimeline {
        ShiftTimeline { data: Vec::new() }
    }
}
```

Nun eblas uzi ShiftTimeline::new() por ricevi la kampon jam pravalorizita. Kaj ankoraŭ unu metodo, kiu akceptas referencon al self kun skribrajto al la kampoj de la strukturo:

```rust
impl ShiftTimeline {

    ...

    fn record_sleep_time(&mut self, asleep_at: NaiveDateTime, awake_at: NaiveDateTime) {
       let start_min = asleep_at_time.minute();
       let end_min = awake_at.minute();
       for idx in start_min..end_min {
           self.data.push(idx);
       }
    }
}

...

shift_timeline.record_sleep_time(...)
```
