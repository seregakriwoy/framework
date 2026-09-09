# Система управления поставщиками

## Назначение проекта
Проект удобно управлять своими система поставок, поставщиками, договорами и товарами.

## Целевая аудитория
Целевой аудиторией проекта является малый и средний бизнес, у которого не так много ресурсов на разработку и поддержание собственных систем управления поставками.

## Предметная область
Предметной областью проекта является логистика и управление закупками.

## Основные сущности
- Поставщик
- Товар
- Договор
- Поставка

## Основные функции
### Поставщики
- create_supplier()
- get_all_suppliers()
- get_supplier_by_id()
- update_supplier()
- delete_supplier()
- search_suppliers()

### Товары
- add_product()
- get_all_products()
- get_product_by_id()
- update_product()
- delete_product()
- get_products_by_supplier()
- assign_supplier_to_product()

### Договоры
- create_contract()
- get_all_contracts()
- get_contract_by_id()
- update_contract()
- delete_contract()
- change_contract_status()
- upload_contract_file()
- get_expiring_contracts()
- terminate_contract()

### Поставки
- create_delivery_order()
- get_all_deliveries()
- get_delivery_by_id()
- change_delivery_status()
- accept_delivery()
- get_delivery_history()
- generate_acceptance_act()
- filter_deliveries_by_date()

### Аналитика
- get_total_spent()
- get_supplier_rating()
- get_stock_balance()
- get_low_stock_products()

## План развития
На следующих этапах планируется:
- разработка веб-приложения;
- подключение базы данных;
- реализация пользователей;
- разработка API;
- контейнеризация приложения;
- настройка CI/CD.
