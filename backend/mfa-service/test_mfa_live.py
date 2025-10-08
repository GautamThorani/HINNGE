import requests
import pyotp

def test_mfa_live():
    print("Testing MFA Service Live...")
    
    user_id = "user_993bfcc1"  
    
    print("1. Setting up MFA...")
    setup_response = requests.post(f"http://localhost:8000/mfa/setup/{user_id}")
    setup_data = setup_response.json()
    secret = setup_data["secret"]
    print(f"Secret: {secret}")
    print(f" QR Code generated: {len(setup_data['qr_code'])} chars")

    print("2. Generating TOTP code...")
    totp = pyotp.TOTP(secret)
    current_code = totp.now()
    print(f"Current TOTP code: {current_code}")
    
    print("3. Verifying TOTP code...")
    verify_data = {
        "user_id": user_id,
        "token": current_code
    }
    verify_response = requests.post("http://localhost:8000/mfa/verify", json=verify_data)
    verify_result = verify_response.json()
    print(f"Verification: {verify_result}")
    
    print("4. Checking MFA status...")
    status_response = requests.get(f"http://localhost:8000/mfa/status/{user_id}")
    status_data = status_response.json()
    print(f"MFA Enabled: {status_data['mfa_enabled']}")

    print("5. Testing with wrong code...")
    wrong_verify = {
        "user_id": user_id,
        "token": "000000"
    }
    wrong_response = requests.post("http://localhost:8000/mfa/verify", json=wrong_verify)
    wrong_result = wrong_response.json()
    print(f"Wrong code rejected: {wrong_result}")

if __name__ == "__main__":
    test_mfa_live()