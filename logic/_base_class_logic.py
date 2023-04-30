from models.database import SessionLocal
from models.crud import criteria, contractors, contractors_to_contractors
from typing import List, Dict

class BaseClassLogic:

    @staticmethod
    def get_contractors_query():
        with SessionLocal() as session:
            contractors_list = contractors.get_limit_offset(session, 5, 0)
        return contractors_list

    @staticmethod
    def get_data_contractors() -> List[Dict]:
        data = []
        with SessionLocal() as session:
            contractors_list = contractors.get_list(session)
        for unit in contractors_list:
            data.append({
                "id_contractor": unit.id_contractor, "contractor_name": unit.contractor_name,
                "work_cost": unit.work_cost, "availability_of_technology": unit.availability_of_technology,
                "tech_equipment": unit.tech_equipment,
                "availability_of_production_facilities": unit.availability_of_production_facilities,
                "qualified_human_resources_personnel": unit.qualified_human_resources_personnel
            })
        return data

    @staticmethod
    def get_data_criteria() -> list:
        data = []
        with SessionLocal() as session:
            criteria_list = criteria.get_criteria_list(session)
        for criteria_unit in criteria_list:
            data.append({"id": criteria_unit.id_criteria, "name": criteria_unit.criteria_name})
        return data
