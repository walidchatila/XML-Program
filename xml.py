from xml.etree.ElementTree import Element, fromstring, tostring
import io

element_list = []
secondStart = 0

"""
    travers is a recursive function that is also appending the element name into
    element_list. Thr lists is a global variables, nothing is returned
    """
def XML_traverse (a, d = "") :
    assert(a != "")
    global element_list
    element_list.append(a)
    for v in a :
        XML_traverse(v, d + "\t")

"""
    parsing the XML file int oa string, calls on XML_traverse to have both lists filled,
    built a new list called match_found_list that will store all line numbers that are appended to when a match is found
    num_elements_to_match is the integer lenght of how many elements will need to be matched in the second xml file
    """
def XML_solve(r, w):
    global element_list
    s = "<xml>" + "".join(r.read()) + "</xml>"
    assert(type(s) is str)
    
    a = fromstring(s)
    assert(type(a) is Element)
    element_list = element_list
    XML_traverse(a)
    num_elements_to_match = XML_num_of_elements(a)
    assert(num_elements_to_match > 0)
    
    match_found_list = []
    occur = XML_match(element_list, num_elements_to_match)[0]
    match_found_list = XML_match(element_list, num_elements_to_match)[1]
    XML_printer(w, occur, match_found_list)
    return True

"""
    takes input, returns it with a backspace
    """
def XML_num_of_elements (a):
    global element_list, secondStart
    p = iter(a)
    e = next(p)
    r = next(p)
    leng = len(element_list)
    lenCounter = -1
    startList = 0
    startSecList = 0
    for i in element_list:
        lenCounter += 1
        if i == e:
            startList = lenCounter
        if i == r:
            startSecList = lenCounter
    secondStart = startSecList
    num_elements_to_match = leng - startSecList
    return num_elements_to_match

"""
    main method where elements are being matched, num_elements_to_match is the number of times counter has to be added
    before an occurance is counter, marker is a variable used to makr when a parent is added, each time marker is modified that position
    at i is apppened to the match_found_list, the conditional statements verify that children match up in the correct order of parent/child
    """
def XML_match(element_list, num_elements_to_match):
    global secondStart
    match_found_list = []
    i = 1
    j = secondStart
    count = 0
    occurance = 0
    while (i < len(element_list) -1):
        if element_list[i].tag == element_list[j].tag:
            count += 1
            j +=1
            HOLD = i
            if count == 1:
                HOLD1 = HOLD
            HOLD = HOLD1
        if j < len(element_list) and element_list[i + 1].tag == element_list[j-1].tag:
            count = 0
            j = secondStart
        if element_list[i].tag != element_list[j-1].tag and count >= 1:
            z = element_list[i]
            for p in element_list[HOLD].iter(element_list[j].tag):
                z = p
            if z.tag != element_list[i].tag and z.tag != element_list[j].tag:
                count = 0
                i -= 1
                j = secondStart
        if count == num_elements_to_match:
            occurance +=1
            match_found_list.append(HOLD)
            count = 0
        if j == len(element_list):
            j = secondStart
        i +=1
    return occurance, match_found_list

"""
    method that will be printing the number of matches and the line that corresponds to each match
    """
def XML_printer(w, occur, match_found_list):
    w.write(str(occur) + "\n")
    if (occur > 0):
        for i in match_found_list:
            w.write(str(i) + "\n")