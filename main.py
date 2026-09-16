from datetime import datetime, date

suppliers = []

def create_supplier(name, inn):
    supplier_id = len(suppliers) + 1
    created_at = datetime.now()
    supplier = {"Id": supplier_id, "Название": name, "ИНН": inn, "Дата регистрации": f"{created_at:%d.%m.%Y}"}
    suppliers.append(supplier)

def get_all_suppliers():
    return suppliers

def get_supplier_by_id(supplier_id):
    for i in suppliers:
        if i["Id"] == supplier_id:
            return i
    return None

create_supplier("АО ООН", "125678910")
print(get_all_suppliers())
print(get_supplier_by_id(1))