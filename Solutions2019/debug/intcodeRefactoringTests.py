#file with unit tests for the intcode computer rewrite work

def doIntcodeTests():
    totalTests = 0
    totalFailures = 0

    #do tests

    #day 2
    from Solutions2019.y2019d2 import y2019d2
    r = y2019d2(autoTesting = True)
    e = ("3101878", "8444")
    if(r != e):
        totalFailures +=1
        print("y2019d2 failed:\n\tgot value: " + str(r) + "\n\texpected:  " + str(e))

    #day 5

    if(totalFailures == 0):
        print("All " + str(totalTests) + " tests completed successfully.")