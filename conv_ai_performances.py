import argparse
import sys
import rospy
from std_msgs.msg import String
from hr_msgs.msg import TTS
from hr_msgs.srv import RunByName, RunByNameRequest

class ConvAIPerformance:
    
    performance_service_name = "/hr/control/performances/background/run_by_name"

    def __init__(self,node_name,topic_name):
        rospy.init_node(node_name)
        rospy.Subscriber(topic_name,String,self.speech_string_callback)
        print("************ Connector Initialized ************")
        rospy.spin()

    def speech_string_callback(self,performance_sel):
        """_summary_

        Args:
            performance_sel (std_msgs.msg:string): relative path of the performance to be played
        """

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

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("--topic", help="/grace_performance")
    args=parser.parse_args()
    conv_ai_performance = ConvAIPerformance("grace_listener",args.topic)
    
