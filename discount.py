def calculate_price(price, has_orders):
    # Логика ветвления по блок-схеме:
    # Если за месяц заказов НЕТ (not has_orders) -> применяется скидка 25%
    if not has_orders:
        return price * 0.75
    else:
        return price

# Проверочный запуск функции (Вывод: цена)
if __name__ == "__main__":
    toy_name = "Плюшевый Мишка"
    base_price = 1000.00
    
    print(f"Товар: {toy_name}, Базовая цена: {base_price} руб.")
    
    # Сценарий 1: У клиента ЕСТЬ заказы за месяц (has_orders = True)
    price_1 = calculate_price(base_price, has_orders=True)
    print(f"Есть заказы за месяц? Да  -> Итоговая цена: {price_1} руб. (Без изменений)")
    
    # Сценыыарий 2: У клиента НЕТ заказов за месяц (has_orders = False)
    price_2 = calculate_price(base_price, has_orders=False)
    print(f"Есть заказы за месяц? Нет -> Итоговая цена: {price_2} руб. (Скидка 25% применена)")
