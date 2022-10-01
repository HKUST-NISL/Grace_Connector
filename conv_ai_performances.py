import argparse
import sys
import rospy
from std_msgs.msg import String
from hr_msgs.msg import TTS
from hr_msgs.srv import RunByName, RunByNameRequest
from hr_msgs.msg import Event

class ConvAIPerformance:
    
    performance_event_name = "/hr/control/performances/events"
    performance_event_topic_to_convas = "/grace_performance_event"
    performance_service_name = "/hr/control/performances/background/run_by_name"


    def __init__(self,node_name,topic_name):
        rospy.init_node(node_name)
        rospy.Subscriber(topic_name,String,self.speech_string_callback)
        rospy.Subscriber(self.performance_event_name,Event,self.performance_event_callback)
        self.performance_event_pub = rospy.Publisher(self.performance_event_topic_to_convas, String, queue_size=10)
        print("************ Connector Initialized ************")
        rospy.spin()

    def speech_string_callback(self,performance_sel):
        print ("Performance to be played: %s"%(performance_sel.data))

        #Play the performance by invoking the servie of HRSDK
        rospy.wait_for_service(self.performance_service_name)
    
        succ_flag = False
        try:
            run_by_name = rospy.ServiceProxy(self.performance_service_name, RunByName)
            
            request = RunByNameRequest()
            request.id = performance_sel.data

            response = run_by_name(request)

            succ_flag = response.success

        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
            succ_flag = False
        print("Performance play service success: %s"%(succ_flag))

    def performance_event_callback(self, event_msg):
        self.performance_event_pub.publish(String(event_msg.event))
        print("Performance play event: %s"%(event_msg.event))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("--topic", help="/grace_performance")
    args=parser.parse_args()
    conv_ai_performance = ConvAIPerformance("grace_listener",args.topic)
    
