from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.session import Base

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    dob = Column(String(10), nullable=True)
    reg_no = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    certificates = relationship('Certificate', back_populates='student')

class Certificate(Base):
    __tablename__ = 'certificates'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=True)
    image_path = Column(String(500), nullable=False)
    status = Column(String(50), default='processed')
    created_at = Column(DateTime, default=datetime.utcnow)
    student = relationship('Student', back_populates='certificates')
    fields = relationship('ExtractedField', back_populates='certificate', cascade='all, delete-orphan')

class ExtractedField(Base):
    __tablename__ = 'extracted_fields'
    id = Column(Integer, primary_key=True)
    certificate_id = Column(Integer, ForeignKey('certificates.id'), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    certificate = relationship('Certificate', back_populates='fields')

