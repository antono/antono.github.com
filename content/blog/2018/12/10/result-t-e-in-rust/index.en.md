+++
title = "Result<T,E> in Rust"
date = 2018-12-10T22:03:36Z
updated = 2022-04-15T12:14:10Z
aliases = ["/r1YKGw3y4/"]

[taxonomies]
tags = ["rust"]

[extra]
lang = "en"
teletype = "https://blog.antono.info/r1YKGw3y4"
+++
![](475510fa-92f5-486d-a41a-d3c9da93d97b.jpeg)

In my [first puzzle in advent of code challenge](@/blog/2018/12/09/advent-of-code-in-rust/index.en.md) I used some copy/pasted rust code which was not completely clear to me... It's time to understand the code and document it here.

I talking about .expect and .unwrap() methods.

File::open() will throw compilation error without .expect() in copy/pasted code

```rust
File::open(filename).expect("error message");
```

Parse function will throw compilation error without .unwrap() call in copy/pasted code

```rust
line.parse::<i32>().unwrap();
```

From signature of [std::fs::File::open()](https://doc.rust-lang.org/std/fs/struct.File.html#method.open) I see that it returns [Result](https://doc.rust-lang.org/std/io/type.Result.html)\<[File](https://doc.rust-lang.org/std/fs/struct.File.html)\> instead of File. Googling leads to [Error Handling](https://doc.rust-lang.org/1.30.0/book/2018-edition/ch09-00-error-handling.html) topic in Rust Book which explains:

> Rust doesn’t have exceptions. Instead, it has the type `Result<T, E>` for recoverable errors and the `panic!` macro that stops execution when the program encounters an unrecoverable error.

> [`Result<T, E>`](https://doc.rust-lang.org/std/result/enum.Result.html) is the type used for returning and propagating errors. It is an enum with the variants, [`Ok(T)`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Ok), representing success and containing a value, and [`Err(E)`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err), representing error and containing an error value.

Generic Result enum looks like this:

```rust
enum Result<T, E> {
   Ok(T),
   Err(E),
}
```

After getting result developer should handle Ok(result) or Err(why) situations. Typical error handling in rust looks like this:

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

This is how rust book explains code above:

> In the case where `File::open` succeeds, the value in \[match construction\] will be an instance of `Ok` that contains a file handle. In the case where it fails, the value in \[match construction\] will be an instance of `Err` that contains more information about the kind of error that happened.

Only one branch will be executed depending on operation result.

So what is purpose of **.expect()** in this code?

```rust
File::open(filename).expect("error message");
```

Looking at documentation for [std::result::Result](https://doc.rust-lang.org/std/result/enum.Result.html) and seeing explanation:

> Unwraps a result, yielding the content of an [`Ok`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Ok). Panics if the value is an [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err), with a panic message **including the passed message**, and the content of the [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err).

So basically .expect() is a shorthand for match construction above. It either takes result or panics with message. I checked the code of std::result::Result and seeing this:

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

Very similar to example with Result matching i gave above.

One more note from Rust Book:

> Rust groups errors into two major categories: *recoverable* and *unrecoverable* errors. For a recoverable error, such as a file not found error, it’s reasonable to report the problem to the user and retry the operation. Unrecoverable errors are always symptoms of bugs, like trying to access a location beyond the end of an array.

.expect() makes unrecoverable error from recoverable. In simple cases it is okay to handle situation like this but production programs should not panic if file is missing or not readable.

[.unwrap()](https://doc.rust-lang.org/std/result/enum.Result.html#method.unwrap) is very similar to .expect:

> Unwraps a result, yielding the content of an [`Ok`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Ok). Panics if the value is an [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err), with a panic message provided by the [`Err`](https://doc.rust-lang.org/std/result/enum.Result.html#variant.Err)'s value.

So difference from expect is only that expect takes additional error message.

## Additional reading:

- [Rust Book: Error Handling](https://doc.rust-lang.org/1.30.0/book/2018-edition/ch09-00-error-handling.html)
- [Rust By Example: Result](https://doc.rust-lang.org/rust-by-example/error/result.html)
- [std::result](https://doc.rust-lang.org/std/result/index.html) module documentation
- [std::result::Result api](https://doc.rust-lang.org/std/result/enum.Result.html)

---

[Disclaimer](@/blog/2018/12/09/aoc-posts-disclaimer/index.en.md)
