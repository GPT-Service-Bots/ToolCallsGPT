import httpx
import asyncio
import html

from functions.registry import register

# Заглушки
telegram_token = "7254347718:AAEhl4AyfYcDHwd8syfg4TmxHaqQuwgSU5w"
manager_ids = [1815995090]

# telegram_token = "6249292999:AAG8Sx22mEPe4716orn0qm1rbzlnPrujfik"
# manager_ids = [977249859]


@register
async def send_user_info_Vsg618t8(phone_number: str, additional_info: str, client_name: str):
    # Экранирование спецсимволов для HTML
    safe_phone = html.escape(phone_number)
    safe_info = html.escape(additional_info)
    safe_client_name = html.escape(client_name)

    message = f"📞 <b>Новый контакт:</b>\n<b>Номер:</b> {safe_phone}\n<b>Имя клиента:</b> {safe_client_name}\n<b>Инфо:</b> {safe_info}"
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

    async with httpx.AsyncClient() as client:
        tasks = [
            client.post(
                url,
                json={
                    "chat_id": manager_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
            )
            for manager_id in manager_ids
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

if __name__ == "__main__":
    pass