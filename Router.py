from flask import Flask
from Controller.CrsdtlControlller import get_student_courses_by_reg,get_Fail_courses_by_reg
from Controller.STMTRController import login, signup
from Model.BERT_based import get_answer
from Controller.KnowledgeBaseController import get_all_knowledgebase,update_knowledgebase,add_knowledgebase,disable_knowledgebase_rule,enable_knowledgebase_rule

app=Flask(__name__)

from Model.Configure import Base,engine

# Base.metadata.create_all(engine)
# print("Table created successfully")
#============------------->       student   Login     <--------=========================



@app.route('/StudentLogin',methods=['POST'])
def studentLogin():
    return login()

@app.route('/signup', methods=['POST'])
def signUp():
    return signup()
# --------------------------> Bert Model respones Api

@app.route("/get_answer", methods=["POST"])
def Bertbase():
    try:
        return get_answer()
    except Exception as e:
        return {"error": str(e)}, 500

# ===========------------->     Show All Courses Details    <============--------------------

@app.route('/ShowAllCoursesDetail',methods=['GET'])
def get_Courses():
    return get_student_courses_by_reg()


@app.route('/ShowFailCoursesByReg',methods=['GET'])
def get_FailCourses():
    return get_Fail_courses_by_reg()



########################################## Knowledge Base ##################################
@app.route('/getKnowledgeBase',methods=['GET'])
def getKnowledgeBase():
    return get_all_knowledgebase()

@app.route('/updateKnowledgeBase',methods=['PUT'])
def updateKnowledgeBase():
    return update_knowledgebase()



@app.route('/addKnowledgeBase',methods=['POST'])
def addKnowledgeBase():
    return add_knowledgebase()

@app.route('/EnableStatusKnowledgeBase',methods=['PUT'])
def enableStatusKnowledgeBase():
    return enable_knowledgebase_rule()


@app.route('/DisableStatusKnowledgeBase',methods=['PUT'])
def DisableStatusKnowledgeBase():
    return disable_knowledgebase_rule()



if __name__=='__main__':
    app.run('0.0.0.0',debug=True)




