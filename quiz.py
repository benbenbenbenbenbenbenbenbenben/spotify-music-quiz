import json
import time

def read_quiz_file(file):
    try:
        with open(f'logs/{file}.json') as f:
            return json.load(f)
    except OSError as e: 
        print('No active quiz')
        return False
        
def write_quiz_file(file, data):
    with open(f'logs/{file}.json', 'w') as f:
       json.dump(data, f)

def new_quiz(name):
    # Merge Active Data to Previous
    active_quiz = read_quiz_file('active-quiz')
    previous_quizzes = read_quiz_file('previous-quizzes')
    try:
        data = previous_quizzes + [active_quiz]
        write_quiz_file('previous-quizzes', data)
        # Store New ID, Name, TS, reset categories
        quiz = {
            'quiz': 
            {
                'id': str(len(previous_quizzes) + 1),
                'name': name,
                'timestamp': time.time(),
                'categories': [] 
            }
        }

    # No Previous File
    except:
        try:
            data = [active_quiz]
            write_quiz_file('previous-quizzes', data)
            quiz = {
                'quiz': 
                {
                    'id': str(len(previous_quizzes) + 1),
                    'name': name,
                    'timestamp': time.time(),
                    'categories': [] 
                }
            }
        # No Active or Previos File
        except:
            try:
                print("Could not merge active and previous")
                quiz = {
                    'quiz': 
                    {
                        'id': "1",
                        'name': name,
                        'timestamp': time.time(),
                        'categories': [] 
                    }
                }
            except:
                pass

    write_quiz_file('active-quiz', quiz)
