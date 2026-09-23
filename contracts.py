from datetime import date, datetime
from suppliers import _next_id

STATUS_ACTIVE = "ACTIVE"
STATUS_EXPIRED = "EXPIRED"
STATUS_TERMINATED = "TERMINATED"

VALID_STATUSES = (STATUS_ACTIVE, STATUS_EXPIRED, STATUS_TERMINATED)


def create_contract(contracts: list[dict], supplier_id: int, product_id: int, number: str, start: date,
                    end: date) -> dict:
    contract = {
        "id": _next_id(contracts),
        "supplier_id": supplier_id,
        "product_id": product_id,
        "number": number,
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "status": STATUS_ACTIVE
    }
    contracts.append(contract)
    return contract


def get_contract_by_id(contracts: list[dict], contract_id: int) -> dict | None:
    for contract in contracts:
        if contract["id"] == contract_id:
            return contract
    return None


def get_all_contracts(contracts: list[dict]) -> None:
    if not contracts:
        print("No contracts found.")
        return
    for contract in contracts:
        print(
            f"[{contract['id']}] №{contract['number']} | поставщик #{contract['supplier_id']} | товар #{contract['product_id']}"
            f"| {contract['start_date']}-{contract['end_date']} | {contract['status']}")


def update_contract(contracts: list[dict], contract_id: int, number: str | None = None, start: date | None = None,
                    end: date | None = None) -> bool:
    contract = get_contract_by_id(contracts, contract_id)
    if contract is None:
        return False
    if number is not None:
        contract["number"] = number
    if start is not None:
        contract["start_date"] = start.strftime("%Y-%m-%d")
    if end is not None:
        contract["end_date"] = end.strftime("%Y-%m-%d")
    return True


def delete_contract(contracts: list[dict], contract_id: int) -> bool:
    contract = get_contract_by_id(contracts, contract_id)
    if contract is None:
        return False
    contract.remove(contract)
    return True


def change_contract_status(contracts: list[dict], contract_id: int, status: str) -> bool:
    if status not in VALID_STATUSES:
        return False
    contract = get_contract_by_id(contracts, contract_id)
    if contract is None:
        return False
    contract["status"] = status
    return True


def terminate_contract(contracts: list[dict], contract_id: int) -> bool:
    contract = get_contract_by_id(contracts, contract_id)
    if contract is None:
        return False
    contract["status"] = STATUS_TERMINATED
    return True


def get_expired_contracts(contracts: list[dict], days: int = 30) -> list[dict]:
    today = date.today()
    result = []
    for contract in contracts:
        if contract["status"] != STATUS_EXPIRED:
            continue
        end = datetime.strptime(contract["end_date"], "%Y-%m-%d").date()
        if 0 <= (end - today).days <= days:
            result.append(contract)
    return result
