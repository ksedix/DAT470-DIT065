import time
import argparse
import findspark
findspark.init()
from pyspark import SparkContext

def filterlogin(line):
    parts = line.split(":")
    message = parts[3].strip()
    substr1 = "Accepted password for"
    substr2 = "Failed password for"
    substr3 = "message repeated"
    if message.startswith(substr1) or message.startswith(substr2):
        return True
    if message.startswith("message repeated"):
        main_message = parts[4].strip()
        if "Failed password for" in main_message:
            return True
    
        
def extractLoginInfo(line):
    parts = line.split(":")
    day = " ".join(parts[0].split()[:2])
    message = parts[3].strip()
    substr1 = "Failed password for invalid user"
    substr2 = "Failed password for"
    substr3 = "Accepted password for"
    substr4 = "message repeated"
    message_parts = message.split()
    if message.startswith(substr1):
        word_count = len(substr1.split())
        user = message_parts[word_count]
        ip_address = message_parts[word_count+2]
        return (user,(day,"invalid",ip_address,1))
    elif message.startswith(substr2):
        word_count = len(substr2.split())
        user = message.split()[word_count]
        ip_address = message_parts[word_count+2]
        return (user,(day,"unsuccessful",ip_address,1))
    elif message.startswith(substr3):
        word_count = len(substr3.split())
        user = message.split()[word_count]
        ip_address = message_parts[word_count+2]
        return (user,(day,"successful",ip_address,1))
    else:
        word_count = len(substr4.split())
        repeat_count = message.split()[word_count]
        main_message = parts[4]
        if substr1 in main_message:
            user = main_message.split(substr1)[-1].split()[0]
            ip_address = main_message.split(substr1)[-1].split()[2]
            return (user,(day,"invalid",ip_address,int(repeat_count)))
        else:
            user = main_message.split(substr2)[-1].split()[0]
            ip_address = main_message.split(substr2)[-1].split()[2]
            return (user,(day,"unsuccessful",ip_address,int(repeat_count)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute login statistics')
    parser.add_argument('-w','--num-workers',default=1,type=int,
                            help = 'Number of workers')
    parser.add_argument('filename',type=str,help='Input filename')
    args = parser.parse_args()

    start = time.time()
    sc = SparkContext(master = f'local[{args.num_workers}]')
    lines = sc.textFile(args.filename)
    login_data = lines.filter(filterlogin)

    #get the login info in a tuple format
    login_info = login_data.map(extractLoginInfo).cache()

    #a
    #Q: Why does this give the same result as when checking for maximum attempts in individual category?
    all_attempts = login_info.map(lambda x : (x[0],x[1][3]))
    attempts_sum = all_attempts.reduceByKey(lambda a,b : a+b)
    maximum_attempts = attempts_sum.max(key = lambda x : x[1])


    #b,c
    #remap to extract the attributes of interest and prepare for aggregation
    login_tuples = login_info.map(lambda x : ((x[0],x[1][1]),x[1][3]))
    #aggregate(reduce) by the key
    login_tuples = login_tuples.reduceByKey(lambda a,b : a+b)

    successful_logins = login_tuples.filter(lambda x : x[0][1]=="successful")
    maximum_successful = successful_logins.max(key = lambda x : x[1])
    
    unsuccessful_logins = login_tuples.filter(lambda x : x[0][1]=="unsuccessful" or x[0][1]=="invalid")
    unsuccessful_logins = unsuccessful_logins.map(lambda x : (x[0][0],x[1]))
    unsuccessful_logins = unsuccessful_logins.reduceByKey(lambda a,b : a+b)
    maximum_unsuccessful = unsuccessful_logins.max(key = lambda x : x[1])

    #d
    login_tuples_successful = successful_logins.map(lambda x: (x[0][0],(x[1],0)))
    login_tuples_unsuccessful = unsuccessful_logins.map(lambda x: (x[0][0],(0,x[1])))
    login_tuples_modified = login_tuples_successful.union(login_tuples_unsuccessful)
    login_tuples_modified = login_tuples_modified.reduceByKey(lambda a,b : (a[0]+b[0],a[1]+b[1]))
    success_rates = login_tuples_modified.mapValues(lambda x : x[0] * 100 / (x[0]+x[1]))
    maximum_success_rate = success_rates.values().max()
    maximum_success_rates = success_rates.filter(lambda x : x[1]==maximum_success_rate)
    max_success_rates_list = maximum_success_rates.collect()

    #e
    #make the ip address the key
    ip_address_activity = login_info.map(lambda x : (x[1][2],x[1][3]))
    ip_address_activity = ip_address_activity.reduceByKey(lambda a,b : a+b)
    top_3_ip_addresses = ip_address_activity.takeOrdered(3, key = lambda x : -x[1])

    #f
    #here, we are specifically interested in invalid logins, i.e. where the provided user account was invalid
    invalid_logins = login_tuples.filter(lambda x : x[0][1]=="invalid")
    maximum_invalid = invalid_logins.values().max()
    maximum_invalid_list = invalid_logins.takeOrdered(10,key = lambda x : -x[1])

    #g
    #make the day the key
    login_activity = login_info.map(lambda x : ((x[1][0]),x[1][3]))
    login_activity = login_activity.reduceByKey(lambda a,b: a+b)
    max_login_activity = login_activity.max(key = lambda x : x[1])
    min_login_activity = login_activity.min(key = lambda x : x[1])

    #a
    #user with maximum number of successful+unsuccessful login attempts and number of attempts
    print(f'Maximum attempts: {maximum_attempts}')

    #b
    #user with most successful login attempts and number of attempts
    print(f'Maximum successful: {maximum_successful}')

    #c
    #user(valid or invalid) with most unsuccessful login attempts and number of attempts
    print(f'Maximum unsuccessful: {maximum_unsuccessful}')

    #d
    #the maximum success rate in logging in
    print(f'Maximum success rate: {maximum_success_rate}%')
    #List of all accounts with maximum login success rate
    print(f'List of people with Maximum success rate {max_success_rates_list}')

    #e
    #Top 3 Ip address with most failed login attempts. These will be reported
    print(f'Top 3 Ip address failed login: {top_3_ip_addresses}')

    #f
    #Most failed login attempts for invalid account
    print(f'Maximum invalid: {maximum_invalid}')
    #Top 10 invalid accounts with most failed login attempts
    print(f'Top 10 invalid: {maximum_invalid_list}')

    #g
    #The day with the highest login activity seen to amount of successful/unsuccessful logins
    print(f'Maximum login activity: {max_login_activity}')
    #The day with the lowest login activity seen to amount of successful/unsuccessful logins
    print(f'Minimum login activity: {min_login_activity}')

