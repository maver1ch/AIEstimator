from typing import Optional
from sqlalchemy.orm import Session
from backend.crud.base import CRUDBase
from backend.models.document import Document

class CRUDDocument(CRUDBase[Document]):
    def get_by_filename(self, db: Session, *, filename: str) -> Optional[Document]:
        return db.query(self.model).filter(self.model.filename == filename).first()

document = CRUDDocument(Document)
