from models.database import SessionLocal
from models.crud import contractors, criteria

"""
Добавить автоматически данные критериев и подрядчиков
"""

if __name__ == '__main__':
    with SessionLocal() as session:
        # restore contractors
        contractors_list = [
            {
                "contractor_name": "Подрядчик1", "work_cost": "300000", "availability_of_technology": "да",
                "tech_equipment": "высокая", "availability_of_production_facilities": "да",
                "qualified_human_resources_personnel": "нет"
            }, {
                "contractor_name": "Подрядчик2", "work_cost": "4000000", "availability_of_technology": "да",
                "tech_equipment": "средняя", "availability_of_production_facilities": "нет",
                "qualified_human_resources_personnel": "да"
            }, {
                "contractor_name": "Подрядчик3", "work_cost": "500000", "availability_of_technology": "нет",
                "tech_equipment": "низкая", "availability_of_production_facilities": "нет",
                "qualified_human_resources_personnel": "да"
            }, {
                "contractor_name": "Подрядчик4", "work_cost": "56969959", "availability_of_technology": "нет",
                "tech_equipment": "высокая", "availability_of_production_facilities": "нет",
                "qualified_human_resources_personnel": "да"
            }, {
                "contractor_name": "Подрядчик5", "work_cost": "4545343", "availability_of_technology": "да",
                "tech_equipment": "средняя", "availability_of_production_facilities": "да",
                "qualified_human_resources_personnel": "нет"
            },
        ]
        for contractor in contractors_list:
            contractors.create(session, **contractor)
        # restore criteria
        criteria_name_list = [
            "Стоимость работ", "Наличие эффективных технологий и опыт их применения", "Техническая оснащенность",
            "Наличие производственных мощностей, необходимых для обслуживания оборудования и инструментов",
            "Обеспеченность квалифицированным кадровым персоналом"
        ]
        for criteria_element in criteria_name_list:
            criteria.create_criteria(session, criteria_element)
