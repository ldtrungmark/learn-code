import time
from sqlalchemy import create_engine, text

DATABASE_URI = 'postgresql://dummy:dummy@localhost:5432/postgres'
engine = create_engine(DATABASE_URI)


def execution_time(func):
    def wrapper(*args, **kwargs):
        print(f"==> Function name: {func.__name__}")
        t1 = time.perf_counter(), time.process_time()
        result = func(*args, **kwargs)
        t2 = time.perf_counter(), time.process_time()
        run_time = t2[0] - t1[0]
        print(f"== Real time: {run_time:.2f} seconds")
        print(f"== CPU time: {t2[1] - t1[1]:.2f} seconds")
        print()
        return run_time, result

    return wrapper


@execution_time
def query_data(query):
    print("== SQL:", query)
    with engine.connect() as connection:
        result = connection.execute(text(query))
    return result


if __name__ == '__main__':
    query = """
        select * from public.t_upload_idx 
        where device_type = 'Smartphone'
        order by id desc
        offset 1000000
        limit 1000;
    """

    # query = """
    #     select * from public.t_upload_idx 
    #     where device_type = 'Smartphone' and id < 7998002
    #     order by id desc
    #     limit 1000;
    # """

    total = 0
    num_times = 0
    for i in range(5):
        print("Times:",i+1)
        run_time, _ = query_data(query)
        total += run_time
        num_times += 1
        time.sleep(2)
    print("AVG time:", total/num_times) 
