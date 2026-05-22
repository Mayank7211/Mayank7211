import requests

def test_api():
    base_url = "http://localhost:8000/api"
    
    # 1. Create a Tenant
    print("Creating Tenant...")
    tenant_data = {
        "name": "Dr. Smith Dental Clinic",
        "domain_name": "drsmithdental.com",
        "business_services": "Teeth cleaning, Root canals, Whitening",
        "faqs": "Q: Are you open on weekends? A: No, Mon-Fri only.",
        "tone_of_voice": "professional and friendly"
    }
    res = requests.post(f"{base_url}/tenants/", json=tenant_data)
    print("Response:", res.status_code, res.text)
    
    if res.status_code == 200:
        tenant_id = res.json()["id"]
        
        # 2. Create an Agent for the Tenant
        print(f"\nCreating Agent for Tenant {tenant_id}...")
        agent_data = {
            "name": "Smith Assistant"
        }
        res2 = requests.post(f"{base_url}/tenants/{tenant_id}/agents/", json=agent_data)
        print("Response:", res2.status_code, res2.text)
        
        if res2.status_code == 200:
            agent_id = res2.json()["id"]
            print(f"\nAgent created! ID: {agent_id}. The Widget Script can exactly point to this ID.")
            
            # 3. Test Chat
            print("\nTesting Chat with Agent...")
            chat_payload = {
                "message": "Do you do teeth whitening? And are you open on Saturday?",
                "history": []
            }
            chat_res = requests.post(f"{base_url}/chat/{agent_id}", json=chat_payload)
            print("Chat Response:", chat_res.status_code)
            if chat_res.status_code == 200:
                print("Agent says:", chat_res.json()["response"])
            else:
                print("Error Details:", chat_res.text)

if __name__ == "__main__":
    test_api()
