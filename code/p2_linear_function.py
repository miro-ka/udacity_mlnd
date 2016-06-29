#
#
# Regression and Classification programming exercises
#
#


#
#	In this exercise we will be taking a small data set and computing a linear function
#	that fits it, by hand.
#

#	the data set

import numpy as np

sleep = [5,6,7,8,10]
scores = [65,51,75,75,86]


def compute_regression(sleep,scores):

    #	First, compute the average amount of each list

    avg_sleep = float(sum(sleep))/float(len(sleep))
    avg_scores = float(sum(scores))/float(len(scores))

    #	Then normalize the lists by subtracting the mean value from each entry

    normalized_sleep = [float(x)-avg_sleep for x in sleep]
    normalized_scores = [float(x)-avg_scores for x in scores]

    #	Compute the slope of the line by taking the sum over each student
    #	of the product of their normalized sleep times their normalized test score.
    #	Then divide this by the sum of squares of the normalized sleep times.


    # -----APPROACH 1

    #norm_product_sum = 0
    #for index in xrange(len(normalized_sleep)):
    #    norm_product_sum += (normalized_sleep[index] * normalized_scores[index])

    #scores_sum = sum(scores)
    #sleep_sum = sum(sleep)

    #xy_sums = 0
    #for idx in xrange(len(scores)):
    #    xy_sums += (scores[idx] * sleep[idx])


    #slope_tmp1 = (float(len(sleep)) * float(xy_sums)) - (scores_sum * sleep_sum)
    #x_squared = sum([np.square(x) for x in sleep]) * (len(sleep))
    #sum_x_squared = np.square(sum(sleep))
    #slope_tmp2 = x_squared - sum_x_squared

    #slope_ = slope_tmp1 / slope_tmp2

    #print slope_





    norm_product_sum = 0
    for index in xrange(len(normalized_sleep)):
        norm_product_sum += (normalized_sleep[index] * normalized_scores[index])

    sleep_squared_sum = sum([np.square(x) for x in normalized_sleep])
    slope = norm_product_sum/sleep_squared_sum
    print slope

    #	Finally, We have a linear function of the form
    #	y - avg_y = slope * ( x - avg_x )
    #	Rewrite this function in the form
    #	y = m * x + b
    #	Then return the values m, b

    m = slope
    intercept = (sum(scores) - slope*sum(sleep))/(float(len(sleep)))
    b = intercept
    return m,b



if __name__=="__main__":
    m,b = compute_regression(sleep,scores)
    print "Your linear model is y={}*x+{}".format(m,b)
