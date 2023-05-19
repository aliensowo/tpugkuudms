from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from models.database import Base

class Work(Base):
    __tablename__ = "Work"
    id_work = Column(Integer, primary_key=True)
    work_name = Column(String)

class Plan(Base):
    __tablename__ = "Plan"
    id = Column(Integer, primary_key=True)
    id_work = Column(String)
    work_name = Column(String)
    volume = Column(String)
    work_start = Column(String)
    work_end =Column(String)
    work_complete = Column(String)

class Fact(Base):
    __tablename__ = "Fact"
    id = Column(Integer, primary_key=True)
    id_work = Column(String)
    work_name = Column(String)
    volume = Column(String)
    work_start = Column(String)
    work_end =Column(String)
    work_complete = Column(String)

class ObjectsContracts(Base):
    __tablename__ = "ObjectsContracts"

    id_object = Column(Integer, primary_key=True)
    object_name = Column(String)
    date_start = Column(String)
    date_end = Column(String)


class ValuationObject(Base):
    __tablename__ = "ValuationObject"

    id_valuation_object = Column(Integer, primary_key=True)
    valuation_object_name = Column(String)


class PlanAndFacts(Base):
    __tablename__ = "PlanAndFacts"

    id_plan_and_fact = Column(Integer, primary_key=True)
    id_valuation_object = Column(Integer, ForeignKey('ValuationObject.id_valuation_object', ondelete='CASCADE'))
    plan = Column(String)
    fact = Column(String)


class ObjectPlanFact(Base):
    __tablename__ = "ObjectPlanFact"

    id_object = Column(Integer, ForeignKey('ObjectsContracts.id_object', ondelete='CASCADE'), primary_key=True)
    id_plan_and_fact = Column(Integer, ForeignKey('PlanAndFacts.id_plan_and_fact', ondelete='CASCADE'))


class WorkGroupClassifications(Base):
    __tablename__ = "WorkGroupClassifications"

    id_work_group = Column(Integer, primary_key=True)
    work_group_name = Column(String)


class WorkTypes(Base):
    __tablename__ = "WorkTypes"

    id_work_type = Column(Integer, primary_key=True)
    id_work_group = Column(
        String,
        ForeignKey('WorkGroupClassifications.id_work_group', ondelete='CASCADE'),
        nullable=False,
    )
    work_type_name = Column(String)


class Works(Base):
    __tablename__ = "Works"

    id_work = Column(Integer, primary_key=True)
    id_work_type = Column(Integer, ForeignKey('WorkTypes.id_work_type', ondelete='CASCADE'))
    id_object = Column(Integer, ForeignKey('ObjectsContracts.id_object', ondelete='CASCADE'))
    work_name = Column(String)
    unit = Column(String)
    budgeted_items = Column(String)
    unit_rate_number = Column(String)
    Price_per_unit = Column(String)


class WorkPlanFact(Base):
    __tablename__ = "WorkPlanFact"

    id_work = Column(Integer, ForeignKey('Works.id_work', ondelete='CASCADE'), primary_key=True)
    id_plan_and_fact = Column(Integer, ForeignKey('PlanAndFacts.id_plan_and_fact', ondelete='CASCADE'))


class CompletedWorksAsKC6a(Base):
    __tablename__ = "CompletedWorksAsKC6a"

    id_completed_work = Column(Integer, primary_key=True)
    id_work = Column(Integer, ForeignKey('Works.id_work', ondelete='CASCADE'))
    year = Column(String)
    month = Column(String)
    count = Column(String)
    cost = Column(String)


class NeighborhoodDirectory(Base):
    __tablename__ = "NeighborhoodDirectory"

    id_directory = Column(Integer, primary_key=True)
    directory_name = Column(String)
    directory_start = Column(String)
    directory_end = Column(String)


class WorkToDirectories(Base):
    # TODO: мб не нужна тк будет мтм
    __tablename__ = "Directories"

    id = Column(Integer, primary_key=True)
    id_work = Column(Integer, ForeignKey('Works.id_work', ondelete='CASCADE'))
    id_directory = Column(Integer, ForeignKey('NeighborhoodDirectory.id_directory', ondelete='CASCADE'))


class Criteria(Base):
    __tablename__ = "Criteria"

    id_criteria = Column(Integer, primary_key=True)
    criteria_name = Column(String)


class Contractors(Base):
    __tablename__ = "Contractors"

    id_contractor = Column(Integer, primary_key=True)
    contractor_name = Column(String)
    work_cost = Column(String)
    availability_of_technology = Column(String)
    tech_equipment = Column(String)
    availability_of_production_facilities = Column(String)
    qualified_human_resources_personnel = Column(String)


class Compare(Base):
    __tablename__ = "Compare"

    id_compare = Column(Integer, primary_key=True)
    name = Column(String)


class CompareWinners(Base):
    __tablename__ = "CompareWinners"

    id_compare_winner = Column(Integer, primary_key=True)
    id_compare = Column(Integer, ForeignKey('Compare.id_compare', ondelete='CASCADE'))
    id_contractor = Column(Integer, ForeignKey('Contractors.id_contractor', ondelete='CASCADE'))


class CriteriaToCriteria(Base):
    __tablename__ = "CriteriaToCriteria"

    id_criteria_to_criteria = Column(Integer, primary_key=True)
    id_criteria_one = Column(Integer, ForeignKey("Criteria.id_criteria", ondelete='CASCADE'))
    id_criteria_two = Column(Integer, ForeignKey("Criteria.id_criteria", ondelete='CASCADE'))
    value = Column(String)
    id_compare = Column(Integer, ForeignKey('Compare.id_compare', ondelete='CASCADE'))


class ContractorsToContractors(Base):
    __tablename__ = "ContractorsToContractors"

    id_contractor_to_contractor = Column(Integer, primary_key=True)
    id_contractor_one = Column(Integer, ForeignKey("Contractors.id_contractor", ondelete='CASCADE'))
    id_contractor_two = Column(Integer, ForeignKey("Contractors.id_contractor", ondelete='CASCADE'))
    value = Column(String)
    id_criteria = Column(Integer, ForeignKey("Criteria.id_criteria", ondelete='CASCADE'))
    id_compare = Column(Integer, ForeignKey('Compare.id_compare', ondelete='CASCADE'))


class CustomUsers(Base):
    __tablename__ = "CustomUsers"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
