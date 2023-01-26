from typing import List


class DnsRecord:
    def __init__(self, name, content, zone_id, type: str = "CNAME",
                 ttl: int = 600, comment: str = None, tags: List[str] = None):
        self.name = name
        self.content = content
        self.zone_id = zone_id
        self.type = type
        self.ttl = ttl
        self.comment = comment
        self.tags = tags

    @classmethod
    def from_properties(cls, properties):
        return cls(
            properties['Name'],
            properties['Content'],
            properties['ZoneId'],
            properties.get('Type', 'CNAME'),
            properties.get('Ttl', 600),
            properties.get('Comment'),
            properties.get('Tags')
        )

    def to_json(self):
        record = {
            'type': self.type,
            'name': self.name,
            'content': self.content,
            'ttl': self.ttl
        }
        if self.comment:
            record['comment'] = self.comment
        if self.tags:
            record['tags'] = self.tags
        return record
