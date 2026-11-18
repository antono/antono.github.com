+++
title = "Кое-что о Cargo"
date = 2019-01-05T18:50:22Z
updated = 2019-01-05T18:56:36Z

[taxonomies]
tags = ["rust", "aoc"]

[extra]
lang = "ru"
teletype = "https://blog.antono.info/rJyKtUCbV"
+++
![](0455f396-f4bf-4275-a7e6-85b109d138a1.jpeg)

*Фото: [Philipp Medicus](https://www.flickr.com/photos/p_medicus/) (CC BY-NC 2.0)*

---

> Cargo — это инструмент, который позволяет пакетам Rust объявлять свои зависимости и гарантирует, что сборка всегда будет воспроизводимой.

На этой неделе я узнал о Cargo кое-что интересное.

Во-первых, есть хорошо структурированная [книга по Cargo](https://doc.rust-lang.org/cargo/index.html). Коротко и понятно. Если вы раньше работали с Bundler из Ruby или с npm, в Cargo разберётесь без труда.

Во-вторых, есть [список сторонних подкоманд Cargo](https://github.com/rust-lang/cargo/wiki/Third-party-cargo-subcommands). Расширения, которые мне очень понравились:

- [cargo fmt](https://github.com/rust-lang/rustfmt) — форматирует весь код с помощью rustfmt (инструмента, который приводит код на Rust в соответствие с рекомендациями по стилю).
- [cargo count](https://github.com/kbknapp/cargo-count) — собирает статистику по проекту (пример ниже)
- [cargo-deb](https://github.com/mmstick/cargo-deb), [cargo-rpm](https://github.com/rustrpm/cargo-rpm), [cargo-pkgbuild](https://github.com/kstep/cargo-pkgbuild) — для сборки нативных пакетов под Linux
- [cargo-tree](https://github.com/sfackler/cargo-tree) — выводит дерево зависимостей, прямо как \`npm ls\`
- [cargo-audit](https://github.com/RustSec/cargo-audit) — проверяет Cargo.lock на крейты с известными уязвимостями

```
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

```
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
