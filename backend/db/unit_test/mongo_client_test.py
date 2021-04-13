
import sys
sys.path.append('E:\github\examOnline')


from db.mongo_client import MyMongoClient
from gen.proto import db_pb2, api_pb2

from google.protobuf import json_format

def drop_all_collections(client):
    print('===== drop collection =====')
    print(client.choice_problem_collection.drop())
    print(client.judge_problem_collection.drop())

def test_choice_problem_collection(client):
    print('===== test choice problem collection =====')
    problem = db_pb2.ChoiceQuestion()
    problem.id = 1
    problem.description = '测试'
    problem.answser = 'A'
    problem.option_a = 'A'
    problem.option_b = 'B'
    problem.option_c = 'C'
    problem.option_d = 'D'
    client.create_choice_problem(problem)
    
def main():
    client = MyMongoClient()
    drop_all_collections(client)
    test_choice_problem_collection(client)

if __name__ == '__main__':
    main()