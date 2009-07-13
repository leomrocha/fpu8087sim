#include <stdio.h>
#include <stdlib.h>
#include "cdecl.h"

int PRE_CDECL _hello_asm( void ) POST_CDECL;
int PRE_CDECL _sum( int ) POST_CDECL; /* prototype for assembly routine */

extern void PRE_CDECL _find_primes( int * a, unsigned n ) POST_CDECL;
 
//cuando python carga es biblioteca ejecuta _init() automaticamente
//puede usarse para inicializar variables u otros procedimientos
void _init()
{
    printf("Inicializacion del wrapper\n");
}
 
//idem _init pero al terminar el programa 
void _fini()
{
    printf("saliendo del wrapper\n");
   
}
 
//simple suma de dos enteros
int add(int a, int b)
{
    return(a+b);
}

//recibe un puntero de enteros 
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

/*hola mundo hecho en ensamblador. ver hello.asm 
Imprime al stdout y retorna 0 */

int hello_asm()
{
  int ret_status;
  ret_status = _hello_asm();
  return ret_status;
}

/* sum recibe un entero N desde python 
y devuelve la sumatoria de 1 a N
sub5.asm
*/

int sum(int n)
{
  return _sum(n);
}


/*busca primos. recibe un parametro desde python 
e imprime en stdout*/

int find_primes(unsigned max)
{
  int status;
  unsigned i;
  int * a;

  a = calloc( sizeof(int), max);

  if ( a ) {

    _find_primes(a,max); /*envia parametro a la funcion en prime2.asm */


    for(i= 0; i < max; i++ )
      printf("%3d %d\n", i+1, a[i]);   
      
    free(a);
    status = 0;
  } else {
    fprintf(stderr, "Can not create array of %u ints\n", max);
    status = 1;
  }

  return status;
}



