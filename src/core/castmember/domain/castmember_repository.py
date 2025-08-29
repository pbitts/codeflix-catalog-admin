from abc import ABC, abstractmethod
from uuid import UUID

from src.core.castmember.domain.castmember import CastMember


class CastMemberRepository(ABC):
    @abstractmethod
    def save(self, castmember):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> CastMember | None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, castmember: CastMember) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[CastMember]:
        raise NotImplementedError