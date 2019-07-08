
#include <mini_mpi3.hpp>
#include <iostream>


int main()
{
  environment env;
  communicator world = env.world();
  std::cout << "Hello from " << world.rank() << std::endl;
  return 0;
}
