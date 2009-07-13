from ctypes import *
 
# load the shared object
libtest = cdll.LoadLibrary('./libtest.so.1.0')
 
# call the function, yes it is as simple as that!
print libtest.add(10, 20)

#llamo a hello de asm
libtest.hello_asm()
 

n = int(raw_input(u'ingrese limite de sumantoria: '))
print "La sumatoria de 1 a %i es %i" % (n, libtest.sum(c_uint(n)))



#ahora otra funcion asm, esta vez con un parametro
max = int(raw_input(u'cuanto primos queres encontrar?'))
primos = libtest.find_primes(c_uint(max))  #el tipo de datos que espera C es unsigned
print primos

 
# call the sum_values() function
# we have to create a c int array for this
array_of_5_ints = c_int * 5
nums = array_of_5_ints()
 
# fill up array with values
for i in xrange(5): nums[i] = i
 
# since the function expects an array pointer, we pass is byref (provided by ctypes)
print libtest.sum_values(byref(nums), 5)
