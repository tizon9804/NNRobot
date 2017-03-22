import json
from watson_developer_cloud import ConversationV1
import Speak as sp
import TextToSpeak as txtSp

class Watson:
    def __init__(self):
        self.speak = sp.Speak()
        self.txtSp = txtSp.TextToSpeak()
        self.conversation = ConversationV1(
            username='abb1f14f-2099-4718-b564-b357f56a4a80',
            password='MYXIM5zNXcHQ',
            version='2016-09-20')
        # replace with your own workspace_id
        self.workspace_id = '114f8365-2e75-4fee-8b98-0df2527972bf'

    def talk(self,text):
        response = self.conversation.message(workspace_id=self.workspace_id, message_input={
            'text': text})
        parse = json.dumps(response,indent=2)
        parse = json.loads(parse)
        resp = parse["output"]["text"]
        print resp
        # When you send multiple requests for the same conversation, include the
        # context object from the previous response.
        # response = conversation.message(workspace_id=workspace_id, message_input={
        # 'text': 'turn the wipers on'},
        #                                context=response['context'])
        # print(json.dumps(response, indent=2))

        return resp






