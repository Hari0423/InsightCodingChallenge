# Insight Data Engineering Coding Challenge
import sys
import json
import time

def main(inputF, outputF):
    """
    main function loads transactions into memory line by line and verifies the 60sec time frame
    :param inputF: path of input text file that contains Venmo transactions
    :param outputF: path of output text file to which rolling median is printed to
    """
    graph = {}      # Grpah dictionary that contains the vertices and edges
    times = []      # List that contains the timestamps for the 60sec time frame
    actors = []     # 2D list (list of list) that contains target-actor for transactions in the 60sec time frame

    fi = open(inputF,'r')
    open(outputF, 'w').close()      # make the output file empty
    fo = open(outputF,'w')

    for line in fi:
        data = json.loads(line)     # Deserializes transactions into str-object dictionary key-value pair
        """
        data['target'] - target user that the transaction has been made to
        data['actor'] - actor user that has made the transaction
        data['created_time'] - time the transaction was registered
        """

        timestamp = int(time.mktime(time.strptime(data['created_time'],'%Y-%m-%dT%H:%M:%SZ')))
        new_time = []   # new_time and new_actors lists are supplementary DS to facilitate deletion
        new_actors = []
        # First transaction
        if not times:
            times.append(timestamp)
            l=[]
            l.append(data['target'])
            l.append(data['actor'])
            actors.append(l)
            updateGraph(data['target'], data['actor'], graph)
        else:
            sorted(times, reverse=True)
            maximum = times[0]
            # Timestamps and maximum timestamp from the times list are equal
            if maximum == timestamp:
                times.append(timestamp)
                l = []
                l.append(data['target'])
                l.append(data['actor'])
                actors.append(l)
                updateGraph(data['target'],data['actor'],graph)
            else:
                # Scenario 1: Current transaction is greater than max timestamp in times list and is within the 60sec time frame
                if max(timestamp, maximum) == timestamp:
                    if timestamp-maximum <=60:
                        new_time.append(timestamp)
                        l = []
                        l.append(data['target'])
                        l.append(data['actor'])
                        new_actors.append(l)
                        updateGraph(data['target'], data['actor'], graph)
                        for j in range(len(times)):
                            if timestamp-times[j] <=60:
                                new_time.append(times[j])
                                new_actors.append(actors[j])
                            else:
                                break
                        for k in range(len(times)):
                            if times[k] not in new_time:
                                delGraph(actors[k][0],actors[k][1],graph)

                        del times[:]
                        del actors[:]
                        times = new_time[:]
                        actors = new_actors[:]

                    else:
                        # Scenario 2: Current transaction is greater than max timestamp and is greater than 60sec time frame
                        del times[:]
                        del actors[:]
                        graph.clear()
                        times.append(timestamp)
                        l = []
                        l.append(data['target'])
                        l.append(data['actor'])
                        actors.append(l)
                        updateGraph(data['target'], data['actor'], graph)
                else:
                    # Scenario 3: Current transaction is lesser than max timestamp and is lesser than 60sec time frame
                    if maximum-timestamp<=60:
                        times.append(timestamp)
                        l = []
                        l.append(data['target'])
                        l.append(data['actor'])
                        actors.append(l)
                        updateGraph(data['target'], data['actor'], graph)

                    #(else) implicit Scenario 4: Current transaction is lesser than max timestamp
                                                 # and is greater than 60sec time frame, Hence discarded

        # Calculate median of values from grpah dictionary
        med =[]
        for key,value in graph.items():
            med.append(len(value))
        writing = str("%.2f" % median(med)) +"\n"
        fo.write(writing)
    fo.close()


def updateGraph(target, actor, graph):
    """
    updateGraph function adds new vertices and links edges which represents transactions in the graph
    :param target: target user in the transaction
    :param actor: actor user to whom the transaction has been made to
    :param graph: dictionary that contains the graph
    """
    dict_key = target
    dict_value = actor
    if not (dict_key in graph):
        graph[dict_key] = []
        graph[dict_key].append(dict_value)
    else:
        graph[dict_key].append(dict_value)
    if not (dict_value in graph):
        graph[dict_value] = []
        graph[dict_value].append(dict_key)
    else:
        graph[dict_value].append(dict_key)


def delGraph(target, actor, graph):
    """
    delGrpah function deletes the transaction's vertices and edges in the graph
    :param target: target user in the transaction
    :param actor: actor user to whom the transaction has been made to
    :param graph: dictionary that contains the graph
    """
    dict_key = target
    dict_value = actor
    if len(graph[dict_key]) == 1 and graph[dict_key][0] == actor:
        del graph[dict_key]
    elif len(graph[dict_key]) > 1:
        if actor in graph[dict_key]:
            graph[dict_key].remove(actor)
    if len(graph[dict_value]) == 1 and graph[dict_value][0] == target:
        del graph[dict_value]
    elif len(graph[dict_value]) > 1:
        if target in graph[dict_value]:
            graph[dict_value].remove(target)


def median(L):
    """
    Median function calculates the median for a given list
    :param L: List of values from the graph dictionary
    :return: median float
    """
    L = sorted(L)
    n = len(L)
    m = n - 1
    return (L[n/2] + L[m/2]) / 2.00


# arguments -> location of input file and output file
main(sys.argv[1], sys.argv[2])