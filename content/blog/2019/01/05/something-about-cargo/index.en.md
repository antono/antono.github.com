+++
title = "Something about Cargo"
date = 2019-01-05T18:50:22Z
updated = 2019-01-05T18:56:36Z
aliases = ["/rJyKtUCbV/"]

[taxonomies]
tags = ["rust", "aoc"]

[extra]
lang = "en"
teletype = "https://blog.antono.info/rJyKtUCbV"
+++
![](0455f396-f4bf-4275-a7e6-85b109d138a1.jpeg)

*Photo by [Philipp Medicus](https://www.flickr.com/photos/p_medicus/) (CC BY-NC 2.0)*

---

> Cargo is a tool that allows Rust packages to declare their various dependencies and ensure that you’ll always get a repeatable build.

This week i found something interesting about cargo.

First there is a well organized [cargo book](https://doc.rust-lang.org/cargo/index.html). Short and clear text. Cargo is easy to understand if you have ruby bundler or npm background.

Second: there is a [list of third party cargo sub commands](https://github.com/rust-lang/cargo/wiki/Third-party-cargo-subcommands). Extensions I liked very much:

- [cargo fmt](https://github.com/rust-lang/rustfmt) - to format all the code with rustfmt (a tool for formatting Rust code according to style guidelines).
- [cargo count](https://github.com/kbknapp/cargo-count) - to produce statistics for the project (see example below)
- [cargo-deb](https://github.com/mmstick/cargo-deb), [cargo-rpm](https://github.com/rustrpm/cargo-rpm), [cargo-pkgbuild](https://github.com/kstep/cargo-pkgbuild) - for native linux packaging
- [cargo-tree](https://github.com/sfackler/cargo-tree) - list dependency tree just like \`npm ls\`
- [cargo-audit](https://github.com/RustSec/cargo-audit) - Audit Cargo.lock for crates with security vulnerabilities

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
