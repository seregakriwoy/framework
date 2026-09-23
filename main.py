"""Точка входа в приложение «Система управления поставщиками»."""
from contracts import (
    change_contract_status,
    create_contract,
    delete_contract,
    get_contract_by_id,
    get_expired_contracts,
    get_all_contracts,
    terminate_contract,
    update_contract,
)
from products import (
    add_products,
    assign_supplier_to_products,
    delete_products,
    get_product_by_id,
    get_products_by_supplier,
    get_all_products,
    update_products,
)
from storage import (
    load_contracts,
    load_products,
    load_suppliers,
    save_contracts,
    save_products,
    save_suppliers,
)
from suppliers import (
    create_supplier,
    delete_supplier,
    get_supplier_by_id,
    search_suppliers,
    get_all_suppliers,
    update_supplier,
)
from utils import input_date, input_float, input_int, input_str


def menu() -> None:
    """Вывести главное меню."""
    print("\n=== Система управления поставщиками ===")
    print("--- Поставщики ---")
    print("1.  Показать поставщиков")
    print("2.  Добавить поставщика")
    print("3.  Найти поставщика")
    print("4.  Обновить поставщика")
    print("5.  Удалить поставщика")
    print("--- Товары ---")
    print("6.  Показать товары")
    print("7.  Добавить товар")
    print("8.  Товары поставщика")
    print("9.  Обновить товар")
    print("10. Удалить товар")
    print("11. Назначить поставщика товару")
    print("--- Договоры ---")
    print("12. Показать договоры")
    print("13. Добавить договор")
    print("14. Обновить договор")
    print("15. Удалить договор")
    print("16. Изменить статус договора")
    print("17. Расторгнуть договор")
    print("18. Истекающие договоры")
    print("--- Прочее ---")
    print("0.  Выход")


# ---------- Обработчики поставщиков ----------

def handle_show_suppliers(suppliers, products, contracts) -> None:
    get_all_suppliers(suppliers)


def handle_add_supplier(suppliers, products, contracts) -> None:
    name = input_str("Название: ")
    inn = input_str("ИНН: ")
    create_supplier(suppliers, name, inn)
    print("Поставщик добавлен.")


def handle_search_suppliers(suppliers, products, contracts) -> None:
    query = input_str("Запрос (название или ИНН): ")
    get_all_suppliers(search_suppliers(suppliers, query))


def handle_update_supplier(suppliers, products, contracts) -> None:
    sid = input_int("ID поставщика: ")
    supplier = get_supplier_by_id(suppliers, sid)
    if supplier is None:
        print("Поставщик не найден.")
        return
    name = input_str("Новое название: ")
    update_supplier(suppliers, sid, name=name)
    print("Поставщик обновлён.")


def handle_delete_supplier(suppliers, products, contracts) -> None:
    sid = input_int("ID поставщика: ")
    # Проверка ссылочной целостности: нельзя удалить,
    # если у поставщика есть товары или договоры.
    if any(p["supplier_id"] == sid for p in products):
        print("Нельзя удалить: у поставщика есть товары.")
        return
    if any(c["supplier_id"] == sid for c in contracts):
        print("Нельзя удалить: у поставщика есть договоры.")
        return
    if delete_supplier(suppliers, sid):
        print("Поставщик удалён.")
    else:
        print("Поставщик не найден.")


# ---------- Обработчики товаров ----------

def handle_show_products(suppliers, products, contracts) -> None:
    get_all_products(products)


def handle_add_product(suppliers, products, contracts) -> None:
    name = input_str("Название товара: ")
    price = input_float("Цена: ")
    sid = input_int("ID поставщика: ")
    if get_supplier_by_id(suppliers, sid) is None:
        print("Поставщик не найден.")
        return
    add_products(products, name, price, sid)
    print("Товар добавлен.")


def handle_products_by_supplier(suppliers, products, contracts) -> None:
    sid = input_int("ID поставщика: ")
    get_all_products(get_products_by_supplier(products, sid))


def handle_update_product(suppliers, products, contracts) -> None:
    pid = input_int("ID товара: ")
    if get_product_by_id(products, pid) is None:
        print("Товар не найден.")
        return
    name = input_str("Новое название: ")
    price = input_float("Новая цена: ")
    update_products(products, pid, name=name, price=price)
    print("Товар обновлён.")


def handle_delete_product(suppliers, products, contracts) -> None:
    pid = input_int("ID товара: ")
    if delete_products(products, pid):
        print("Товар удалён.")
    else:
        print("Товар не найден.")


def handle_assign_supplier(suppliers, products, contracts) -> None:
    pid = input_int("ID товара: ")
    sid = input_int("ID нового поставщика: ")
    if get_supplier_by_id(suppliers, sid) is None:
        print("Поставщик не найден.")
        return
    if assign_supplier_to_products(products, pid, sid):
        print("Поставщик назначен.")
    else:
        print("Товар не найден.")


# ---------- Обработчики договоров ----------

def handle_show_contracts(suppliers, products, contracts) -> None:
    get_all_contracts(contracts)


def handle_add_contract(suppliers, products, contracts) -> None:
    sid = input_int("ID поставщика: ")
    if get_supplier_by_id(suppliers, sid) is None:
        print("Поставщик не найден.")
        return
    number = input_str("Номер договора: ")
    start = input_date("Дата начала (ДД.ММ.ГГГГ): ")
    end = input_date("Дата окончания (ДД.ММ.ГГГГ): ")
    if end <= start:
        print("Дата окончания должна быть позже даты начала.")
        return
    create_contract(contracts, sid, number, start, end)
    print("Договор создан.")


def handle_update_contract(suppliers, products, contracts) -> None:
    cid = input_int("ID договора: ")
    if get_contract_by_id(contracts, cid) is None:
        print("Договор не найден.")
        return
    number = input_str("Новый номер: ")
    start = input_date("Новая дата начала (ДД.ММ.ГГГГ): ")
    end = input_date("Новая дата окончания (ДД.ММ.ГГГГ): ")
    if end <= start:
        print("Дата окончания должна быть позже даты начала.")
        return
    update_contract(contracts, cid, number=number, start=start, end=end)
    print("Договор обновлён.")


def handle_delete_contract(suppliers, products, contracts) -> None:
    cid = input_int("ID договора: ")
    if delete_contract(contracts, cid):
        print("Договор удалён.")
    else:
        print("Договор не найден.")


def handle_change_contract_status(suppliers, products, contracts) -> None:
    cid = input_int("ID договора: ")
    status = input_str("Новый статус (активен/истёк/расторгнут): ")
    if change_contract_status(contracts, cid, status):
        print("Статус изменён.")
    else:
        print("Договор не найден или недопустимый статус.")


def handle_terminate_contract(suppliers, products, contracts) -> None:
    cid = input_int("ID договора: ")
    if terminate_contract(contracts, cid):
        print("Договор расторгнут.")
    else:
        print("Договор не найден.")


def handle_expiring_contracts(suppliers, products, contracts) -> None:
    days = input_int("За сколько дней считать истекающими? ")
    get_all_contracts(get_expired_contracts(contracts, days=days))


# ---------- Карта обработчиков ----------

HANDLERS: dict[int, callable] = {
    1: handle_show_suppliers,
    2: handle_add_supplier,
    3: handle_search_suppliers,
    4: handle_update_supplier,
    5: handle_delete_supplier,
    6: handle_show_products,
    7: handle_add_product,
    8: handle_products_by_supplier,
    9: handle_update_product,
    10: handle_delete_product,
    11: handle_assign_supplier,
    12: handle_show_contracts,
    13: handle_add_contract,
    14: handle_update_contract,
    15: handle_delete_contract,
    16: handle_change_contract_status,
    17: handle_terminate_contract,
    18: handle_expiring_contracts,
}


# ---------- Точка входа ----------

def main() -> None:
    """Точка запуска: загрузка данных, меню, сохранение."""
    suppliers = load_suppliers()
    products = load_products()
    contracts = load_contracts()

    while True:
        menu()
        choice = input_int("Выберите действие: ")

        match choice:
            case 0:
                save_suppliers(suppliers)
                save_products(products)
                save_contracts(contracts)
                print("Данные сохранены. Выход.")
                break
            case _ if choice in HANDLERS:
                HANDLERS[choice](suppliers, products, contracts)
            case _:
                print("Неверный выбор. Повторите ввод.")


if __name__ == "__main__":
    main()