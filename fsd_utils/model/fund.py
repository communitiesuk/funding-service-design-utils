import inspect
from dataclasses import dataclass
from dataclasses import field

from fsd_utils.model.round import Round


@dataclass
class Fund:
    id: str
    name_json: dict
    title_json: dict
    short_name: str
    description_json: dict
    owner_organisation_name: str
    owner_organisation_shortname: str
    welsh_available: bool = False
    owner_organisation_logo_uri: str | None = None
    has_devolved_authority_validation: bool = False
    fund_types: list[str] = field(default_factory=lambda: ["ALL"])
    rounds: list[Round] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            **{
                k: v
                for k, v in d.items()
                if k in inspect.signature(cls).parameters and v is not None
            }
        )

    def add_round(self, fund_round: Round):
        if not self.rounds:
            self.rounds = []
        self.rounds.append(fund_round)
