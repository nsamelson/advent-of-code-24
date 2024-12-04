def fizzBuzz(n):
    for i in range(1,n+1):
        if i % 3==0 and i % 5 ==0:
            print("FizzBuzz")
        elif i % 3==0 and i % 5 !=0:
            print("Fizz")
        elif i % 3!=0 and i % 5 ==0:
            print("Buzz")
        else:
            print(i)

# if __name__ == '__main__':
#     n = int(input().strip())

# fizzBuzz(15)

# powered by electricity = 0
# powered by solar = 1  WANT THIS AS MUCH AS POSSIBLE

# can replace a 0 by a 1 if not adjacent to any other 1s

def getMaxSolar(bulbs):

    output = ""

    for i,char in enumerate(bulbs):
        if char =="1":
            output += char
        elif char == "0":
            # start or end
            if i == 0 or i == len(bulbs) - 1:

                if i == 0 and bulbs[i+1] == "0":
                    output += "1"
                # end
                elif i == len(bulbs) - 1 and output[i-1] == "0":
                    output += "1"
                else:
                    output += char
            else:
                if bulbs[i+1] == "0" and output[i-1] == "0":
                    output += "1"
                else:
                    output += char
        else:
            continue

    count = list(output).count("1")
    return count

# out = getMaxSolar("01100110000010")
# print(out)

# Question 2
# compute overall qualityScore = max possible sum of consecutive ratings
# each item is rated by customers based on quality and environmental impact
# to improve quality score, we have integer impactFactor and 2 strats:
#   - amplify ratings: select contiguous segment of ratings and multiply each rating in that range by impact factor
#   - adjust ratings: select a contiguous segment and divide each rating in that range by impact factor
# apply one of the strategies to find the max qualityscore

import math

def calculateMaxQualityScore(impactFactor, ratings):
    segments = [(i,j) for i in range(len(ratings)) for j in range(i, len(ratings))]
    
    sum_ratings_per_seg = []
    for segment in segments:
        mult_ratings = []
        div_ratings = []
        for i,rate in enumerate(ratings):

            # if rating within segment
            if i >= segment[0] and i <= segment[1]:
                mult_ratings.append(rate * impactFactor)
                
                div_method = math.floor if rate >=0 else math.ceil
                div_ratings.append(div_method(rate / impactFactor)) 
            else:
                mult_ratings.append(rate)
                div_ratings.append(rate)

        # sum the stuff and add to repertory
        sum_ratings_per_seg.append(sum(mult_ratings))
        sum_ratings_per_seg.append(sum(div_ratings))

    return max(sum_ratings_per_seg)

impact_factor = 3
ratings = [1,4,-2,3,-3,-1]

score = calculateMaxQualityScore(impact_factor, ratings)
print(score)