import sys
import json
import time

# number of rolling medians should be the same as number of transactions



def main(inputF, outputF):
    graph = {}
    times = []
    actors = []
    fi = open(inputF,'r')

    open(outputF, 'w').close()
    fo = open(outputF,'w')

    for line in fi:
        data = json.loads(line)
        timestamp = int(time.mktime(time.strptime(data['created_time'],
                                                  '%Y-%m-%dT%H:%M:%SZ')))
        new_time = []
        new_actors=[]
        if not times:
            times.append(timestamp)
            l=[]
            l.append(data['target'])
            l.append(data['actor'])
            actors.append(l)
            updateGraph(data['target'], data['actor'], graph)
        else:
            sorted(times)
            maximum = times[0]
            if maximum == timestamp:
                times.append(timestamp)
                l = []
                l.append(data['target'])
                l.append(data['actor'])
                actors.append(l)
                updateGraph(data['target'],data['actor'],graph)
            else:
                if max(timestamp, maximum) == timestamp:        # Scenario 1 update G change
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

                    else:                           #Scenario 3
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
                    if maximum-timestamp<=60:   # Scenario 2
                        times.append(timestamp)
                        l = []
                        l.append(data['target'])
                        l.append(data['actor'])
                        actors.append(l)
                        updateGraph(data['target'], data['actor'], graph)
                    # (else) implicit Scenario 4
        med =[]

        for key,value in graph.items():
            #print key, value
            med.append(len(value))
        #print ""
        writing = str("%.2f" % median(med)) +"\n"
        fo.write(writing)
        #print med
        #print median(med)
    fo.close()

def updateGraph(target, actor, graph):
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
    L = sorted(L)
    n = len(L)
    m = n - 1
    return (L[n/2] + L[m/2]) / 2.00

start_time = time.time()
main(sys.argv[1], sys.argv[2])
#main("/home/varun/MEGAsync/ASU/ResearchDev/Dev/Workspaces/PyCharm/coding-challenge-master/venmo_input/venmo-trans.txt", "/home/varun/MEGAsync/ASU/ResearchDev/Dev/Workspaces/PyCharm/coding-challenge-master/venmo_output/output.txt")
#print("--- %s seconds ---" % (time.time() - start_time))