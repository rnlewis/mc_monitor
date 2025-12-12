import re
from typing import Dict, Any


class Version:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        data: int = 0,
        series: str = "",
        protocol: int = 0,
        build_time: str = "",
        pack_resource: float = 0.0,
        pack_data: float = 0.0,
        stable: bool = False,
    ):
        self.id = id
        self.name = name
        self.data = data
        self.series = series
        self.protocol = protocol
        self.build_time = build_time
        self.pack_resource = pack_resource
        self.pack_data = pack_data
        self.stable = stable

    def __str__(self):
        return (
            f"ID: {self.id}, Name: {self.name}, Data: {self.data}, Series: {self.series}, "
            f"Protocol: {self.protocol}, Build Time: {self.build_time}, "
            f"Pack Resource: {self.pack_resource}, Pack Data: {self.pack_data}, Stable: {self.stable}"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "data": self.data,
            "series": self.series,
            "protocol": self.protocol,
            "build_time": self.build_time,
            "pack_resource": self.pack_resource,
            "pack_data": self.pack_data,
            "stable": self.stable,
        }

    @classmethod
    def from_string(cls, raw: str):
        """
        Parse a raw 'Server version info' string into a Version object.
        Example input:
        'Server version info:id = 1.21.10name = 1.21.10data = 4556series = mainprotocol = 773 (0x305)build_time = Tue Oct 07 05:14:11 EDT 2025pack_resource = 69.0pack_data = 88.0stable = yes'
        """

        KEYS = (
            "id|name|data|series|protocol|build_time|pack_resource|pack_data|stable"
        )

        pattern = re.compile(rf"(\w+)\s*=\s*(.*?)(?=(?:{KEYS})\s*=|$)")
        raw = re.sub(r"^.*?info:\s*", "", raw, flags=re.IGNORECASE)
        fields: Dict[str, str] = {}
        for key, val in pattern.findall(raw):
            fields[key] = val.strip()

        return cls(
            id=fields.get("id", ""),
            name=fields.get("name", ""),
            data=int(fields.get("data", 0)),
            series=fields.get("series", ""),
            protocol=int(fields.get("protocol", "0").split()[0]),
            build_time=fields.get("build_time", ""),
            pack_resource=float(fields.get("pack_resource", 0.0)),
            pack_data=float(fields.get("pack_data", 0.0)),
            stable=fields.get("stable", "").lower() in ("yes", "true", "1"),
        )
