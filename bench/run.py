from argparse import ArgumentParser
from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Dict, Generic, List, TypeVar

from bench import simple, jin

A = TypeVar('A')


@dataclass
class BenchCompare(Generic[A]):
    gen: Callable[[int], A]
    comparisons: Dict[str, Callable[[List[A]], None]]


SIMPLE_HTML = "SIMPLE_HTML"
JINJA2 = "JINJA2"

benches = {
    "hello world": BenchCompare(
        lambda i: None,
        {
            SIMPLE_HTML: simple.hello_world_empty,
            JINJA2: jin.hello_world_empty
        },
    ),
    "basic": BenchCompare(
        lambda i: (str(i), f"some content {i}", ["ok" for _ in range(i % 50)]),
        {SIMPLE_HTML: simple.basic,
         JINJA2: jin.basic}
    )
}


def run_bench(
        chunks: int, chunk_size: int, gen: Callable[[int], A],
        fn: Callable[[List[A]], None]
) -> None:
    total_time: float = 0.0
    for i in range(chunks):
        # generate in chunks so generation isn't included in the
        # measured time
        objs = [gen((i * chunk_size) + j + 1) for j in range(chunk_size)]
        start = perf_counter()
        fn(objs)
        total_time += perf_counter() - start

    print(f"Execution time: {total_time:.4f} secs\n")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "tests",
        type=str,
        nargs="*",
        help="which tests to run",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=50,
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1_000,
    )

    args = parser.parse_args()

    print(f"{args.iterations} ITERATIONS of {args.chunk_size}")

    for name, compare_bench in benches.items():
        if args.tests == [] or name in args.tests:
            print(f"----- BEGIN {name} -----\n")
            for subject_name, test in compare_bench.comparisons.items():
                print(subject_name)
                run_bench(args.iterations, args.chunk_size, compare_bench.gen, test)

            print(f"----- END {name} -----\n")
