import requests

def login_via_api(email, password):
    try:
        payload = {
            "email": email,
            "password": password,
            "gcmInstanceId": "028c341c-1d10-482f-b6e8-f04d3acbbe6c",
            "fcmInstance": "-sD5yG:aF_Y4jhOvRWPpdsuul_Wh_05qk-jETGrZatZUnguOoc:bvI-MQBOqxMEGHDZR9xxaY_qexxb1PPQVZDBnB:aWeWx5uH9R6UPU_Vhu-ITr-m7Gd2AFHAcEALjWk1WnUy_I2LvGcIkO6Oztw0qk",
            "isIphone": "0"
        }

        response = requests.post(
            "https://api.sidly-platform-dev.com/mobile/Authentication",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        print("📡 Status code:", response.status_code)
        print("📨 Raw text:", response.text)

        if response.status_code == 200:
            data = response.json()
            if data.get("errorCode") == 0:
                return data
        return None

    except Exception as e:
        print("❌ API login error:", e)
        return None
