#!/usr/bin/env python3

import sys
import requests
import json

if len(sys.argv)  == 2:
    print("Provide only remote IP address of host and its port")
    print("orious_test.py <remote_ip> <port>")
    exit(1)

IP = sys.argv[1]
PORT = sys.argv[2]
URI = f'http://{IP}:{PORT}'
notes = []

headers  = {'Content-type': 'application/json', 'charset': 'utf-8'}

def can_user_get_notes(URI):
    res = requests.get(f'{URI}/notes')
    notes = json.loads(res.content.decode('utf-8'))

    if notes or res.status_code == 200:
        return notes

    return False

def can_user_create_note(URI):
    note_to_add = {
            "title": "User can create Title note",
            "content": "User can create Content note"
    }
    

    res = requests.post(f'{URI}/notes', data=json.dumps(note_to_add), headers=headers)

    if res.status_code == 201:
        return True
    else:
        return False

    
       
def can_user_update_note(URI, current_note):
    note_to_update = {
            "title": "User can update notes title",
            "content": "User can update notes content"
    }

    res = requests.put(f"{URI}/notes/{current_note['_id']}", data=json.dumps(note_to_update), headers=headers)

    if res.status_code == 200:
        return True
    else:
        return False

def can_user_delete_note(URI, current_note):
    
    res = requests.delete(f"{URI}/notes/{current_note['_id']}", headers=headers)

    if res.status_code == 200:
        return True
    else:
        return False

try:
    notes = can_user_get_notes(URI)
    ableGet = True if notes else False  

    ableCreate = can_user_create_note(URI)
    ableUpdate = can_user_update_note(URI, notes[0])
    ableDelete = can_user_delete_note(URI, notes[len(notes) - 2])

except:
    print("Tests failed, unreachable endpoints")
    sys.exit(1)

if ableGet and ableCreate and ableUpdate and ableDelete:
        print("Tests were successful")
        sys.exit(0)
else:
    print("Test(s) failed:")
    print("Can get notes: ", ableGet)
    print("Can create notes: ", ableCreate)
    print("Can update notes: ", ableUpdate)
    print("Can delete notes: ", ableDelete)
    sys.exit(1)

