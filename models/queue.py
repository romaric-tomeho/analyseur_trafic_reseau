from __future__ import annotations
import heapq
from collections import deque
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.packet import Packet

class PacketQueue:
        def __init__(self, max_size: int = 10, mode: str = "fifo") -> None:
            if mode not in {"fifo", "priority"}:
              raise ValueError("mode must be 'fifo' or 'priority'")
            self._max_size = max_size
            self._mode = mode
            self._lost_packets = 0
            self._fifo_queue: deque[Packet] = deque()
            self._priority_queue: list[tuple[int, int, Packet]] = []
            self._sequence = 0
        @property
        def lost_packets(self)-> int:
             return self._lost_packets
        @property
        def mode(self)-> str: 
             return self._mode
        @property
        def max_size(self)-> int:
             return self._max_size
        def enqueue(self,packet: "Packet")-> bool:
             if len(self)>= self._max_size:
                  self._lost_packets+=1
                  packet.mark_dropped("queue_ouverflow")
                  return False
             if self._mode =="fifo":
                  self._fifo_queue.append(packet)
             else:
                  heapq.heappush(
                      self._priority_queue,
                      (-packet.priority,self._sequence,packet), 
                  )
                  self._sequence+=1
                  return True
             def dequeue(self)-> "Packet |None":
                  if self._mode == "fifo":
                       return self._fifo_queue.popleft() if self._fifo_queue else None
                  if not self._priority_queue:
                       return None
                  return heapq.heappop(self._priority_queue)[2]
             def snapshot(self)-> list[dict[str,object]]:
                  if self._mode =="fifo":
                       return [packet.to_dict() for packet in self._priority_queue]
                  return[item[2].to_dict() for item in sorted (self.priority_queue)]
             def _len_(self)-> int:
                  if self._mode == "fifo":
                       return len(self.fifo_queue)
                  return len(self._priority_queue)
             