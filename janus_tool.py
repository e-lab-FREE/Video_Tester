import json
import requests
from pprint import pprint
plugin_id = 0
session_id = 0
server = "146.193.41.143"
#server = "localhost"

def connect_janus_stream(apisecret):
    
    data = {
    "janus": "create",
    "transaction": "transaction-x",
    "apisecret" : str(apisecret)
    }
    print(f'http://{server}:8088/janus/')
    response = requests.post(f'http://{server}:8088/janus/', json = data)
    print(response)

    json_ret = response.json()

    if(response.status_code != 200 or  json_ret['janus']!='success'):
        print("ERROR")
        print(response.json())
        return (0, 0)

    #get session_id
    session_id = json_ret['data']['id']

    #print(session_id)

    #connect to streamming plugin

    data = {
    "janus" : "attach",
    "plugin" : "janus.plugin.streaming",
    "transaction": "transaction-x",
    "apisecret": str(apisecret)
    }

    response = requests.post(f'http://{server}:8088/janus/'+str(session_id), json = data)
    json_ret = response.json()
    if(response.status_code != 200 or  json_ret['janus']!='success'):
        print("ERROR")
        print(response.json())
        return (0, 0)

#    print(response.json())
#   print('OK')

    plugin_id = json_ret['data']['id']
    #print("plugin_id "+str(plugin_id))
    return   (plugin_id, session_id)

def list_streams(apisecret):
    plugin_id, session_id = connect_janus_stream(apisecret)
    ret_list = []
    #print(session_id)
    #print(plugin_id)

    if session_id ==0 or plugin_id == 0:
        return -1

    data = {
        "janus": "message",
        "body": {
            "request": "list"
        },
        "transaction": "transaction-x",
        "apisecret": apisecret
    }

    #print(f'http://localhost:8088/janus/{session_id}/{plugin_id}'    )
    response = requests.post(f'http://{server}:8088/janus/{session_id}/{plugin_id}', json = data)
    json_ret = response.json()
    try:
        return json_ret['plugindata']['data']['list']
    except:
        return []
    


def stream_info(apisecret, stream_id):
    plugin_id, session_id = connect_janus_stream(apisecret)
    ret_list = []
    #print(session_id)
    #print(plugin_id)

    if session_id ==0 or plugin_id == 0:
        return []

    data = {
            "janus": "message",
            "body": {
                "request": "info",
                "id": int(stream_id)
            },
            "transaction": "transaction-x",
            "apisecret": apisecret
        }
    print(f'http://localhost:8088/janus/{session_id}/{plugin_id}'    )
    response = requests.post(f'http://{server}:8088/janus/{session_id}/{plugin_id}', json = data)
    json_ret = response.json()
    try: 
        return json_ret['plugindata']['data']['info']
    except:
        return {}




def create_stream(name, description, port, apisecret,stream_admin_key):
    plugin_id, session_id = connect_janus_stream(apisecret)

    if session_id ==0 or plugin_id == 0:
        return {}

    data = {
        "janus": "message",
        "body": {
            
                "request" : "create",
                #"admin_key" : "<plugin administrator key; mandatory if configured>",
                "type" : "rtp",
                #"id" : <unique ID to assign the mountpoint; optional, will be chosen by the server if missing>,
                "name" : name,
                "description" : description,
                #"metadata" : "<metadata of mountpoint; optional>",
                #"secret" : "<secret to query/edit the mountpoint later; optional>",
                #"pin" : "<PIN required for viewers to access mountpoint; optional>",
                #"is_private" : <true|false, whether the mountpoint should be listable; true by default>,
                "audio" : False,
                "video" : True,
                #"data" : <true|false, whether the mountpoint will have datachannels; false by default>,
                "permanent" : True,
                "videoport" : 0,  #Porto onde são recebidos os pacotes do stream (ver comando de gstreamer) 
#                "videoport" : int(port),  #Porto onde são recebidos os pacotes do stream (ver comando de gstreamer) 
                "videopt" : 126,  #nao alterar 
                "videortpmap" : "H264/90000",  #nao alterar 
                "videofmtp" : "profile-level-id=42e01f;packetization-mode=1", #nao alterar 
                "admin_key": stream_admin_key
            
        },
        "transaction": "transaction-x",
        "apisecret": apisecret,
    }

    #print(f'http://localhost:8088/janus/{session_id}/{plugin_id}')
    response = requests.post(f'http://{server}:8088/janus/{session_id}/{plugin_id}', json = data)
    json_ret = response.json()
    if(json_ret['janus']!= 'success'):
        return {}
    json_plugin = json_ret['plugindata']['data']
    try: 
        return json_plugin['stream'] 
    except:
        print(json_plugin['error'])
        return {}
 

if __name__ == "__main__":
    #secret = input('Janus Secret ')
    stream_admin_key = str(input("Streaming admin key: "))
    apisecret = "janurocks"
    while True:
        print("L - List Streams\nN - New Strem\nD - Delete Stream\nI - Stream Info")
        option = input('L I N D :')
        if option == 'L':
            pprint(list_streams(apisecret))
        if option == 'I':
            stream_id = input("Stream ID :")
            pprint(stream_info(apisecret, stream_id))
        if option == 'N':
            s_name = input("Stream name :")
            s_description = input("Stream description :")
            #s_port = input("Stream port :")
            pprint(create_stream(s_name, s_description, 0, apisecret, stream_admin_key))