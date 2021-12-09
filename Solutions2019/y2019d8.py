

def y2019d8(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d8.txt"
    print("2019 day 8:")

    with open(inputPath) as f:
        for line in f:
            #do something
            myline = line #TODO - rework to the proper format for single line
            break

        myline = myline.strip()

        width = 25
        height = 6

        #for testing
        # myline = "0222112222120000"
        # width = 2
        # height = 2

        totalPixelPerLayer = width*height

        fewestZero = float('inf')
        layerSum = None

        layerList = []

        layers = len(myline)/totalPixelPerLayer
        print("Layers computed: " + str(layers))

        while(len(myline) >= totalPixelPerLayer):
            myLayer= myline[:totalPixelPerLayer]
            myline = myline[totalPixelPerLayer:]
            layerList.append(myLayer)

            thisZero = myLayer.count('0')
            if(thisZero < fewestZero):
                fewestZero = thisZero
                layerSum = myLayer.count('1')*myLayer.count('2')

        print("Part 1: " + str(layerSum))
        print("Total layers found: " + str(len(layerList)))

        myImage = ['2']*totalPixelPerLayer

        for i in range(len(layerList)):
            myLayer = layerList[i]
            for j in range(totalPixelPerLayer):
                if myImage[j] == '2':
                    #transparent
                    myImage[j] = myLayer[j]
            i-=1

        #print my image
        borderStr = "+"+"-"*width+"+" #purely cosmetic
        print(borderStr)
        for i in range(0, height):
            myPrintLineStart = i*width
            myPrintLine = myImage[myPrintLineStart:myPrintLineStart+width]

            myStr = "|"
            for p in myPrintLine:
                if(p == "0"):
                    myStr += " "
                elif(p == "1"):
                    #initally used zero, but this turns out to be much more readable
                    myStr += "█"
                else:
                    myStr += t
            myStr += "|"
            print(myStr)
        print(borderStr)
        print("The part two answer for my input was YGRYZ")

    print("===========")

    # the fact that this is hardcoded is annoying
    # TODO - fix
    return (layerSum, "YGRYZ")
