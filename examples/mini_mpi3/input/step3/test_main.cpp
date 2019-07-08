
#include <mini_mpi3.hpp>
#include <iostream>

int main()
{
  environment env;
  communicator world = env.world();

  int a = 1;
  if (world.rank() == 0) {a = 3;}
  world.broadcast_value(a);
  std::cout << "From rank " << world.rank()  << " a = " << a << std::endl;
  
  return 0;
}
