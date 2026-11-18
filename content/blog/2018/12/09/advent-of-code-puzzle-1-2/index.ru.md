+++
title = "Advent of Code: задача 1.2"
date = 2018-12-09T22:52:40Z
updated = 2022-04-15T11:55:32Z

[taxonomies]
tags = ["rust"]

[extra]
lang = "ru"
teletype = "https://blog.antono.info/rkbphGsyE"
+++
![](00327ce5-8ff5-4ef9-9f8e-39a7c2e193fd.jpeg)

*Фото: [Kevin Utting](https://www.flickr.com/photos/tallkev/) ([CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)), кадрировано.*

---

Решаю вторую часть первого дня [Advent of Code](https://adventofcode.com/). Задача продолжает [первую часть первого дня](@/blog/2018/12/09/advent-of-code-in-rust/index.ru.md).

Условие такое:

> Вы замечаете, что устройство раз за разом повторяет один и тот же список изменений частоты. Чтобы откалибровать устройство, нужно найти первую частоту, которая встретится дважды.

Смотрим на решение [из первой части](@/blog/2018/12/09/advent-of-code-in-rust/index.ru.md):

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

Задача кажется простой: надо всего лишь собирать результаты и найти первый повтор! Первая мысль — складывать их в массив и на каждой итерации проверять, есть ли там уже текущий результат. Но поиск по массиву — это O(n), и если итераций понадобится много, код начнёт тормозить. Хеш-таблица тут, пожалуй, лучше — доступ за O(1). Вот только в хеше к каждому ключу нужно хранить какое-то значение, а мне оно ни к чему. Значит, нужна коллекция с дешёвой вставкой и проверкой на вхождение. Посмотрим, что есть в стандартной библиотеке Rust: [коллекции](https://doc.rust-lang.org/beta/std/collections/).

В Rust четыре основные категории коллекций:

- Последовательности: [`Vec`](https://doc.rust-lang.org/beta/std/vec/struct.Vec.html), [`VecDeque`](https://doc.rust-lang.org/beta/std/collections/struct.VecDeque.html), [`LinkedList`](https://doc.rust-lang.org/beta/std/collections/struct.LinkedList.html)
- Словари: [`HashMap`](https://doc.rust-lang.org/beta/std/collections/struct.HashMap.html), [`BTreeMap`](https://doc.rust-lang.org/beta/std/collections/struct.BTreeMap.html)
- Множества: [`HashSet`](https://doc.rust-lang.org/beta/std/collections/struct.HashSet.html), [`BTreeSet`](https://doc.rust-lang.org/beta/std/collections/struct.BTreeSet.html)
- Разное: [`BinaryHeap`](https://doc.rust-lang.org/beta/std/collections/struct.BinaryHeap.html)

Документация вполне приличная и объясняет плюсы и минусы каждого типа…

> [Используйте `Set`-вариант любого из этих `Map`, когда:](https://doc.rust-lang.org/beta/std/collections/#use-the-set-variant-of-any-of-these-maps-when)

> Вам нужно просто запомнить, какие ключи вы уже видели.

> С ключами не связано никакого осмысленного значения.

> Вам просто нужно множество.

Похоже, ровно то, что мне нужно. Есть [BTreeSet](https://doc.rust-lang.org/beta/std/collections/struct.BTreeSet.html) и [HashSet](https://doc.rust-lang.org/beta/std/collections/struct.HashSet.html). Мне кажется, у второго вставка дешевле, так что возьму его.

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

По сути всё то же самое, что и раньше, только теперь каждый результат добавляется в [HashSet](https://doc.rust-lang.org/beta/std/collections/struct.HashSet.html). Метод insert возвращает false, если значение уже есть в множестве.

Запускаю — и ничего не выводится.

Не может быть! Включаю отладочный вывод (по результату на строку) и сравниваю средствами шелла:

```shell
cargo run > nums.txt
wc -l nums.txt
989 nums.txt
uniq nums.txt > nums2.txt
wc -l nums2.txt
989 nums2.txt
```

Количество уникальных значений то же самое — повторов нет. Внимательно перечитываю условие и вижу то, что в первый раз пропустил:

> Учтите, что устройству может понадобиться повторить свой список изменений частоты много раз, прежде чем найдётся повторяющаяся частота, и что повтор может обнаружиться посреди обработки списка.

Ясно. Значит, надо проходить по строкам снова и снова, пока не попадётся повторяющееся число. Но input.lines() возвращает структуру Lines, то есть итератор, а он, дойдя до конца последовательности, просто останавливается. Первой мыслью было превратить итератор в список и дальше по старинке крутить бесконечный цикл с ручной вознёй с индексами + break, как только значение найдено. Но, покопавшись в документации по итераторам, я нашёл способ зациклить итератор: [std::iter::iterator#cycle](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.cycle). input.lines() возвращает [структуру Lines, реализующую трейт Iterator](https://doc.rust-lang.org/std/str/struct.Lines.html). Судя по всему, это значит, что можно вызвать cycle() и бесконечно ходить по значениям по кругу.

Добавляю вызов .cycle() на Lines:

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

Запускаем:

```
cargo run
   Compiling aoc2018 v0.1.0 (file:///Users/antono/Code/rust/aoc2018)
    Finished dev [unoptimized + debuginfo] target(s) in 0.62 secs
     Running `target/debug/1`
Sum of freq adjustments: 493
Repeating frequency: 413
```

Отправляю ответ:

> Это правильный ответ! Вы на одну золотую звезду ближе к починке потока времени.

Код запушен на GitHub.

---

## Выводы

- Внимательно читайте условие :)
- Навыки работы в Unix-шелле всё ещё в цене
- Всё, что мне нужно знать [об итераторах в Rust, — на одной странице](https://doc.rust-lang.org/std/iter/index.html)

---

[Дисклеймер](@/blog/2018/12/09/aoc-posts-disclaimer/index.ru.md)
