from models.database import SessionLocal
from models.crud import criteria, contractors, compare
from typing import List, Dict


class BaseClassLogic:

    @staticmethod
    def is_number(str_number: str) -> bool:
        if "." in str_number:
            splitting = str_number.split(".")
            if splitting[0].isnumeric() and splitting[1].isnumeric():
                return True
        elif "," in str_number:
            splitting = str_number.split(",")
            if splitting[0].isnumeric() and splitting[1].isnumeric():
                return True
        else:
            return str_number.isnumeric()

    @staticmethod
    def get_or_create_compare(compare_name: str) -> int:
        with SessionLocal() as session:
            exist = compare.get(session, compare_name)
            if exist:
                return int(exist.id_compare)
            else:
                exist = compare.create(session, compare_name)
                return int(exist.id_compare)

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
            data.append({
                "id": criteria_unit.id_criteria,
                "name": criteria_unit.criteria_name,
                "code": criteria_unit.criteria_code
            })
        return data
