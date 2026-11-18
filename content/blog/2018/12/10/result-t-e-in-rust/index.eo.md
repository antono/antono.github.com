+++
title = "Result<T,E> en Rust"
date = 2018-12-10T22:03:36Z
updated = 2022-04-15T12:14:10Z

[taxonomies]
tags = ["rust"]

[extra]
lang = "eo"
teletype = "https://blog.antono.info/r1YKGw3y4"
+++
![](475510fa-92f5-486d-a41a-d3c9da93d97b.jpeg)

En mia [unua enigmo de la defio Advent of Code](@/blog/2018/12/09/advent-of-code-in-rust/index.eo.md) mi uzis iom da kopiita kaj algluita Rust-kodo, kiun mi ne tute komprenis… Jam tempas kompreni la kodon kaj priskribi ĝin ĉi tie.

Temas pri la metodoj .expect kaj .unwrap().

File::open() en la kopiita kodo kaŭzas kompilan eraron sen .expect()

```rust
File::open(filename).expect("error message");
```

La funkcio parse en la kopiita kodo kaŭzas kompilan eraron sen voko de .unwrap()

```rust
line.parse::<i32>().unwrap();
```

El la signaturo de [std::fs::File::open()](https://doc.rust-lang.org/std/fs/struct.File.html#method.open) mi vidas, ke ĝi redonas ne File, sed [Result](https://doc.rust-lang.org/std/io/type.Result.html)\<[File](https://doc.rust-lang.org/std/fs/struct.File.html)\>. Guglado kondukas al la ĉapitro [Error Handling](https://doc.rust-lang.org/1.30.0/book/2018-edition/ch09-00-error-handling.html) en la Rust Book, kiu klarigas:

> Rust ne havas esceptojn. Anstataŭe ĝi havas la tipon `Result<T, E>` por ripareblaj eraroj kaj la makroon `panic!`, kiu haltigas la plenumon, kiam la programo renkontas neripareblan eraron.

> [`Result<T, E>`](https://doc.rust-lang.org/std/result/enum.Result.html) estas la tipo uzata por redoni kaj plusendi erarojn. Ĝi estas enumeracio kun la variantoj [`Ok(T)`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Ok), kiu reprezentas sukceson kaj enhavas valoron, kaj [`Err(E)`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err), kiu reprezentas eraron kaj enhavas erarvaloron.

La ĝenerala enumeracio Result aspektas jene:

```rust
enum Result<T, E> {
   Ok(T),
   Err(E),
}
```

Ricevinte rezulton, la programisto devas trakti ambaŭ kazojn: Ok(result) kaj Err(why). Tipa erartraktado en Rust aspektas jene:

```rust
use std::fs::File;
use std::error::Error;

fn main() {
    let path = ".gitignore";
    match File::open(&path) {
        Err(why) => panic!("couldn't open {}: {}", path, why.description()),
        Ok(file) => println!("{:?}", file),
    };
}
```

Jen kiel la Rust Book klarigas la supran kodon:

> Kiam `File::open` sukcesas, la valoro en \[la konstruaĵo match\] estos instanco de `Ok`, kiu enhavas dosiertenilon. Kiam ĝi malsukcesas, la valoro en \[la konstruaĵo match\] estos instanco de `Err`, kiu enhavas pliajn informojn pri la speco de la okazinta eraro.

Depende de la rezulto de la operacio, plenumiĝos nur unu branĉo.

Do kio estas la celo de **.expect()** en ĉi tiu kodo?

```rust
File::open(filename).expect("error message");
```

Mi rigardas la dokumentaron de [std::result::Result](https://doc.rust-lang.org/std/result/enum.Result.html) kaj vidas jenan klarigon:

> Elpakas rezulton, liverante la enhavon de [`Ok`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Ok). Panikas, se la valoro estas [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err), kun panikmesaĝo, **kiu inkluzivas la transdonitan mesaĝon**, kaj la enhavon de [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err).

Do esence .expect() estas mallongigo de la supra konstruaĵo match. Ĝi aŭ prenas la rezulton, aŭ panikas kun mesaĝo. Mi kontrolis la kodon de std::result::Result kaj vidas jenon:

```rust
  #[inline]
  #[stable(feature = "result_expect", since = "1.4.0")]
  pub fn expect(self, msg: &str) -> T {
      match self {
          Ok(t) => t,
          Err(e) => unwrap_failed(msg, e),
      }
  }
```

Tre simile al la ekzemplo kun kongruigo de Result, kiun mi donis supre.

Ankoraŭ unu noto el la Rust Book:

> Rust grupigas erarojn en du ĉefajn kategoriojn: *ripareblaj* kaj *neripareblaj* eraroj. Ĉe riparebla eraro, ekzemple kiam dosiero ne troviĝas, estas racie raporti la problemon al la uzanto kaj reprovi la operacion. Nerepareblaj eraroj ĉiam estas simptomoj de cimoj, ekzemple provo aliri lokon trans la fino de tabelo.

.expect() faras el riparebla eraro neripareblan. En simplaj kazoj estas akcepteble trakti la situacion tiel, sed produktaj programoj ne paniku, se dosiero mankas aŭ ne estas legebla.

[.unwrap()](https://doc.rust-lang.org/std/result/enum.Result.html#method.unwrap) tre similas al .expect:

> Elpakas rezulton, liverante la enhavon de [`Ok`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Ok). Panikas, se la valoro estas [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err), kun panikmesaĝo provizita de la valoro de [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err).

Do la sola diferenco estas, ke expect akceptas aldonan erarmesaĝon.

## Plia legaĵo:

- [Rust Book: Error Handling](https://doc.rust-lang.org/1.30.0/book/2018-edition/ch09-00-error-handling.html)
- [Rust By Example: Result](https://doc.rust-lang.org/rust-by-example/error/result.html)
- dokumentaro de la modulo [std::result](https://doc.rust-lang.org/std/result/index.html)
- [API de std::result::Result](https://doc.rust-lang.org/std/result/enum.Result.html)

---

[Averto](@/blog/2018/12/09/aoc-posts-disclaimer/index.eo.md)
