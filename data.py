from dataclasses import dataclass


@dataclass
class FB:
    name: str
    fb_type: str
    resource: str = ''

@dataclass
class Parameter:
    value: str
    destination: str
    fb: FB

@dataclass
class Connection:
    source: str
    destination: str
    resource: str

@dataclass
class Resource:
    short_name: str
    res_type: str
    full_name: str = ''