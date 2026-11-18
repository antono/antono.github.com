+++
title = "Iom pri Cargo"
date = 2019-01-05T18:50:22Z
updated = 2019-01-05T18:56:36Z

[taxonomies]
tags = ["rust", "aoc"]

[extra]
lang = "eo"
teletype = "https://blog.antono.info/rJyKtUCbV"
+++
![](0455f396-f4bf-4275-a7e6-85b109d138a1.jpeg)

*Foto de [Philipp Medicus](https://www.flickr.com/photos/p_medicus/) (CC BY-NC 2.0)*

---

> Cargo estas ilo, kiu ebligas al Rust-pakaĵoj deklari siajn diversajn dependaĵojn kaj certigas, ke vi ĉiam ricevos ripeteblan kompilaĵon.

Ĉi-semajne mi malkovris ion interesan pri Cargo.

Unue, ekzistas bone organizita [libro pri Cargo](https://doc.rust-lang.org/cargo/index.html). Mallonga kaj klara teksto. Cargo estas facile komprenebla, se vi jam spertis Bundler de Ruby aŭ npm.

Due, ekzistas [listo de eksteraj subkomandoj de Cargo](https://github.com/rust-lang/cargo/wiki/Third-party-cargo-subcommands). Etendaĵoj, kiuj tre plaĉis al mi:

- [cargo fmt](https://github.com/rust-lang/rustfmt) — por formati la tutan kodon per rustfmt (ilo, kiu formatas Rust-kodon laŭ la stilaj gvidlinioj).
- [cargo count](https://github.com/kbknapp/cargo-count) — por fari statistikon pri la projekto (vidu la ekzemplon sube)
- [cargo-deb](https://github.com/mmstick/cargo-deb), [cargo-rpm](https://github.com/rustrpm/cargo-rpm), [cargo-pkgbuild](https://github.com/kstep/cargo-pkgbuild) — por krei denaskajn pakaĵojn por Linukso
- [cargo-tree](https://github.com/sfackler/cargo-tree) — listigas la arbon de dependaĵoj, same kiel \`npm ls\`
- [cargo-audit](https://github.com/RustSec/cargo-audit) — kontrolas Cargo.lock pri kestoj (crates) kun sekurecaj vundeblecoj

```console
$ cargo install cargo-count
... skip ...
$ cargo count --all --language rs
Gathering information...
         Language  Files  Lines  Blanks  Comments  Code
         --------  -----  -----  ------  --------  ----
         Rust      7      1324   197     423       704
         --------  -----  -----  ------  --------  ----
Totals:            7      1324   197     423       704
```

```console
$ cargo install cargo-tree
... skip ...
$ cargo tree

aoc2018 v0.1.0 (/Users/antono/Code/rust/aoc2018)
├── chrono v0.4.6
│   ├── num-integer v0.1.39
│   │   └── num-traits v0.2.6
│   ├── num-traits v0.2.6 (*)
│   └── time v0.1.41
│       └── libc v0.2.45
│       [dev-dependencies]
│       └── winapi v0.3.6
├── indoc v0.3.1
│   ├── indoc-impl v0.3.1
│   │   ├── proc-macro-hack v0.5.4
│   │   │   ├── proc-macro2 v0.4.24
│   │   │   │   └── unicode-xid v0.1.0
│   │   │   ├── quote v0.6.10
│   │   │   │   └── proc-macro2 v0.4.24 (*)
│   │   │   └── syn v0.15.23
│   │   │       ├── proc-macro2 v0.4.24 (*)
│   │   │       ├── quote v0.6.10 (*)
│   │   │       └── unicode-xid v0.1.0 (*)
│   │   ├── proc-macro2 v0.4.24 (*)
│   │   ├── quote v0.6.10 (*)
│   │   ├── syn v0.15.23 (*)
│   │   └── unindent v0.1.3
│   └── proc-macro-hack v0.5.4 (*)
├── lazy_static v1.2.0
└── regex v1.1.0
    ├── aho-corasick v0.6.9
    │   └── memchr v2.1.2
    │       ├── cfg-if v0.1.6
    │       └── libc v0.2.45 (*)
    │       [build-dependencies]
    │       └── version_check v0.1.5
    ├── memchr v2.1.2 (*)
    ├── regex-syntax v0.6.4
    │   └── ucd-util v0.1.3
    ├── thread_local v0.3.6
    │   └── lazy_static v1.2.0 (*)
    └── utf8-ranges v1.0.2
```
