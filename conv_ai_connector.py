import argparse
import sys
import rospy
from std_msgs.msg import String
from hr_msgs.msg import TTS

class ConvAIConnector:
    
    prosody_rate_tag_XSLOW = "<prosody rate=\"x-slow\">"; 
    prosody_rate_tag_SLOW = "<prosody rate=\"slow\">"; 
    prosody_rate_tag_MEDIUM = "<prosody rate=\"medium\">"; 
    prosody_rate_tag_FAST = "<prosody rate=\"fast\">"; 
    prosody_rate_tag_XFAST = "<prosody rate=\"x-fast\">"; 
    prosody_end_Tag = "</prosody>";    

    lang_en_us = "en-US"
    lang_cantonese = "yue-Hant-HK"


    def __init__(self,node_name,topic_name,language_code):
        self.language_code = language_code
        rospy.init_node(node_name)
        rospy.Subscriber(topic_name,String,self.speech_string_callback)
        self.ttsPub = rospy.Publisher('/hr/control/speech/say',TTS,queue_size=10)
        rospy.spin()

    def speech_string_callback(self,received_data):
        """_summary_

        Args:
            data (std_msgs.msg:string): string provided by the conv ai for Grace to speak
        """

        print ("Received speech content is: %s"%(received_data.data))

        #Compose TTS
        hr_msg = TTS()
        #(1) Text content
        text_to_speak = received_data.data
        #(2) Language code
        hr_msg.lang = self.language_code
        #(3) Prosody tags
        prosody_rate_tag = self.prosody_rate_tag_MEDIUM
        #(4) Final tts string
        hr_msg.text = prosody_rate_tag + received_data.data + self.prosody_end_Tag
        #(5) Publish to trigger speech
        self.ttsPub.publish(hr_msg)



if __name__ == '__main__':


    parser=argparse.ArgumentParser()
    parser.add_argument("--language_code", help="English: en-US Cantonese: yue-Hant-HK")
    parser.add_argument("--topic", help="/grace_chat")
    args=parser.parse_args()

    conv_ai_connector = ConvAIConnector("grace_listener",args.topic,args.language_code)

