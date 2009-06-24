from ctypes import *
 
# load the shared object
libtest = cdll.LoadLibrary('./libtest.so.1.0')
 
# call the function, yes it is as simple as that!
print libtest.add(10, 20)
 
# call the sum_values() function
# we have to create a c int array for this
array_of_5_ints = c_int * 5
nums = array_of_5_ints()
 
# fill up array with values
for i in xrange(5): nums[i] = i
 
# since the function expects an array pointer, we pass is byref (provided by ctypes)
print libtest.sum_values(byref(nums), 5)
