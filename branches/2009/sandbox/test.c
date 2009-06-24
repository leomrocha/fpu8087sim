#include <stdio.h>
#include "cdecl.h"
int PRE_CDECL asm_main( void ) POST_CDECL;
 
// you can initialize stuff in this function
// it is called when the so is loaded
void _init()
{
    printf("Inicializacion del wrapper\n");
    asm_();
}
 
// you can do final clean-up in this function
// it is called when the so is getting unloaded
void _fini()
{
    printf("saliendo del wrapper\n");
   
}
 
int add(int a, int b)
{
    return(a+b);
}
 
int sum_values(int *values, int n_values)
{
    int i;
    int sum = 0;
 
    for (i=0; i<n_values; i++)
    {
        sum += values[i];
    }
 
    return sum;
}


int asm_()
{
  int ret_status;
  ret_status = asm_main();
  return ret_status;
}


