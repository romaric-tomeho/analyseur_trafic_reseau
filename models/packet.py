from __future__ import annotations # type: ignore
from dataclasses import dataclass,field
@dataclass(slots=True)
class Packet:
    source:str
    destination:str
    size:int
    priority:int=0
    path:list[str]=field(default_factory=list)
    total_lactency_ms:float=0.0
    delivered:bool=False
    dropped_raison:str |None =None
    def add_hop(self,node_id:str)->None:
        self.path.append(node_id)
    def add_lactency(self,lactency_ms:float)->None:
        self.total_lactency_ms+=lactency_ms
    def mark_delivered(self)->None:
        self.delivered=True
    def mark_dropped(self,reason:str)->None:
        self.dropped_raison=reason
    def to_dict(self)->dict[str,object]:
        return{
            "source": self.source,
            "destintion":self.destination,
            "size":self.size,
            "priority":self.priority,
            "path":list(self.path),
            "total_lactency_ms":self.total_lactency_ms,
            "delivered":self.delivered,
            "dropped":self.dropped_raison

        }        
