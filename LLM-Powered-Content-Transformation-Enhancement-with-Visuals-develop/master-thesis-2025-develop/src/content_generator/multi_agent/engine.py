import time

from abc import abstractmethod, ABC
from typing import Any
from functools import wraps

from langgraph.graph import StateGraph


class Engine:
    def run(self, graph: StateGraph, initial_state: Any) -> Any:
        # todo: add logging or anything what may be useful

        return graph.invoke(initial_state)


def log_node(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"Running {f.__name__}")
        res = f(*args, **kwargs)
        print(f"Result (in {time.time() - start}) of {f.__name__}: \n{res}")
        return res

    return wrapper


class NodeBase(ABC):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        start = time.time()
        print(f"Running {self.name()}")
        res = self.call(*args, **kwds)
        print(f"Result (in {time.time() - start}) of {self.name()}: \n{res}")
        return res

    @abstractmethod
    def call(self, *args: Any, **kwds: Any) -> Any:
        pass

    def name(self):
        return self.__class__.__name__


def visualise_graph(graph, out_path: str = "") -> str:
    try:
        drawable = graph.get_graph(xray=1)
        if out_path:
            drawable.draw_png(output_file_path=out_path)
        return drawable.draw_ascii()

    except Exception as e:
        print(f"can not visualise flow: {e}")
        pass
