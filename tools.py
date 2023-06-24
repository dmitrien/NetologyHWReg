import json
import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        arguments = f'{args}, {kwargs}'
        name = old_function.__name__
        start_time = datetime.datetime.now()
        result = old_function(*args, **kwargs)
        end_time = datetime.datetime.now()
        work_time = end_time - start_time
        logs = {'name': name,
            'work_time': work_time,
            'args': arguments,
            'result': result}

        f = open('main.log', 'a', encoding='utf-8')
        json.dump(logs, f, ensure_ascii=False, indent=4, default=str)
        f.close()

        return result

    return new_function


def second_logger(path):
    def __logger(old_function):

        def new_function(*args, **kwargs):

            arguments = f'{args}, {kwargs}'
            name = old_function.__name__
            start_time = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            end_time = datetime.datetime.now()
            work_time = end_time - start_time
            logs = {'name': name,
                    'work_time': work_time,
                    'args': arguments,
                    'result': result}

            f = open(path, 'a', encoding='utf-8')
            json.dump(logs, f, ensure_ascii=False, indent=4, default=str)
            f.close()

            return result

        return new_function

    return __logger