"""Точка входа (ООП-версия)."""
from datetime import date, datetime
from analytics import (
    get_low_stock_products, get_stock_balance,
    get_supplier_rating, get_total_spent,
)
from models import STATUS_FLOW, DeliveryItem
from services import (
    add_product, add_supplier, create_contract, create_delivery,
    delete_contract, delete_supplier, filter_deliveries_by_date,
    find_contract_by_id, find_delivery_by_id, find_product_by_id,
    find_supplier_by_id, get_all_deliveries, get_delivery_history,
    get_expiring_contracts, get_products_by_supplier,
    search_suppliers, show_contracts, show_deliveries,
    show_products, show_suppliers,
)
from storage import (
    load_contracts, load_deliveries, load_products, load_suppliers,
    save_contracts, save_deliveries, save_products, save_suppliers,
)
from utils import input_date, input_float, input_int, input_str

suppliers = load_suppliers()
products = load_products(suppliers)
contracts = load_contracts(suppliers)
deliveries = load_deliveries(suppliers, contracts, products)

def menu() -> None:
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
    print("--- Поставки ---")
    print("19. Создать поставку")
    print("20. Показать поставки")
    print("21. Изменить статус поставки")
    print("22. Принять поставку")
    print("23. Акт приёмки")
    print("24. История поставок")
    print("25. Фильтр поставок по дате")
    print("--- Аналитика ---")
    print("26. Общая сумма затрат")
    print("27. Рейтинг поставщиков")
    print("28. Остатки на складе")
    print("29. Товары с низким остатком")
    print("0.  Выход")


def main() -> None:
    suppliers = load_suppliers()
    products = load_products(suppliers)
    contracts = load_contracts(suppliers)
    deliveries = load_deliveries(suppliers, contracts, products)

    while True:
        menu()
        choice = input_int("Выберите действие: ")

        match choice:
            case 0:
                save_suppliers(suppliers)
                save_products(products)
                save_contracts(contracts)
                save_deliveries(deliveries)
                print("Данные сохранены. Выход.")
                break

            case 1:
                show_suppliers(suppliers)
            case 2:
                add_supplier(suppliers, input_str("Название: "),
                             input_str("ИНН: "))
            case 3:
                show_suppliers(search_suppliers(
                    suppliers, input_str("Запрос: ")))
            case 4:
                sid = input_int("ID поставщика: ")
                s = find_supplier_by_id(suppliers, sid)
                if s is None:
                    print("Поставщик не найден.")
                else:
                    s.update(name=input_str("Новое название: "))
                    print("Поставщик обновлён.")
            case 5:
                sid = input_int("ID поставщика: ")
                print("Удалено." if delete_supplier(suppliers, products,
                                                    contracts, sid)
                      else "Нельзя удалить: поставщик не найден "
                           "или на него есть ссылки.")

            case 6:
                show_products(products)
            case 7:
                sid = input_int("ID поставщика: ")
                s = find_supplier_by_id(suppliers, sid)
                if s is None:
                    print("Поставщик не найден.")
                else:
                    add_product(products, input_str("Название: "),
                                input_float("Цена: "), s)
            case 8:
                sid = input_int("ID поставщика: ")
                s = find_supplier_by_id(suppliers, sid)
                if s is None:
                    print("Поставщик не найден.")
                else:
                    show_products(get_products_by_supplier(products, s))
            case 9:
                pid = input_int("ID товара: ")
                p = find_product_by_id(products, pid)
                if p is None:
                    print("Товар не найден.")
                else:
                    p.update(name=input_str("Новое название: "),
                             price=input_float("Новая цена: "))
                    print("Товар обновлён.")
            case 10:
                pid = input_int("ID товара: ")
                p = find_product_by_id(products, pid)
                if p is None:
                    print("Товар не найден.")
                else:
                    products.remove(p)
                    print("Товар удалён.")
            case 11:
                pid = input_int("ID товара: ")
                sid = input_int("ID нового поставщика: ")
                p = find_product_by_id(products, pid)
                s = find_supplier_by_id(suppliers, sid)
                if p is None or s is None:
                    print("Товар или поставщик не найден.")
                else:
                    p.assign_supplier(s)
                    print("Поставщик назначен.")

            case 12:
                show_contracts(contracts)
            case 13:
                sid = input_int("ID поставщика: ")
                s = find_supplier_by_id(suppliers, sid)
                if s is None:
                    print("Поставщик не найден.")
                else:
                    number = input_str("Номер: ")
                    start = input_date("Начало (ДД.ММ.ГГГГ): ")
                    end = input_date("Окончание (ДД.ММ.ГГГГ): ")
                    if end <= start:
                        print("Окончание должно быть позже начала.")
                    else:
                        create_contract(contracts, s, number, start, end)
            case 14:
                cid = input_int("ID договора: ")
                c = find_contract_by_id(contracts, cid)
                if c is None:
                    print("Договор не найден.")
                else:
                    c.update(number=input_str("Новый номер: "),
                             start_date=input_date("Новое начало: "),
                             end_date=input_date("Новое окончание: "))
                    print("Договор обновлён.")
            case 15:
                cid = input_int("ID договора: ")
                print("Удалено." if delete_contract(contracts, deliveries,
                                                    cid)
                      else "Нельзя удалить: договор не найден "
                           "или на него есть ссылки.")
            case 16:
                cid = input_int("ID договора: ")
                c = find_contract_by_id(contracts, cid)
                if c is None:
                    print("Договор не найден.")
                else:
                    status = input_str("Новый статус "
                                       "(активен/истёк/расторгнут): ")
                    print("Изменено." if c.change_status(status)
                          else "Недопустимый статус.")
            case 17:
                cid = input_int("ID договора: ")
                c = find_contract_by_id(contracts, cid)
                if c is None:
                    print("Договор не найден.")
                else:
                    c.terminate()
                    print("Договор расторгнут.")
            case 18:
                days = input_int("За сколько дней? ")
                show_contracts(get_expiring_contracts(contracts, days))

            case 19:
                sid = input_int("ID поставщика: ")
                cid = input_int("ID договора: ")
                s = find_supplier_by_id(suppliers, sid)
                c = find_contract_by_id(contracts, cid)
                if s is None or c is None:
                    print("Поставщик или договор не найден.")
                else:
                    ddate = input_date("Дата поставки (ДД.ММ.ГГГГ): ")
                    items: list[DeliveryItem] = []
                    while True:
                        pid = input_int("ID товара (0 — закончить): ")
                        if pid == 0:
                            break
                        p = find_product_by_id(products, pid)
                        if p is None:
                            print("Товар не найден.")
                            continue
                        qty = input_int("Количество: ")
                        price = input_float("Цена за единицу: ")
                        items.append(DeliveryItem(p, qty, price))
                    if not items:
                        print("Поставка без позиций — отменено.")
                    else:
                        create_delivery(deliveries, s, c, ddate, items)
                        print("Поставка создана.")
            case 20:
                show_deliveries(get_all_deliveries(deliveries))
            case 21:
                did = input_int("ID поставки: ")
                d = find_delivery_by_id(deliveries, did)
                if d is None:
                    print("Поставка не найдена.")
                else:
                    print("Текущий статус:", d.status)
                    print("Следующий:", d.next_status())
                    new_status = input_str("Новый статус "
                                           f"({'/'.join(STATUS_FLOW)}): ")
                    print("Изменено." if d.change_status(new_status)
                          else "Недопустимый переход.")
            case 22:
                did = input_int("ID поставки: ")
                d = find_delivery_by_id(deliveries, did)
                if d is None:
                    print("Поставка не найдена.")
                else:
                    print("Принята." if d.accept()
                          else "Приёмка возможна только из статуса «В пути».")
            case 23:
                did = input_int("ID поставки: ")
                d = find_delivery_by_id(deliveries, did)
                if d is None:
                    print("Поставка не найдена.")
                else:
                    print(d.acceptance_act())
            case 24:
                sid = input_int("ID поставщика (0 — все): ")
                if sid == 0:
                    show_deliveries(get_delivery_history(deliveries))
                else:
                    s = find_supplier_by_id(suppliers, sid)
                    if s is None:
                        print("Поставщик не найден.")
                    else:
                        show_deliveries(get_delivery_history(deliveries, s))
            case 25:
                start = input_date("Начало (ДД.ММ.ГГГГ): ")
                end = input_date("Окончание (ДД.ММ.ГГГГ): ")
                show_deliveries(filter_deliveries_by_date(
                    deliveries, start, end))

            case 26:
                start = input_date("Начало (ДД.ММ.ГГГГ): ")
                end = input_date("Окончание (ДД.ММ.ГГГГ): ")
                print(f"Итого: {get_total_spent(deliveries, start, end):.2f}")
            case 27:
                for supplier, total in get_supplier_rating(deliveries):
                    print(f"{supplier.name}: {total:.2f} руб.")
            case 28:
                for pid, qty in get_stock_balance(products).items():
                    print(f"Товар #{pid}: {qty}")
            case 29:
                threshold = input_int("Порог: ")
                for p in get_low_stock_products(products, threshold):
                    print(p)

            case _:
                print("Неверный выбор. Повторите ввод.")


if __name__ == "__main__":
    main()