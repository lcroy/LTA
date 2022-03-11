from transformers import pipeline, Conversation


conversational_pipeline = pipeline("conversational")

text_to_speech_microsoft("Ok, now you can talk to GPT2 now")
change_topic = 0
pre_response = ''
conv1_start = speech_to_text_microsoft()
conv1 = Conversation(conv1_start)
result = str(conversational_pipeline([conv1]))
print(result)
index = result.rfind('>>')
text_to_speech_microsoft(result[index+2:])
print("===========================================")
while True:
    conv1_2 = speech_to_text_microsoft()
    if change_topic == 0:
        conv1.add_user_input(conv1_2)
    else:
        conv1 = Conversation(conv1_2)
        change_topic = 0
        pre_response = ''
    result = str(conversational_pipeline([conv1]))
    print(result)
    index = result.rfind('>>')
    print("===========================================")
    if len(result[index + 2:]) <= 3:
        text_to_speech_microsoft("Sorry, I cannot support such deeper conversation at this moment. Can we talk something else?")
        change_topic = 1
        continue
    if pre_response == result[index + 2:]:
        text_to_speech_microsoft(
            "Well, my answer is the same as the previous. Please ask me something else instead.")
        change_topic = 1
        continue
    else:
        pre_response = result[index + 2:]
    text_to_speech_microsoft(result[index + 2:])

#
# # print(str(conversational_pipeline([conv1])))
#
# index = result.find('>>')   #第一次出现的位置
# index2=result.find('>>',index+1)  #第二次出现的位置
#
# print(result[index2+2:])

#
#
# conv_start = "Hello"
# conv = Conversation(conv_start)
# result = str(conversational_pipeline([conv]))
# index = result.rfind('>>')
# text_to_speech_microsoft(result[index+2:])
# while True:
#     print("Please say anything to Max...")
#     conv_next = speech_to_text_microsoft()
#     conv.add_user_input(conv_next)
#     result = str(conversational_pipeline([conv]))
#     print(result)
#     index = result.rfind('>>')
#     text_to_speech_microsoft(result[index+2:])
