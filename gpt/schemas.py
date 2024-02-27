from pydantic import BaseModel


class Algorithm(BaseModel):
    order: int
    text: str


class TaskDetail(BaseModel):
    algorithms: list[Algorithm]

    @property
    def pretty_text(self) -> str:
        prefix = 'Here is your algorithm:\n'
        algorithms = '\n'.join(f'{a.order}) {a.text}'
                               for a in self.algorithms)

        return prefix + algorithms
