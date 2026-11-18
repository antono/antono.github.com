+++
title = "Result<T,E> в Rust"
date = 2018-12-10T22:03:36Z
updated = 2022-04-15T12:14:10Z

[taxonomies]
tags = ["rust"]

[extra]
lang = "ru"
teletype = "https://blog.antono.info/r1YKGw3y4"
+++
![](475510fa-92f5-486d-a41a-d3c9da93d97b.jpeg)

В [первой задаче Advent of Code](@/blog/2018/12/09/advent-of-code-in-rust/index.ru.md) я использовал скопипащенный код на Rust, который был мне не до конца понятен… Пора разобраться в нём и записать всё здесь.

Речь о методах .expect и .unwrap().

File::open() в скопипащенном коде без .expect() даёт ошибку компиляции

```rust
File::open(filename).expect("error message");
```

Функция parse в скопипащенном коде без вызова .unwrap() даёт ошибку компиляции

```rust
line.parse::<i32>().unwrap();
```

По сигнатуре [std::fs::File::open()](https://doc.rust-lang.org/std/fs/struct.File.html#method.open) видно, что она возвращает не File, а [Result](https://doc.rust-lang.org/std/io/type.Result.html)\<[File](https://doc.rust-lang.org/std/fs/struct.File.html)\>. Гугл приводит к главе [Error Handling](https://doc.rust-lang.org/1.30.0/book/2018-edition/ch09-00-error-handling.html) в Rust Book, где объясняется:

> В Rust нет исключений. Вместо них есть тип `Result<T, E>` для исправимых ошибок и макрос `panic!`, который останавливает выполнение, когда программа сталкивается с неисправимой ошибкой.

> [`Result<T, E>`](https://doc.rust-lang.org/std/result/enum.Result.html) — это тип, который используется для возврата и распространения ошибок. Это перечисление с вариантами [`Ok(T)`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Ok), обозначающим успех и содержащим значение, и [`Err(E)`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err), обозначающим ошибку и содержащим значение ошибки.

Обобщённое перечисление Result выглядит так:

```rust
enum Result<T, E> {
   Ok(T),
   Err(E),
}
```

Получив результат, разработчик должен обработать оба случая: Ok(result) и Err(why). Типичная обработка ошибок в Rust выглядит так:

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

Вот как Rust Book объясняет этот код:

> Если `File::open` выполнится успешно, значением в \[конструкции match\] будет экземпляр `Ok`, содержащий дескриптор файла. Если же произойдёт ошибка, значением в \[конструкции match\] будет экземпляр `Err`, содержащий подробности о том, какая ошибка случилась.

В зависимости от результата операции выполнится только одна ветка.

Так зачем же в этом коде **.expect()**?

```
File::open(filename).expect("error message");
```

Смотрю документацию по [std::result::Result](https://doc.rust-lang.org/std/result/enum.Result.html) и вижу объяснение:

> Разворачивает результат, возвращая содержимое [`Ok`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Ok). Паникует, если значение — [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err), с сообщением о панике, **включающим переданное сообщение** и содержимое [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err).

То есть по сути .expect() — это сокращённая запись той самой конструкции match. Она либо достаёт результат, либо паникует с сообщением. Я заглянул в код std::result::Result и вижу вот что:

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

Очень похоже на пример с сопоставлением Result, который я приводил выше.

И ещё одна цитата из Rust Book:

> Rust делит ошибки на две большие категории: *исправимые* и *неисправимые*. В случае исправимой ошибки, например когда файл не найден, разумно сообщить о проблеме пользователю и повторить операцию. Неисправимые ошибки — это всегда симптомы багов, например попытка обратиться к элементу за пределами массива.

.expect() превращает исправимую ошибку в неисправимую. В простых случаях так обходиться с ситуацией нормально, но боевая программа не должна паниковать, если файла нет или его нельзя прочитать.

[.unwrap()](https://doc.rust-lang.org/std/result/enum.Result.html#method.unwrap) очень похож на .expect:

> Разворачивает результат, возвращая содержимое [`Ok`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Ok). Паникует, если значение — [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err), с сообщением о панике, которое берётся из значения [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err).

Так что отличие от expect только в том, что expect принимает дополнительное сообщение об ошибке.

## Что почитать ещё:

- [Rust Book: Error Handling](https://doc.rust-lang.org/1.30.0/book/2018-edition/ch09-00-error-handling.html)
- [Rust By Example: Result](https://doc.rust-lang.org/rust-by-example/error/result.html)
- документация модуля [std::result](https://doc.rust-lang.org/std/result/index.html)
- [API std::result::Result](https://doc.rust-lang.org/std/result/enum.Result.html)

---

[Дисклеймер](@/blog/2018/12/09/aoc-posts-disclaimer/index.ru.md)
