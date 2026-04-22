from__future__ import annotations # type: ignore
from models.packet import Packet
class NetworkLink:
    def __init__(self,
        source_id: str,
        destination_id:str,
        bandwidth_mbps:float,
        lactency_ms:float,
        active:bool=True,        

     )->None:
        self._source_id = source_id
        self._destination_id = destination_id
        self._bandwidth_mbps = bandwidth_mbps
        self._lactency_ms = lactency_ms
        self._active = active
        self._current_load_mbps = 0.0

    @property
    def source_id(self)->str:
        return self._source_id
    @property
    def destination_id(self)->str:
        return self._destination_id    
    @property
    def bandwidth_mbps(self)->float:
        return self._bandwidth_mbps
    def lactency_ms(self)->float:
        return self._lactency_ms
    @property
    def current_load_mbps(self)-> float:
        return self._current_load_mbps
    @property
    def active(self)->bool:
        return self._active
    def activate(self)-> bool:
        return self._active == True
    def deactivate(self)-> None:
        self._active ==False
    def reset_load(self)-> None:
        self._current_load_mbps=0.0
    def is_saturated(self,thresnold: float=0.8)->bool:
        if self._bandwidth_mbps ==0:   
            return True
        return(self._current_load_mbps/ self._bandwidth_mbps)>=thresnold
    def trasmit(self,packet: Packet)-> bool:
        if not self._active:
            packet.mark_dropped("link_inactive")
            return False
        packet_load =(packet.size*8)/1_000_000
        if self.current_load_mbps+packet_load >self._bandwidth_mbps:
            packet.mark_dropped("link_saturated")
            return False
        self.current_load_mbps+=packet_load
        packet.add_lactency(self._lactency_ms)
        return True
    def to_dict(self)->dict[str,object]:
           return{
            "source": self.source_id,
            "destination": self.destination_id,
            "bandwidth_mbps": self.bandwidth_mbps,
            "latency_ms": self.latency_ms,
            "active": self.active,
           }    
    

