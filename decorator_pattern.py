import logging 
from abc import ABC, abstractmethod
from math import sqrt
from time import perf_counter
from typing import Callable, Any

def is_prime(number: int) -> bool:
    if number < 2: 
        return False
    for element in range(2, int(sqrt(number)) + 1):
        if number % element == 0:
            return False

    return True


class AbstractComponent(ABC):
    @abstractmethod
    def execute(self, upper_bound: int) -> int:
        pass

#class ConcreteComponent(AbstractComponent):
#    def execute(self, upper_bound: int) -> int:
#        count = 0
#        for number in range(upper_bound):
#            if is_prime(number):
#                count += 1
#        return count


#def count_prime_numbers(upper_bound: int) -> int:
#    count = 0
#    for number in range(upper_bound):
#        if is_prime(number):
#            count += 1
#    return count



class AbstractDecorator(AbstractComponent):
    def __init__(self, decorated = AbstractComponent) -> None:
        self._decorated = decorated


class BenchmarkDecorator(AbstractDecorator):
    def execute(self, upper_bound: int) -> int:
        start_time = perf_counter()
        value = self._decorated.execute(upper_bound)
        end_time = perf_counter()
        run_time = end_time - start_time

        logging.info(
            f"execution of {self._decorated.__class__.__name__} took {run_time: .4f} seconds"
        )

        return value


#but this is not easy to use with other function that i want to benchmark

#def benchmark(upper_bound: int) -> int: 
#    start_time = perf_counter()
#    value = count_prime_numbers(upper_bound)
#    end_time = perf_counter()
#    run_time = end_time - start_time
#
#    logging.info(
#        f"execution of took {run_time: .4f} seconds"
#    )
#
#    return value

#we need a more generic function that will take a function and arbitrary arguments and will pass the arbitrary arguments to the function
def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time

        print(f"execution of {func.__name__} took {run_time: .4f} seconds")
        return value
    return wrapper
#but the same thing can be done using python decorator

#now define a wrapper method for logging
#class LoggingDecorator(AbstractDecorator):
#    def execute(self, upper_bound: int) -> int:
#        logging.info(f"Calling {self._decorated.__class__.__name__}")
#        value = self._decorated.execute(upper_bound)
#        logging.info(f"Finished calling {self._decorated.__class__.__name__}")
#        return value
def logger(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__}")
        value = count_prime_numbers(*args, **kwargs)
        logging.info(f"Finished calling {func.__name__}")
        return value
    return wrapper



#@logger
@benchmark
def count_prime_numbers(upper_bound: int) -> int:
    count = 0
    for number in range(upper_bound):
        if is_prime(number):
            count += 1
    return count


def main() -> None:

    logging.basicConfig(level=logging.INFO)
    #component = ConcreteComponent()
    #benchmark_decorator = BenchmarkDecorator(component)
    #logging_decorator = LoggingDecorator(benchmark_decorator)
    #value = benchmark_decorator.execute(10000)

    #after using wrapper inside generic benchmark
    #wrapper = benchmark(count_prime_numbers) #code cleaner than using only classes
    #value = wrapper(10000)
    
    #using only benchmark decorators
    #value = count_prime_numbers(10000)
    #logging.info(f"Found {value} prime numbers")

    #using both benchmark and logging decorators
    value = count_prime_numbers(10000)
    logging.info(f"Found {value} prime numbers")

if __name__=="__main__":
    main()
