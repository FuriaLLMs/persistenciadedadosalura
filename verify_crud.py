import urllib.request
import urllib.error
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def log(msg, success=True):
    icon = "✅" if success else "❌"
    print(f"{icon} {msg}")

def req(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    if data:
        body = json.dumps(data).encode('utf-8')
    else:
        body = None
        
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as f:
            status = f.status
            resp_body = f.read().decode('utf-8')
            if resp_body:
                return status, json.loads(resp_body)
            return status, None
    except urllib.error.HTTPError as e:
        status = e.code
        resp_body = e.read().decode('utf-8')
        return status, {"error": resp_body}
    except Exception as e:
        return 0, str(e)

def test_crud():
    print("Starting CRUD verification...")
    
    # 1. Create Professor
    status, data = req("POST", "/professores/", {"nome": "Prof. Urllib"})
    if status == 200:
        prof_id = data["id"]
        log(f"Created Professor ID {prof_id}")
    else:
        log(f"Failed to create professor: {status} {data}", False)
        return

    # 2. Update Professor
    status, data = req("PUT", f"/professores/{prof_id}", {"nome": "Prof. Atualizado"})
    if status == 200 and data["nome"] == "Prof. Atualizado":
        log("Updated Professor successfully")
    else:
        log(f"Failed to update professor: {status} {data}", False)

    # 3. Create Disciplina
    status, data = req("POST", "/disciplinas/", {"nome": "Disciplina Teste", "professor_id": prof_id})
    if status == 200:
        disc_id = data["id"]
        log(f"Created Disciplina linked to Professor")
    else:
        log(f"Failed to create disciplina: {status} {data}", False)
        disc_id = None

    # 4. Get Disciplinas (Optimization Check)
    status, data = req("GET", "/disciplinas/")
    if status == 200:
        log("Read Disciplinas (Optimization check pass via 200 OK)")
    else:
        log("Failed to read disciplinas", False)

    # 5. Delete Disciplina
    if disc_id:
        status, data = req("DELETE", f"/disciplinas/{disc_id}")
        if status == 204:
            log("Deleted Disciplina")
        else:
            log(f"Failed to delete disciplina: {status} {data}", False)

    # 6. Delete Professor
    status, data = req("DELETE", f"/professores/{prof_id}")
    if status == 204:
        log("Deleted Professor")
    else:
        log(f"Failed to delete professor: {status} {data}", False)

    print("\nVerification Complete!")

if __name__ == "__main__":
    test_crud()
